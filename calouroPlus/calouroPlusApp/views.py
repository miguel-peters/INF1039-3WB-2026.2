from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Aula, Curso, Disciplina

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

@login_required
def completar_cadastro(request):
    cursos = Curso.objects.all()
    disciplinas = Disciplina.objects.all()

    if request.method == "POST":
        usuario = request.user

        usuario.nome = request.POST.get("nome")
        usuario.curso = Curso.objects.get(
            id=request.POST.get("curso")
        )
        usuario.save()

        materias = request.POST.getlist("materias")
        usuario.disciplinas.set(materias)

        return redirect("feed")

    contexto = {
        "cursos": cursos,
        "disciplinas": disciplinas
    }

    return render(request, "completar_cadastro.html", contexto)




@login_required
def perfil(request):
    usuario = request.user

    contexto = {
        "usuario": usuario
    }

    return render(request, "perfil.html", contexto)

