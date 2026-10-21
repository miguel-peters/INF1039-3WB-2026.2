from django.shortcuts import render

from .models import Aula

def login_view(request):
    return render(request, "login.html")

def feed(request):
    return render(request, "feed.html")

def minhas_aulas(request):
    aulas = Aula.objects.all()

    contexto = {
        "aulas": aulas
    }

    return render(request, "minhas_aulas.html", contexto)


