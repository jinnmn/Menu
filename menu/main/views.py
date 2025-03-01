from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout


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
    return HttpResponse("Hi!")

def test_view(request):
    return render(request, 'main/test.html')