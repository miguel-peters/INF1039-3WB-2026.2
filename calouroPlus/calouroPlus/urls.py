"""
URL configuration for calouroPlus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from calouroPlusApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name = 'login'),
    path('feed/', views.feed, name = 'feed'),
    path('minhas-aulas/', views.minhas_aulas, name='minhas_aulas'),
    path('completar-cadastro/', views.completar_cadastro, name='completar_cadastro'),
    path('perfil/', views.perfil, name='perfil'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('perfil/', views.perfil, name='perfil'),
    path('completar-cadastro/', views.completar_cadastro, name='completar_cadastro'),
    path('criar-aula/', views.criar_aula, name='criar_aula'),
    path('cadastro/', views.cadastro),
    path('chat/', views.chat),
]
