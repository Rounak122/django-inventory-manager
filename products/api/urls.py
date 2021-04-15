from products.api.views import *
from django.urls import path

app_name = 'products'
urlpatterns = [
    path('get_product', get_product),
    path('update_product', update_product),
    path('create_product', create_product),
    path('delete_product', delete_product),
]
