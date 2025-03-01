from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Dish
from .forms import ProductForm, DishForm, DishIngredientForm

DEFAULT_WEIGHT = Decimal(1000)
NUTRIENT_CONST = 10


@login_required
def product_list(request):
    query = request.GET.get('search', '').strip()
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'app/products.html', {'products': products, 'search_query': query})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    return render(request, 'app/add_product.html', {'form': form})

@login_required
def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    weight_str = request.GET.get('weight', DEFAULT_WEIGHT)  # строка по умолчанию
    try:
        weight = Decimal(weight_str)
    except ValueError:
        weight = DEFAULT_WEIGHT

    calc_k = weight / DEFAULT_WEIGHT  # Коофицент веса
    ingredients = dish.ingredients.all()
    recalculated_ingredients = []

    total_price = Decimal(0)
    total_values = {
        'calories': 0,
        'proteins': Decimal(0),
        'fats': Decimal(0),
        'carbohydrates': Decimal(0),
    }
    # Перерасчет ингредиентов
    for product in ingredients:
        brutto_per_weight = product.brutto * calc_k
        netto_per_weight = product.netto * calc_k

        price_per_weight = brutto_per_weight * (product.product.price / DEFAULT_WEIGHT)  # Цена по брутто
        total_price += price_per_weight

        for nutrient in ['calories', 'proteins', 'fats', 'carbohydrates']:
            total_values[nutrient] += getattr(product.product, nutrient) * calc_k

        recalculated_ingredients.append({
            'product': product.product,
            'brutto': brutto_per_weight.quantize(Decimal('0.01')),
            'netto': netto_per_weight.quantize(Decimal('0.01')),
            'price': price_per_weight.quantize(Decimal('0.01')),
        })

    return render(request, 'app/dish.html', {
        'dish': dish,
        'ingredients': recalculated_ingredients,
        'weight': weight,
        'total_price': total_price.quantize(Decimal('0.01')),
        'total_calories': total_values['calories'],
        'total_proteins': total_values['proteins'].quantize(Decimal('0.01')),
        'total_fats': total_values['fats'].quantize(Decimal('0.01')),
        'total_carbs': total_values['carbohydrates'].quantize(Decimal('0.01')),
    })


@login_required
def add_dish(request):
    if request.method == 'POST':
        dish_form = DishForm(request.POST, request.FILES)
        # Количество ингредиентов
        ingredient_count = int(request.POST.get('ingredient_count', 0))

        if dish_form.is_valid():
            # Сохраняем блюдо, но не ингредиенты пока
            dish = dish_form.save(commit=False)
            dish.author = request.user
            dish.save()
            print(ingredient_count)
            return redirect('add_ingredients', dish_id=dish.id, ingredient_count=ingredient_count)
    else:
        dish_form = DishForm()

    return render(request, 'app/add_dish.html', {
        'dish_form': dish_form,
    })

@login_required
def add_ingredient(request, dish_id, ingredient_count):
    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == 'POST':
        formset = []
        for i in range(ingredient_count):
            form = DishIngredientForm(request.POST, prefix=f"ingredient_{i}")
            formset.append(form)

        # Проверяем, если все формы валидны
        if all(form.is_valid() for form in formset):
            # Сохраняем все ингредиенты для блюда
            for form in formset:
                dish_ingredient = form.save(commit=False)
                dish_ingredient.dish = dish
                dish_ingredient.save()

            return redirect('dish_detail', dish_id=dish.id)
    else:
        formset = [DishIngredientForm(prefix=f"ingredient_{i}") for i in range(ingredient_count)]

    # скрытые поля для управления формами
    management_form = {
        'TOTAL_FORMS': ingredient_count,
        'INITIAL_FORMS': 0,
        'MAX_NUM_FORMS': ingredient_count
    }

    return render(request, 'app/add_ingredients.html', {
        'dish': dish,
        'formset': formset,
        'ingredient_count': ingredient_count,
        'management_form': management_form
    })
