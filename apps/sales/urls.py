from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('get_order/', login_required(get_order), name='get_order'),
    path('sales/', login_required(SalesList.as_view()), name='sales'),
    path('sales_save/', login_required(sales_save), name='sales_create'),

    path('purchase_save/', login_required(purchase_save), name='purchase_save'),
    path('purchase/', login_required(PurchaseList.as_view()), name='purchase'),

    path('pawns/', login_required(PawnsList.as_view()), name='pawns'),
    path('modal_pawns/', login_required(modal_pawns), name='modal_pawns'),
    path('pawns_save/', login_required(pawns_save), name='pawns_save'),

    path('returns/', login_required(ReturnList.as_view()), name='returns'),
    path('get_pawns_by_provider/', login_required(get_pawns_by_provider), name='get_pawns_by_provider'),
    path('modal_return_pawns/', login_required(modal_return_pawns), name='modal_return_pawns'),
    path('return_save/', login_required(return_save), name='return_save'),

    path('delete_order_detail/', login_required(delete_order_detail), name='delete_order_detail'),
    path('get_sales_month/', login_required(get_sales_month), name='get_sales_month'),
    path('get_sales_week/', login_required(get_sales_week), name='get_sales_week'),
    path('report/', login_required(ReportList.as_view()), name='report'),
    path('get_orders/', login_required(get_orders), name='get_orders')
]
