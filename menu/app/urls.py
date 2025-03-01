from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('products/', views.product_list, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
]