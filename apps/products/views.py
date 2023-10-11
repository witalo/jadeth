import decimal
from http import HTTPStatus

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.utils import IntegrityError
from django.http import HttpResponse
from apps.products.forms import ProductForm
from apps.products.models import Product, ProductBrand, ProductModel, Color, Store
from apps.users.models import User


class ListProduct(ListView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product_set'
    queryset = Product.objects.filter(is_state=True)


class CreateProduct(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product')


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product')


class DeleteProduct(DeleteView):
    model = Product

    def post(self, request, pk, *args, **kwargs):
        product_obj = Product.objects.get(id=pk)
        product_obj.is_state = False
        product_obj.save()
        return redirect('products:product')


def modal_product_create(request):
    if request.method == 'GET':
        t = loader.get_template('products/product_create.html')
        c = ({
            'brand_set': ProductBrand.objects.all(),
            'model_set': ProductModel.objects.all(),
            'color_set': Color.objects.all()
        })
        return JsonResponse({
            'success': True,
            'form': t.render(c, request),
        })


def get_model_by_brand(request):
    if request.method == 'GET':
        pk = request.GET.get('brand', '')
        if pk:
            brand_obj = ProductBrand.objects.get(id=int(pk))
            model_set = ProductModel.objects.filter(product_brand=brand_obj)
            serialized_data = serializers.serialize('json', model_set)
            return JsonResponse({
                'success': True,
                'model': serialized_data,
            }, status=HTTPStatus.OK)


@csrf_exempt
def product_create(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            description = request.POST.get('description', '')
            product_brand = request.POST.get('brand', '')
            brand_obj = ProductBrand.objects.get(id=int(product_brand))
            product_model = request.POST.get('model', '')
            model_obj = ProductModel.objects.get(id=int(product_model))
            measures = request.POST.get('measures', '')
            # print(type(request.POST.getlist("color")))
            color = request.POST.getlist("color")
            init = request.POST.get('init', '')
            if init == '':
                init = None
            end = request.POST.get('end', '')
            if end == '':
                end = None
            is_charger = bool(int(request.POST.get('charger', 0)))
            is_add = bool(int(request.POST.get('add', 0)))
            product_obj = Product(
                name=name.upper(),
                description=description,
                product_brand=brand_obj,
                product_model=model_obj,
                measures=measures,
                color=color,
                is_charger=is_charger,
                is_add=is_add,
                is_state=True,
                date_init=init,
                date_end=end)
            product_obj.save()
            return JsonResponse({
                'success': True,
                'product': product_obj.to_json(),
                'message': 'Producto registrado con exito'
            }, status=HTTPStatus.OK)
        except IntegrityError as e:
            return HttpResponse(f"Error al registrar el producto: {str(e)}")
        except Exception as e:
            # Maneja otras excepciones generales
            return HttpResponse(f"Error general: {str(e)}")


def modal_product_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            product_obj = Product.objects.get(id=int(pk))
            t = loader.get_template('products/product_update.html')
            c = ({
                'product_obj': product_obj,
                'brand_set': ProductBrand.objects.all(),
                'model_set': ProductModel.objects.all(),
                'color_set': Color.objects.all()
            })
            return JsonResponse({
                'success': True,
                'form': t.render(c, request),
            })


@csrf_exempt
def product_update(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', '')
        if pk:
            name = request.POST.get('name', '')
            description = request.POST.get('description', '')
            product_brand = request.POST.get('brand', '')
            brand_obj = ProductBrand.objects.get(id=int(product_brand))
            product_model = request.POST.get('model', '')
            model_obj = ProductModel.objects.get(id=int(product_model))
            measures = request.POST.get('measures', '')
            color = request.POST.getlist("color")
            is_charger = bool(int(request.POST.get('charger', 0)))
            is_add = bool(int(request.POST.get('add', 0)))
            product_obj = Product.objects.get(id=int(pk))
            product_obj.name = name
            product_obj.description = description
            product_obj.product_brand = brand_obj
            product_obj.product_model = model_obj
            product_obj.measures = measures
            product_obj.color = color
            product_obj.is_charger = is_charger
            product_obj.is_add = is_add
            product_obj.save()
            return JsonResponse({
                'success': True,
                'message': 'Producto actualizado con exito'
            }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'success': False,
                'message': 'No se logro identificar el producto'
            }, status=HTTPStatus.OK)


def search_product(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        product = []
        if search:
            product_set = Product.objects.filter(name__icontains=search)
            for p in product_set:
                product.append({
                    'pk': p.id,
                    'name': p.name.upper(),
                    'measure': p.measures,
                    'color': p.get_color(),
                    'date': p.date_end,
                    'store': p.get_store(request.user),
                })
        return JsonResponse({
            'status': True,
            'product': product
        })


def modal_store_create(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            product_obj = Product.objects.get(id=int(pk))
            t = loader.get_template('products/product_store_create.html')
            c = ({
                'product_obj': product_obj
            })
            return JsonResponse({
                'success': True,
                'form': t.render(c, request),
            })


@csrf_exempt
def store_create(request):
    if request.method == 'POST':
        try:
            product = request.POST.get('product', '')
            quantity = request.POST.get('quantity', '')
            price = request.POST.get('price', '')
            product_obj = Product.objects.get(id=int(product))
            user = request.user.id
            user_obj = User.objects.get(id=int(user))
            store_obj = Store(
                product=product_obj,
                subsidiary=user_obj.subsidiary,
                quantity=decimal.Decimal(quantity),
                price=decimal.Decimal(price),
            )
            store_obj.save()
            return JsonResponse({
                'success': True,
                'store': store_obj.to_json(),
                'message': 'Stock creado con exito'
            }, status=HTTPStatus.OK)
        except IntegrityError as e:
            return HttpResponse(f"Error al registrar el stock: {str(e)}")
        except Exception as e:
            # Maneja otras excepciones generales
            return HttpResponse(f"Error general: {str(e)}")


def modal_store_update(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', '')
        if pk:
            store_obj = Store.objects.get(id=int(pk))
            product_obj = store_obj.product
            t = loader.get_template('products/product_store_update.html')
            c = ({
                'product_obj': product_obj,
                'store_obj': store_obj
            })
            return JsonResponse({
                'success': True,
                'form': t.render(c, request),
            })


@csrf_exempt
def store_update(request):
    if request.method == 'POST':
        pk = request.POST.get('pk', '')
        price = request.POST.get('price', '')
        store_obj = Store.objects.get(id=int(pk))
        store_obj.price = decimal.Decimal(price)
        store_obj.save()
        return JsonResponse({
            'success': True,
            'store': store_obj.to_json(),
            'message': 'Precio actualizado con exito'
        }, status=HTTPStatus.OK)


def output_store(detail_obj=None, user_obj=None):
    if detail_obj:
        product_obj = detail_obj.product
        subsidiary_obj = user_obj.subsidiary
        store_set = Store.objects.filter(product=product_obj, subsidiary=subsidiary_obj)
        if store_set.exists():
            store_obj = store_set.first()
            old_quantity = store_obj.quantity
            store_obj.quantity = decimal.Decimal(old_quantity) - decimal.Decimal(detail_obj.quantity)
            store_obj.save()


def output_update_store(detail_obj=None, user_obj=None, quantity=0):
    if detail_obj and decimal.Decimal(quantity) > 0:
        product_obj = detail_obj.product
        subsidiary_obj = user_obj.subsidiary
        store_set = Store.objects.filter(product=product_obj, subsidiary=subsidiary_obj)
        if store_set.exists():
            store_obj = store_set.first()
            old_quantity = store_obj.quantity
            new_quantity = decimal.Decimal(detail_obj.quantity) - decimal.Decimal(quantity)
            store_obj.quantity = decimal.Decimal(old_quantity) - new_quantity
            store_obj.save()


def input_store(detail_obj=None, user_obj=None):
    if detail_obj:
        product_obj = detail_obj.product
        subsidiary_obj = user_obj.subsidiary
        store_set = Store.objects.filter(product=product_obj, subsidiary=subsidiary_obj)
        if store_set.exists():
            store_obj = store_set.first()
            old_quantity = store_obj.quantity
            store_obj.quantity = decimal.Decimal(old_quantity) + decimal.Decimal(detail_obj.quantity)
            store_obj.save()
        else:
            store_obj = Store(
                product=product_obj,
                subsidiary=user_obj.subsidiary,
                quantity=decimal.Decimal(detail_obj.quantity),
                price=decimal.Decimal(detail_obj.price)
            )
            store_obj.save()


def input_update_store(detail_obj=None, user_obj=None, quantity=0):
    if detail_obj and decimal.Decimal(quantity) > 0:
        product_obj = detail_obj.product
        subsidiary_obj = user_obj.subsidiary
        store_set = Store.objects.filter(product=product_obj, subsidiary=subsidiary_obj)
        if store_set.exists():
            store_obj = store_set.first()
            old_quantity = store_obj.quantity
            new_quantity = decimal.Decimal(detail_obj.quantity) - decimal.Decimal(quantity)
            store_obj.quantity = decimal.Decimal(old_quantity) + new_quantity
            store_obj.save()
