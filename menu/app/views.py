from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Dish, DishIngredient
from .forms import ProductForm, DishForm, DishIngredientForm


# Create your views here.
DishIngredientFormSet = modelformset_factory(
    DishIngredient,
    form=DishIngredientForm,
    extra=1,  # Это добавляет одну пустую форму по умолчанию для добавления нового ингредиента
    can_delete=True  # Можно добавлять/удалять ингредиенты
)


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
