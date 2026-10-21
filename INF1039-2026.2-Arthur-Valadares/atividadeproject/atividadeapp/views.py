from django.shortcuts import render
from .models import Livro, Lugar

def home(request):
    livros = Livro.objects.all()
    lugares = Lugar.objects.all()
    return render(request, "home.html", {"livros": livros, "lugares": lugares})
