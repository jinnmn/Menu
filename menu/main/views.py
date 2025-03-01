import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from app.models import Dish


def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'main/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Входим в систему
            return redirect('index')
    else:
        form = AuthenticationForm()  # Пустая форма для
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    all_dishes = Dish.objects.all()

    dish_type_filter = request.GET.get('dish_type', None)
    if dish_type_filter:
        all_dishes = all_dishes.filter(dish_type=dish_type_filter)
    if len(all_dishes) < 5:
        random_dishes = all_dishes
    else:
        random_dishes = random.sample(list(all_dishes), 5)
    return render(request, 'main/index.html', {
        'random_dishes': random_dishes,
        'dish_type_filter': dish_type_filter,  # передаем текущий фильтр по типу
        'DISH_TYPES': Dish.DISH_TYPES,  # передаем доступные типы блюд
    })
