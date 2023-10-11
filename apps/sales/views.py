from http import HTTPStatus
import json
import decimal
from django.core import serializers
from django.db.models import Max, Sum, F
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import date, datetime, timedelta

from apps.accounts.models import Account, Payments
from apps.accounts.views import get_number_payment
from apps.clients.models import Client
from apps.products.models import Product, ProductBrand, ProductModel, Color
from apps.products.views import output_store, input_store, output_update_store, input_update_store
from apps.providers.models import Provider
from apps.sales.models import Order, Detail
from apps.users.models import User
from django.utils import timezone

now = timezone.now()


# Create your views here.
class SalesList(ListView):
    model = Product
    template_name = 'sales/sales.html'
    context_object_name = 'product_set'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_date = datetime.now()
        user = self.request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        context["date"] = order_date.strftime("%Y-%m-%d")
        context["account_set"] = Account.objects.filter(subsidiary=subsidiary_obj)
        return context


def get_correlative(subsidiary=None, types=None, order=None):
    if order is not None:
        order_obj = Order.objects.get(id=int(order))
        return order_obj.number
    else:
        number = Order.objects.filter(subsidiary=subsidiary, type=types).aggregate(
            r=Coalesce(Max('number'), int(0))).get('r')
        return number + 1


@csrf_exempt
def sales_save(request):
    if request.method == 'POST':
        order_json = request.POST.get('order', '')
        order = json.loads(order_json)
        client = order['client']
        client_obj = Client.objects.get(id=int(client))
        current = order['date']
        user = request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        payment = order['payment']
        if payment == "" or payment == "0":
            payment = None
        else:
            payment = int(payment)
        amount = order['amount']
        if amount == '' or amount == '0':
            amount = decimal.Decimal(0.00)
        else:
            amount = decimal.Decimal(amount)
        code = order['code']
        account = order['account']
        if account != "" or account != "0":
            account_obj = Account.objects.get(id=int(account))
        pk = None
        if order['order'] != '' and order['order'] != 0 and order['order'] != '0':
            pk = int(order['order'])
        else:
            pk = None
        obj, created = Order.objects.update_or_create(
            id=pk,
            defaults={
                "type": 'V',
                "number": get_correlative(subsidiary=subsidiary_obj, types='V', order=pk),
                "current": current,
                "user": user_obj,
                "client": client_obj,
                "subsidiary": subsidiary_obj,
                "status": 'C'
            })
        if obj:
            for d in order['Detail']:
                detail = d['detail']
                product = d['product']
                product_obj = None
                if product != '0' or product != '':
                    product_obj = Product.objects.get(id=int(product))
                quantity = d['quantity']
                price = decimal.Decimal(d['price'])
                old = decimal.Decimal(d['old'])
                dk = None
                if detail != '0' and detail != '':
                    dk = int(detail)
                else:
                    dk = None
                detail_obj, detail_created = Detail.objects.update_or_create(
                    id=dk,
                    defaults={
                        "order": obj,
                        "product": product_obj,
                        "quantity": decimal.Decimal(quantity),
                        "old_quantity": decimal.Decimal(old),
                        "price": decimal.Decimal(price)
                    })
                if detail_obj:
                    if detail_created:
                        output_store(detail_obj=detail_obj, user_obj=user_obj)
                    else:
                        output_update_store(detail_obj=detail_obj, user_obj=user_obj, quantity=old)
            payment_obj, payment_created = Payments.objects.update_or_create(
                id=payment,
                defaults={
                    'status': 'R',
                    'type': 'I',
                    'order': obj,
                    'payment': 'P',
                    'description': 'PAGO REALIZADO POR VENTA',
                    'code': code,
                    'amount': amount,
                    'date_payment': current,
                    'user': user_obj,
                    'subsidiary': subsidiary_obj,
                    'account': account_obj,
                    'number': get_number_payment(account=account_obj)
                })
            return JsonResponse({
                'success': True,
                'order': obj.id,
                'number': obj.number,
                'message': 'Venta realizada correctamente'
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ocurrio un problema en el proceso'
            }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


def get_order(request):
    if request.method == 'GET':
        order_number = request.GET.get('order', '')
        order_type = request.GET.get('type', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        subsidiary_obj = user_obj.subsidiary
        order_set = Order.objects.filter(type=order_type, subsidiary=subsidiary_obj, number=order_number)
        if order_set.exists():
            order_obj = order_set.last()
            detail = []
            detail_set = Detail.objects.filter(order=order_obj)
            for d in detail_set.order_by('id'):
                row = {
                    'pk': d.id,
                    'id': d.product.id,
                    'product': d.product.name,
                    'measure': d.product.measures,
                    'quantity': d.quantity,
                    'old': d.old_quantity,
                    'price': d.price,
                    'stock': d.product.get_store(user_obj)
                }
                detail.append(row)
            person_obj = None
            if order_type == 'V':
                person_obj = order_obj.client
            elif order_type == 'C' or order_type == 'M':
                person_obj = order_obj.provider
            if order_obj.payments_set.exists():
                payment_obj = order_obj.payments_set.first()
                payment_pk = payment_obj.id
                account_pk = payment_obj.account.id
                amount = payment_obj.amount
                code = payment_obj.code
            else:
                payment_pk = 0
                account_pk = 0
                amount = 0
                code = ''
            return JsonResponse({
                'success': True,
                'pk': order_obj.id,
                'type': order_obj.type,
                'current': order_obj.current,
                'person': person_obj.pk,
                'document': person_obj.document,
                'names': str(person_obj.first_name) + ' ' + str(person_obj.last_name),
                'address': person_obj.address,
                'phone': person_obj.phone,
                'payment': payment_pk,
                'account': account_pk,
                'amount': amount,
                'code': code,
                'detail': detail,
            }, status=HTTPStatus.OK)

        else:
            return JsonResponse({
                'success': False,
                'message': 'No existe ninguna orden con el Numero=' + str(order_number),
            }, status=HTTPStatus.OK)


class PurchaseList(ListView):
    model = Order
    template_name = 'sales/purchases.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_date = datetime.now()
        user = self.request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        context["date"] = order_date.strftime("%Y-%m-%d")
        context["account_set"] = Account.objects.filter(subsidiary=subsidiary_obj)
        return context


@csrf_exempt
def purchase_save(request):
    if request.method == 'POST':
        order_json = request.POST.get('order', '')
        order = json.loads(order_json)
        provider = order['provider']
        provider_obj = Provider.objects.get(id=int(provider))
        current = order['date']
        user = request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        payment = order['payment']
        if payment == "" or payment == "0":
            payment = None
        else:
            payment = int(payment)
        amount = order['amount']
        if amount == '' or amount == '0':
            amount = decimal.Decimal(0.00)
        else:
            amount = decimal.Decimal(amount)
        code = order['code']
        account = order['account']
        if account != "" or account != "0":
            account_obj = Account.objects.get(id=int(account))
        pk = None
        if order['order'] != '' and order['order'] != 0 and order['order'] != '0':
            pk = int(order['order'])
        else:
            pk = None
        obj, created = Order.objects.update_or_create(
            id=pk,
            defaults={
                "type": 'C',
                "number": get_correlative(subsidiary=subsidiary_obj, types='C', order=pk),
                "current": current,
                "user": user_obj,
                "provider": provider_obj,
                "subsidiary": subsidiary_obj,
                "status": 'C'
            })
        if obj:
            for d in order['Detail']:
                detail = d['detail']
                product = d['product']
                product_obj = None
                if product != '0' or product != '':
                    product_obj = Product.objects.get(id=int(product))
                quantity = d['quantity']
                price = decimal.Decimal(d['price'])
                old = decimal.Decimal(d['old'])
                dk = None
                if detail != '0' and detail != '':
                    dk = int(detail)
                else:
                    dk = None
                detail_obj, detail_created = Detail.objects.update_or_create(
                    id=dk,
                    defaults={
                        "order": obj,
                        "product": product_obj,
                        "quantity": decimal.Decimal(quantity),
                        "old_quantity": decimal.Decimal(old),
                        "price": decimal.Decimal(price)
                    })
                if detail_obj:
                    if detail_created:
                        input_store(detail_obj=detail_obj, user_obj=user_obj)
                    else:
                        input_update_store(detail_obj=detail_obj, user_obj=user_obj, quantity=old)
            payment_obj, payment_created = Payments.objects.update_or_create(
                id=payment,
                defaults={
                    'status': 'R',
                    'type': 'E',
                    'order': obj,
                    'payment': 'P',
                    'description': 'PAGO REALIZADO POR VENTA',
                    'code': code,
                    'amount': amount,
                    'date_payment': current,
                    'user': user_obj,
                    'subsidiary': subsidiary_obj,
                    'account': account_obj,
                    'number': get_number_payment(account=account_obj),
                })
            return JsonResponse({
                'success': True,
                'order': obj.id,
                'number': obj.number,
                'message': 'Compra realizada correctamente'
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ocurrio un problema en el proceso'
            }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


class PawnsList(ListView):
    model = Order
    template_name = 'sales/pawns.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_date = datetime.now()
        user = self.request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        context["date"] = order_date.strftime("%Y-%m-%d")
        context["account_set"] = Account.objects.filter(subsidiary=subsidiary_obj)
        return context


def modal_pawns(request):
    if request.method == 'GET':
        date_now = datetime.now()
        t = loader.get_template('sales/modal_pawns.html')
        c = ({
            'brand_set': ProductBrand.objects.all(),
            'model_set': ProductModel.objects.all(),
            'color_set': Color.objects.all(),
            'date': date_now.strftime("%Y-%m-%d")
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


@csrf_exempt
def pawns_save(request):
    if request.method == 'POST':
        order_json = request.POST.get('order', '')
        order = json.loads(order_json)
        provider = order['provider']
        provider_obj = Provider.objects.get(id=int(provider))
        current = order['date']
        user = request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        payment = order['payment']
        if payment == "" or payment == "0":
            payment = None
        else:
            payment = int(payment)
        amount = order['amount']
        if amount == '' or amount == '0':
            amount = decimal.Decimal(0.00)
        else:
            amount = decimal.Decimal(amount)
        code = order['code']
        account = order['account']
        if account != "" or account != "0":
            account_obj = Account.objects.get(id=int(account))
        pk = None
        if order['order'] != '' and order['order'] != 0 and order['order'] != '0':
            pk = int(order['order'])
        else:
            pk = None
        obj, created = Order.objects.update_or_create(
            id=pk,
            defaults={
                "type": 'M',
                "number": get_correlative(subsidiary=subsidiary_obj, types='M', order=pk),
                "current": current,
                "user": user_obj,
                "provider": provider_obj,
                "subsidiary": subsidiary_obj,
                "status": 'P'
            })
        if obj:
            for d in order['Detail']:
                detail = d['detail']
                product = d['product']
                product_obj = None
                if product != '0' or product != '':
                    product_obj = Product.objects.get(id=int(product))
                quantity = d['quantity']
                price = decimal.Decimal(d['price'])
                old = decimal.Decimal(d['old'])
                dk = None
                if detail != '0' and detail != '':
                    dk = int(detail)
                else:
                    dk = None
                detail_obj, detail_created = Detail.objects.update_or_create(
                    id=dk,
                    defaults={
                        "order": obj,
                        "product": product_obj,
                        "quantity": decimal.Decimal(quantity),
                        "old_quantity": decimal.Decimal(old),
                        "price": decimal.Decimal(price)
                    })
                if detail_obj:
                    if detail_created:
                        input_store(detail_obj=detail_obj, user_obj=user_obj)
                    else:
                        input_update_store(detail_obj=detail_obj, user_obj=user_obj, quantity=old)
            payment_obj, payment_created = Payments.objects.update_or_create(
                id=payment,
                defaults={
                    'status': 'R',
                    'type': 'E',
                    'order': obj,
                    'payment': 'P',
                    'description': 'PAGO REALIZADO POR VENTA',
                    'code': code,
                    'amount': amount,
                    'date_payment': current,
                    'user': user_obj,
                    'subsidiary': subsidiary_obj,
                    'account': account_obj,
                    'number': get_number_payment(account=account_obj),
                })
            return JsonResponse({
                'success': True,
                'order': obj.id,
                'number': obj.number,
                'message': 'Operacion realizada correctamente'
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ocurrio un problema en el proceso'
            }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


class ReturnList(ListView):
    model = Order
    template_name = 'sales/returns.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_date = datetime.now()
        context["date"] = order_date.strftime("%Y-%m-%d")
        return context


def get_pawns_by_provider(request):
    if request.method == 'GET':
        dni = request.GET.get('dni', '')
        provider_set = Provider.objects.filter(document=dni)
        if provider_set.exists():
            provider_obj = provider_set.last()
            order_set = Order.objects.filter(type='M', provider=provider_obj)
            temp = loader.get_template('sales/returns_grid_list.html')
            c = ({
                'order_set': order_set,
            })
            return JsonResponse({
                'success': True,
                'message': 'Exito',
                'grid': temp.render(c, request),
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'No se encontraron resultados',
            }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'error': 'Error de petición.'}, status=HTTPStatus.BAD_REQUEST)


def modal_return_pawns(request):
    if request.method == 'GET':
        date_now = datetime.now()
        pk = request.GET.get('pk', '')
        if pk:
            user = request.user.id
            user_obj = User.objects.get(id=int(user))
            subsidiary_obj = user_obj.subsidiary
            order_obj = Order.objects.get(id=int(pk))
            t = loader.get_template('sales/modal_return_pawns.html')
            c = ({
                'order_obj': order_obj,
                'account_set': Account.objects.filter(subsidiary=subsidiary_obj),
                'date': date_now.strftime("%Y-%m-%d")
            })
            return JsonResponse({
                'success': True,
                'form': t.render(c, request),
            })


@csrf_exempt
def return_save(request):
    if request.method == 'POST':
        order_json = request.POST.get('order', '')
        order = json.loads(order_json)
        current = order['date']
        account = order['account']
        amount = order['amount']
        if amount == '' or amount == '0':
            amount = decimal.Decimal(0.00)
        else:
            amount = decimal.Decimal(amount)
        code = order['code']
        account_obj = Account.objects.get(id=int(account))
        user = request.user.id
        user_obj = User.objects.get(id=user)
        subsidiary_obj = user_obj.subsidiary
        pk = None
        order_obj = None
        if order['order'] != '' and order['order'] != 0 and order['order'] != '0':
            pk = int(order['order'])
            order_obj = Order.objects.get(id=int(pk))
        else:
            pk = None
            order_obj = None
        obj, created = Order.objects.update_or_create(
            id=None,
            defaults={
                "type": 'R',
                "number": get_correlative(subsidiary=subsidiary_obj, types='V', order=None),
                "current": current,
                "user": user_obj,
                "provider": order_obj.provider,
                "subsidiary": subsidiary_obj,
                "status": 'C',
                "relative": order_obj.id
            })
        if obj:
            for d in order['Detail']:
                detail = d['detail']
                product = d['product']
                product_obj = None
                if product != '0' or product != '':
                    product_obj = Product.objects.get(id=int(product))
                quantity = d['quantity']
                price = decimal.Decimal(d['price'])
                old = decimal.Decimal(d['old'])
                # dk = None
                # if detail != '0' and detail != '':
                #     dk = int(detail)
                # else:
                #     dk = None
                detail_obj, detail_created = Detail.objects.update_or_create(
                    id=None,
                    defaults={
                        "order": obj,
                        "product": product_obj,
                        "quantity": decimal.Decimal(quantity),
                        "old_quantity": decimal.Decimal(old),
                        "price": decimal.Decimal(price)
                    })
                if detail_obj:
                    if detail_created:
                        output_store(detail_obj=detail_obj, user_obj=user_obj)
                    else:
                        output_update_store(detail_obj=detail_obj, user_obj=user_obj, quantity=old)
                    order_obj.status = 'C'
                    order_obj.save()
            new_payment = {
                'status': 'R',
                'type': 'I',
                'order': obj,
                'payment': 'P',
                'description': 'PAGO POR DEVOLUCION DE PRODUCTO',
                'code': code,
                'amount': amount,
                'date_payment': current,
                'user': user_obj,
                'subsidiary': subsidiary_obj,
                'account': account_obj,
                'number': get_number_payment(account=account_obj)
            }
            payment_obj = Payments.objects.create(**new_payment)
            payment_obj.save()
            return JsonResponse({
                'success': True,
                'order': order_obj.id,
                'number': obj.number,
                'status': order_obj.get_status_display(),
                'message': 'Entrega realizada correctamente'
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Ocurrio un problema en el proceso'
            }, status=HTTPStatus.OK)
    else:
        return JsonResponse({'message': 'Error de peticion.'}, status=HTTPStatus.BAD_REQUEST)


def delete_order_detail(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        o = request.GET.get('o', '')
        if pk:
            detail_obj = Detail.objects.get(id=int(pk))
            user = request.user.id
            user_obj = User.objects.get(id=user)
            if o == 'I':
                input_store(detail_obj=detail_obj, user_obj=user_obj)
            elif o == 'E':
                output_store(detail_obj=detail_obj, user_obj=user_obj)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Detalle eliminado sin afectar el stock',
                }, status=HTTPStatus.OK)
            payment_set = Payments.objects.filter(order=detail_obj.order)
            if payment_set.exists():
                payment_obj = payment_set.first()
                old_amount = payment_obj.amount
                payment_obj.amount = old_amount - detail_obj.quantity * detail_obj.price
                payment_obj.save()
            detail_obj.delete()
            return JsonResponse({
                'success': True,
                'message': 'Detalle eliminado correctamente',
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Detalle sin identificar',
            }, status=HTTPStatus.OK)


def get_sales_month(request):
    if request.method == 'GET':
        date_ = datetime.now()
        year = date_.year
        month = date_.month
        user_id = request.user.id
        user_obj = User.objects.get(id=user_id)
        subsidiary_obj = user_obj.subsidiary
        sales = []
        purchase = []
        m = 1
        while m <= 12:
            s = Detail.objects.filter(order__type='V',
                                      order__current__year=year, order__current__month=m,
                                      order__status='C', order__subsidiary=subsidiary_obj).aggregate(
                r=Coalesce(Sum(F('quantity') * F('price')), decimal.Decimal(0.00))).get('r')
            p = Detail.objects.filter(order__type='C',
                                      order__current__year=year, order__current__month=m,
                                      order__status='C', order__subsidiary=subsidiary_obj).aggregate(
                r=Coalesce(Sum(F('quantity') * F('price')), decimal.Decimal(0.00))).get('r')
            sales.append(s)
            purchase.append(p)
            m += 1
        return JsonResponse({
            'sales': sales,
            'purchase': purchase,
        }, status=HTTPStatus.OK)


def get_sales_week(request):
    if request.method == 'GET':
        date_ = datetime.now()
        week = date_.weekday()
        init = date_ - timedelta(days=int(week))
        user_id = request.user.id
        user_obj = User.objects.get(id=user_id)
        subsidiary_obj = user_obj.subsidiary
        output = []
        days = []
        for i in range(1, 8, 1):
            y = init.year
            m = init.month
            d = init.day
            t = Detail.objects.filter(order__type='V', order__subsidiary=subsidiary_obj, order__current__year=y,
                                      order__current__month=m, order__current__day=d).aggregate(
                r=Coalesce(Sum(F('quantity') * F('price')), decimal.Decimal(0.00))).get('r')
            output.append(t)
            days.append(d)
            init = init + timedelta(days=1)
        return JsonResponse({
            'output': output,
            'days': days
        }, status=HTTPStatus.OK)


# ----------------------------- Report ----------------------------------

class ReportList(ListView):
    model = Order
    template_name = 'reports/orders.html'
    context_object_name = 'order_set'
    date = datetime.now()
    queryset = Order.objects.filter(type='V', current=date.date())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        user_obj = User.objects.get(id=user)
        context["date"] = self.date.strftime("%Y-%m-%d")
        context["type_set"] = Order._meta.get_field('type').choices
        context["count"] = self.queryset.count()
        return context


def get_orders(request):
    if request.method == 'GET':
        t = request.GET.get('type', '')
        init = request.GET.get('init', '')
        end = request.GET.get('end', '')
        user_id = request.user.id
        user_obj = User.objects.get(id=int(user_id))
        subsidiary_obj = user_obj.subsidiary
        if t:
            order_set = Order.objects.filter(subsidiary=subsidiary_obj, type=t, status__in=['C', 'P', 'A'],
                                             current__range=(init, end))
            temp = loader.get_template('reports/orders_grid_list.html')
            c = ({
                'order_set': order_set.order_by('number'),
            })
            return JsonResponse({
                'count': order_set.count(),
                'grid': temp.render(c, request),
            }, status=HTTPStatus.OK)
