from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('add_ingredients/<int:dish_id>/<int:ingredient_count>/', views.add_ingredient, name='add_ingredients'),
]