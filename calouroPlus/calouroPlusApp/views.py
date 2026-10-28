from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm

from .forms import LoginForm
from .models import Aula, Usuario, Chat, Papel, Curso, Disciplina


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']

        usuario = Usuario.objects.filter(email__iexact=email).first()
        user = authenticate(
            request,
            username=usuario.username,
            password=senha
        ) if usuario else None

        if user is not None:
            login(request, user)
            return redirect('feed')

        form.add_error(None, 'E-mail ou senha incorretos.')

    return render(request, 'login.html', {'form': form})


@login_required
def feed(request):
    aulas = Aula.objects.all()
    return render(request, 'feed.html', {'aulas': aulas})


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

        if not usuario.is_authenticated:
            return redirect("login")

        usuario.nome = request.POST.get("nome", "").strip()

        nome_curso = request.POST.get("curso", "").strip()

        if nome_curso:
            curso = Curso.objects.filter(
                nome__iexact=nome_curso
            ).first()

            if curso is None:
                curso = Curso.objects.create(nome=nome_curso)

            usuario.curso = curso

        usuario.save()

        materias_texto = request.POST.get("materias", "")

        nomes_materias = [
            nome.strip()
            for nome in materias_texto.split(",")
            if nome.strip()
        ]

        materias = []

        for nome in nomes_materias:
            disciplina = Disciplina.objects.filter(
                nome__iexact=nome
            ).first()

            if disciplina is None:
                disciplina = Disciplina.objects.create(nome=nome)

            materias.append(disciplina)

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


def esqueci_senha(request):
    mensagem = None

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html',
            )
            mensagem = (
                'Se houver uma conta com esse e-mail, '
                'você receberá as instruções para redefinir a senha.'
            )
        else:
            mensagem = 'Digite um e-mail válido.'

    return render(request, 'esqueci-senha.html', {'mensagem': mensagem})



def cadastro(request):
    papeis = Papel.objects.all()

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get("confirmar_senha", "")
        nome_papel = request.POST.get("papel", "")

        if not email or not senha:
            erro = "Preencha o e-mail e a senha."

        elif Usuario.objects.filter(email__iexact=email).exists():
            erro = "Este e-mail já está cadastrado."

        elif senha != confirmar_senha:
            erro = "As senhas não coincidem."

        elif len(senha) < 8:
            erro = "A senha deve ter pelo menos 8 caracteres."

        else:
            papel = Papel.objects.filter(nome=nome_papel).first()

            usuario = Usuario.objects.create_user(
                username=email,
                email=email,
                password=senha,
                papel=papel
            )

            login(request, usuario)
            return redirect("completar_cadastro")

        return render(request, "cadastro.html", {
            "papeis": papeis,
            "erro": erro
        })

    return render(request, "cadastro.html", {
        "papeis": papeis
    })

def chat(request):
    mensagens = Chat.objects.all()
    return render(request, 'chat.html', {"mensagens": mensagens})


def criar_aula(request):
    return render(request, 'criar-aula.html')
