import random

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from app.models import Dish


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


def test_view(request):
    return render(request, 'main/test.html')


def index(request):
    # Получаем все блюда
    all_dishes = Dish.objects.all()

    # Выбираем случайные 5 блюд
    if len(all_dishes) < 5:
        random_dishes = all_dishes
    else:
        random_dishes = random.sample(list(all_dishes), 5)

    return render(request, 'main/index.html', {'random_dishes': random_dishes})


def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'main/index.html', context)