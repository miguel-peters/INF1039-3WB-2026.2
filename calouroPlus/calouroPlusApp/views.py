from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm
from .models import Aula, Usuario, Chat, Curso


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']

        usuario = Usuario.objects.filter(email__iexact=email).first()
        user = authenticate(request, username=usuario.username, password=senha) if usuario else None

        if user is not None:
            login(request, user)
            return redirect('feed')
        form.add_error(None, 'E-mail ou senha incorretos.')

    return render(request, 'login.html', {'form': form})


@login_required
def feed(request):
    aulas = Aula.objects.all()
    return render(request, "feed.html", context = {"aulas": aulas})

def esqueci_senha(request):
    return render(request, 'esqueci-senha.html')

def perfil(request):
    return render(request, 'perfil.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def completar_cadastro(request):
    cursos = Curso.objects.all()
    return render(request, 'completar_cadastro.html', {"cursos": cursos})

def chat(request):
    mensagens = Chat.objects.all()
    return render(request, 'chat.html', {"mensagens": mensagens})

def criar_aula(request):
    return render(request, 'criar-aula.html')
