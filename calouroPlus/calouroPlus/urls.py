
"""
URL configuration for calouroPlus project.
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from calouroPlusApp import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN
    path('login/', views.login_view, name='login'),

    # FEED
    path('feed/', views.feed, name='feed'),

    # MINHAS AULAS
    path('minhas-aulas/', views.minhas_aulas, name='minhas_aulas'),

    # DETALHES DA AULA
    path(
        'aulas/<int:aula_id>/detalhes/',
        views.detalhes_aula,
        name='detalhes_aula'
    ),

    # DESINSCREVER-SE DA AULA
    path(
        'aulas/<int:aula_id>/desinscrever/',
        views.desinscrever_aula,
        name='desinscrever_aula'
    ),

    # INSCRIÇÃO EM AULAS
    path(
        'aula/<int:id>/inscrever/',
        views.inscrever,
        name='inscrever'
    ),

    # COMPLETAR CADASTRO
    path(
        'completar-cadastro/',
        views.completar_cadastro,
        name='completar_cadastro'
    ),

    # PERFIL
    path('perfil/', views.perfil, name='perfil'),

    # ESQUECI MINHA SENHA
    path(
        'esqueci-senha/',
        views.esqueci_senha,
        name='esqueci_senha'
    ),

    # REDEFINIR SENHA
    path(
        'redefinir-senha/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='esqueci-senha.html',
            success_url='/login/',
            extra_context={'redefinindo': True},
        ),
        name='password_reset_confirm'
    ),

    # CRIAR AULA
    path('criar-aula/', views.criar_aula, name='criar_aula'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('chat/', views.chat, name = 'chat'),
    path('aula/<int:id>/inscrever/', views.inscrever, name='inscrever'),
    path('conversas/', views.conversas, name='conversas'),

    # CADASTRO
    path('cadastro/', views.cadastro, name='cadastro'),

    # CHAT
    path('chat/', views.chat, name='chat'),
]
