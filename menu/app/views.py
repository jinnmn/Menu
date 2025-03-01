from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Dish, DishIngredient
from .forms import ProductForm, DishForm, DishIngredientForm


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
    k = weight / Decimal(1000)
    ingredients = dish.ingredients.all()
    total_price = Decimal(0)
    recalculated_ingredients = []

    total_price = Decimal(0)
    total_calories = 0
    total_proteins = Decimal(0)
    total_fats = Decimal(0)
    total_carbs = Decimal(0)
    # Перерасчет ингредиентов
    for ingredient in ingredients:
        brutto_per_weight = ingredient.brutto * k
        netto_per_weight = ingredient.netto * k

        # Добавление в общую сумму
        price_per_weight = ingredient.product.price * k
        total_price += price_per_weight

        total_calories += ingredient.product.calories * k
        total_proteins += ingredient.product.proteins * k
        total_fats += ingredient.product.fats * k
        total_carbs += ingredient.product.carbohydrates * k

        recalculated_ingredients.append({
            'product': ingredient.product,
            'brutto': brutto_per_weight.quantize(Decimal('0.01')),
            'netto': netto_per_weight.quantize(Decimal('0.01')),
            'price': price_per_weight.quantize(Decimal('0.01')),
        })
    # Возвращаем результат в шаблон
    return render(request, 'app/dish.html', {
        'dish': dish,
        'ingredients': recalculated_ingredients,
        'weight': weight,
        'total_price': total_price.quantize(Decimal('0.01')),
        'total_calories': total_calories,  # общие калории
        'total_proteins': total_proteins.quantize(Decimal('0.01')),  # общие белки
        'total_fats': total_fats.quantize(Decimal('0.01')),  # общие жиры
        'total_carbs': total_carbs.quantize(Decimal('0.01')),  # общие углеводы
    })

@login_required
def add_dish(request):
    if request.method == 'POST':
        dish_form = DishForm(request.POST, request.FILES)
        ingredients_formset = []

        if dish_form.is_valid():
            dish = dish_form.save(commit=False)
            dish.author = request.user
            dish.save()

            # Сохранение ингредиентов
            products = request.POST.getlist('ingredients')  # Получаем список выбранных продуктов
            for product_id in products:
                product = Product.objects.get(id=product_id)
                brutto = request.POST.get(f'brutto_{product.id}', 0)
                netto = request.POST.get(f'netto_{product.id}', 0)
                DishIngredient.objects.create(
                    dish=dish,
                    product=product,
                    brutto=brutto,
                    netto=netto
                )

            return redirect('dish_detail', dish_id=dish.id)
    else:
        dish_form = DishForm()
        ingredients_formset = DishIngredientForm()

    return render(request, 'app/add_dish.html', {
        'dish_form': dish_form,
        'ingredients_formset': ingredients_formset,
    })