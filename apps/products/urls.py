from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.products.views import ListProduct, CreateProduct, UpdateProduct, DeleteProduct, modal_product_create, \
    product_create, product_update, get_model_by_brand, modal_product_update, store_create, \
    modal_store_create, modal_store_update, store_update, search_product

urlpatterns = [
    path('product/', login_required(ListProduct.as_view()), name='product'),
    # path('product_create/', login_required(CreateProduct.as_view()), name='product_create'),
    # path('product_update/<int:pk>/', login_required(UpdateProduct.as_view()), name='product_update'),
    path('product_delete/<int:pk>/', login_required(DeleteProduct.as_view()), name='product_delete'),

    path('modal_product_create/', login_required(modal_product_create), name='modal_product_create'),
    path('modal_product_update/', login_required(modal_product_update), name='modal_product_update'),
    path('product_create/', login_required(product_create), name='product_create'),
    path('product_update/', login_required(product_update), name='product_update'),
    path('get_model_by_brand/', login_required(get_model_by_brand), name='get_model_by_brand'),
    path('modal_store_create/', login_required(modal_store_create), name='modal_store_create'),
    path('modal_store_update/', login_required(modal_store_update), name='modal_store_update'),
    path('search_product/', login_required(search_product), name='search_product'),
    path('store_create/', login_required(store_create), name='store_create'),
    path('store_update/', login_required(store_update), name='store_update')
]
