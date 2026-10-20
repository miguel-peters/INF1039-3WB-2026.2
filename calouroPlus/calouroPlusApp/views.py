from django.shortcuts import render

def login_view(request):
    return render(request, "login.html")

def feed(request):
    return render(request, "feed.html")

def esqueci_senha(request):
    return render(request, 'esqueci-senha.html')

def perfil(request):
    return render(request, 'perfil.html')

def completar_cadastro(request):
    return render(request, 'completar_cadastro.html')

def criar_aula(request):
    return render(request, 'criar-aula.html')