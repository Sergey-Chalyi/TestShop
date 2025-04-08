from django.urls import path, include
from .views import *

urlpatterns = [
        path('', all_products, name='all_products'),
    path('category/<slug:category_slug>/', category_detail, name='category_detail'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
]