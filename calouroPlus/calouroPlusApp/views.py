
import unicodedata

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import LoginForm, FiltroAulaForm
from .models import Aula, Usuario, Chat, Papel, Curso, Disciplina


# LOGIN

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


# NORMALIZAÇÃO DE TEXTO

def normalizar(texto):
    decomposto = unicodedata.normalize('NFD', texto)

    sem_acento = ''.join(
        c for c in decomposto
        if unicodedata.category(c) != 'Mn'
    )

    return sem_acento.casefold().strip()


# FEED

@login_required
def feed(request):
    aulas = Aula.objects.select_related(
        'tutor', 'disciplina'
    ).order_by('horario')

    form = FiltroAulaForm(request.GET or None)

    if form.is_valid():
        busca = form.cleaned_data['busca']
        disciplina = form.cleaned_data['disciplina']
        modo = form.cleaned_data['modo']

        if disciplina:
            aulas = aulas.filter(disciplina=disciplina)

        if modo:
            aulas = aulas.filter(modo=modo)

        if form.cleaned_data['so_preferencias']:
            aulas = aulas.filter(
                disciplina__in=request.user.disciplinas.all()
            )

        if busca:
            termo = normalizar(busca)

            ids = [
                d.id
                for d in Disciplina.objects.all()
                if termo in normalizar(d.nome)
            ]

            aulas = aulas.filter(disciplina_id__in=ids)

    return render(request, 'feed.html', {
        'aulas': aulas,
        'form': form
    })


# INSCRIÇÃO EM AULAS

@login_required
@require_POST
def inscrever(request, id):
    aula = get_object_or_404(Aula, id=id)

    if aula.tutor != request.user and aula.vagas_restantes > 0:
        aula.alunos.add(request.user)

    return redirect('feed')


# MINHAS AULAS - FILTRO

@login_required
def minhas_aulas(request):
    agora = timezone.now()

    aulas = Aula.objects.filter(
        alunos=request.user
    ).select_related(
        'tutor', 'disciplina'
    ).order_by('horario')

    total_proximas = aulas.filter(
        horario__gte=agora
    ).count()

    total_passadas = aulas.filter(
        horario__lt=agora
    ).count()

    filtro = request.GET.get('filtro', 'todas')

    if filtro == 'proximas':
        aulas = aulas.filter(horario__gte=agora)

    elif filtro == 'passadas':
        aulas = aulas.filter(horario__lt=agora)

    else:
        filtro = 'todas'

    contexto = {
        'aulas': aulas,
        'filtro': filtro,
        'total_proximas': total_proximas,
        'total_passadas': total_passadas
    }

    return render(request, 'minhas_aulas.html', contexto)


# DETALHES DA AULA

@login_required
def detalhes_aula(request, aula_id):
    aula = get_object_or_404(
        Aula.objects.select_related(
            'tutor', 'disciplina'
        ),
        id=aula_id,
        alunos=request.user
    )

    contexto = {
        'aula': aula
    }

    return render(request, 'detalhes_aula.html', contexto)


# DESINSCREVER-SE DE UMA AULA

@login_required
@require_POST
def desinscrever_aula(request, aula_id):
    aula = get_object_or_404(
        Aula,
        id=aula_id,
        alunos=request.user
    )

    aula.alunos.remove(request.user)

    return redirect('minhas_aulas')


# COMPLETAR CADASTRO

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

    return render(
        request,
        "completar_cadastro.html",
        contexto
    )


# PERFIL

@login_required
def perfil(request):
    usuario = request.user

    contexto = {
        "usuario": usuario
    }

    return render(request, "perfil.html", contexto)


# RECUPERAÇÃO DE SENHA

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

    return render(request, 'esqueci-senha.html', {
        'mensagem': mensagem
    })


# CADASTRO

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


# CHAT

@login_required
def chat(request):
    usuario = request.user

    papel = request.GET.get("papel", "aluno")

    if papel not in ("aluno", "tutor"):
        papel = "aluno"

    busca = request.GET.get("busca", "").strip()

    mensagens = Chat.objects.filter(
        Q(usuario_from=usuario) | Q(usuario_to=usuario),
        aula__isnull=False
    ).select_related(
        "usuario_from",
        "usuario_to",
        "aula__disciplina"
    )

    if papel == "tutor":
        mensagens = mensagens.filter(aula__tutor=usuario)

    else:
        mensagens = mensagens.filter(aula__alunos=usuario)

    if busca:
        mensagens = mensagens.filter(
            Q(usuario_from__nome__icontains=busca) |
            Q(usuario_to__nome__icontains=busca) |
            Q(usuario_from__username__icontains=busca) |
            Q(usuario_to__username__icontains=busca) |
            Q(aula__disciplina__nome__icontains=busca)
        )

    mensagens = mensagens.order_by("-horario")

    conversas = []
    conversas_vistas = set()

    for mensagem in mensagens:
        outro_usuario = (
            mensagem.usuario_to
            if mensagem.usuario_from_id == usuario.id
            else mensagem.usuario_from
        )

        chave = (mensagem.aula_id, outro_usuario.id)

        if chave in conversas_vistas:
            continue

        conversas_vistas.add(chave)

        conversas.append({
            "usuario": outro_usuario,
            "disciplina": mensagem.aula.disciplina.nome,
            "ultima_mensagem": mensagem.mensagem,
            "horario": mensagem.horario,
        })

    return render(request, "chat.html", {
        "conversas": conversas,
        "papel_ativo": papel,
        "busca": busca
    })


# CRIAR AULA

def criar_aula(request):
    return render(request, 'criar-aula.html')


def conversas(request):
    return render(request, 'conversas.html')
