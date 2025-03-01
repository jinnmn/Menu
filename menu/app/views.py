from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Dish, DishIngredient
from .forms import ProductForm

# Create your views here.

def add_recipe(request):
    return render(request, 'app/add_recipe.html')

def product_list(request):
    query = request.GET.get('search', '').strip()
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'app/products.html', {'products': products, 'search_query': query})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    return render(request, 'app/add_product.html', {'form': form})


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    weight_str = request.GET.get('weight', '1000')  # строка по умолчанию
    try:
        weight = Decimal(weight_str)
    except ValueError:
        weight = 1000.0

    # Перерасчет ингредиентов

    ingredients = dish.ingredients.all()

    recalculated_ingredients = []

    # Перерасчет ингредиентов
    for ingredient in ingredients:
        brutto_per_weight = ingredient.brutto * (weight / Decimal('1000'))
        netto_per_weight = ingredient.netto * (weight / Decimal('1000'))

        recalculated_ingredients.append({
            'product': ingredient.product,
            'brutto': brutto_per_weight.quantize(Decimal('0.01')),  # округление до 2 знаков
            'netto': netto_per_weight.quantize(Decimal('0.01')),  # округление до 2 знаков
        })
    # Возвращаем результат в шаблон
    return render(request, 'app/dish.html', {
        'dish': dish,
        'ingredients': recalculated_ingredients,
        'weight': weight
    })