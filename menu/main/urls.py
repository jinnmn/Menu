from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Страница регистрации
    path('login/', views.login_view, name='login'),  # Страница логина
    path('logout/', views.logout_view, name='logout'),  # Страница выхода
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
]
