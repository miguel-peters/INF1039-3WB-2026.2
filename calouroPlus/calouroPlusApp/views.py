# BIBLIOTECAS DO PYTHON
import unicodedata


# BIBLIOTECAS DO DJANGO
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.urls import reverse


# ARQUIVOS DO PROJETO
from .forms import LoginForm, FiltroAulaForm, AulaForm, CompletarCadastroForm
from .models import Aula, Usuario, Chat, Papel, Curso, Disciplina, Mensagem

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
    ).filter(
        horario__gte=timezone.now()
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
        messages.success(request, "Inscrição feita com sucesso!")

    return redirect('feed')


# MINHAS AULAS - FILTRO

@login_required
def minhas_aulas(request):
    agora = timezone.now()

    papel = request.GET.get('papel', 'aluno')
    if papel not in ('aluno', 'tutor'):
        papel = 'aluno'

    aulas = Aula.objects.select_related(
        'tutor', 'disciplina'
    ).order_by('horario')

    if papel == 'tutor':
        aulas = aulas.filter(tutor=request.user)
    else:
        aulas = aulas.filter(alunos=request.user)

    total_proximas = aulas.filter(horario__gte=agora).count()
    total_passadas = aulas.filter(horario__lt=agora).count()

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
        'papel_ativo': papel,
        'total_proximas': total_proximas,
        'total_passadas': total_passadas,
    }

    return render(request, 'minhas_aulas.html', contexto)

#HISTORICO DO TUTOR

@login_required
def historico_tutor(request):
    agora = timezone.now()

    aulas_passadas = Aula.objects.filter(
        tutor=request.user,
        horario__lt=agora
    ).select_related('disciplina').order_by('-horario')

    contexto = {
        'aulas_passadas': aulas_passadas,
    }

    return render(request, 'historico_tutor.html', contexto)

# DETALHES DA AULA

@login_required
def detalhes_aula(request, aula_id):
    aula = get_object_or_404(
        Aula.objects.select_related('tutor', 'disciplina').filter(
            Q(tutor=request.user) | Q(alunos=request.user)
        ).distinct(),
        id=aula_id,

    )

    aula_passada = aula.horario < timezone.now()

    contexto = {
        'aula': aula,
        'aula_passada': aula_passada,
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

    if aula.horario < timezone.now():
        messages.error(
            request,
            "Não é possível cancelar a inscrição em uma aula passada."
        )
        return redirect(
            f"{reverse('minhas_aulas')}?papel=aluno&filtro=passadas"
        )

    aula.alunos.remove(request.user)

    return redirect(
        f"{reverse('minhas_aulas')}?papel=aluno"
    )

# COMPLETAR CADASTRO

@login_required
def completar_cadastro(request):
    contexto = {
        "cursos": list(Curso.objects.values("nome")),
        "disciplinas": list(Disciplina.objects.values("nome")),
    }

    if request.method == "POST":
        usuario = request.user
        nome = request.POST.get("nome", "").strip()
        nome_curso = request.POST.get("curso", "").strip()
        materias_texto = request.POST.get("materias", "")

        erros = []
        curso = None

        if nome_curso:
            curso = Curso.objects.filter(nome__iexact=nome_curso).first()
            if curso is None:
                erros.append(f'Curso não cadastrado: "{nome_curso}".')

        materias = []

        for nome_materia in materias_texto.split(","):
            nome_materia = nome_materia.strip()
            if not nome_materia:
                continue

            disciplina = Disciplina.objects.filter(
                nome__iexact=nome_materia
            ).first()

            if disciplina is None:
                erros.append(f'Matéria não cadastrada: "{nome_materia}".')
            else:
                materias.append(disciplina)

        if erros:
            contexto["erros"] = erros
            return render(request, "completar_cadastro.html", contexto)

        usuario.nome = nome
        if curso is not None:
            usuario.curso = curso

        usuario.save()
        usuario.disciplinas.set(materias)
        
        return redirect("feed")

    return render(request, "completar_cadastro.html", contexto)


# PERFIL

@login_required
def perfil(request):
    usuario = request.user

    contexto = {
        "usuario": usuario
    }

    return render(request, "perfil.html", contexto)

# ALTERAR FOTO DE PERFIL

@login_required
@require_POST
def alterar_foto(request):
    foto = request.FILES.get('foto')

    if foto and foto.content_type in ('image/jpeg', 'image/png') and foto.size <= 5 * 1024 * 1024:
        request.user.foto = foto
        request.user.save()

    return redirect('perfil')

# REMOVER MATÉRIA DO PERFIL

@login_required
@require_POST
def remover_materia(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    request.user.disciplinas.remove(disciplina)

    return redirect('perfil')

# EDITAR PERFIL

@login_required
def editar_perfil(request):
    form = CompletarCadastroForm(request.POST or None, usuario=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("perfil")

    return render(request, "editar-perfil.html", {
    "form": form,
    "cursos": list(Curso.objects.values("nome")),
    "disciplinas": list(Disciplina.objects.values("nome")),
})


# ALTERAR SENHA

@login_required
def alterar_senha(request):
    form = PasswordChangeForm(request.user, request.POST or None)

    if form.is_valid():
        usuario = form.save()
        # sem isso o Django desloga o usuário depois de trocar a senha
        update_session_auth_hash(request, usuario)
        return redirect("perfil")

    return render(request, "alterar-senha.html", {"form": form})


# SAIR

def sair(request):
    logout(request)
    return redirect("login")

# RECUPERAÇÃO DE SENHA

def esqueci_senha(request):
    mensagem = None

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            Usuario = get_user_model()

            usuario = Usuario.objects.filter(
                email__iexact=email
            ).first()

            if usuario:
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='password_reset_email.html',
                )

                mensagem = (
                    f'E-mail cadastrado! Se a conta estiver habilitada '
                    f'para recuperação, o link será enviado para {email}.'
                )

            else:
                mensagem = (
                    'Não encontramos nenhuma conta cadastrada '
                    'com esse e-mail.'
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
    busca = request.GET.get("busca", "").strip()

    papel = request.GET.get("papel", "aluno")
    if papel not in ("aluno", "tutor"):
        papel = "aluno"

    if papel == "tutor":
        aulas = Aula.objects.filter(tutor=usuario).select_related("disciplina")
    else:
        aulas = Aula.objects.filter(alunos=usuario).select_related("disciplina", "tutor")

    conversas = []

    for aula in aulas:

        if papel == "tutor":
            pessoas = aula.alunos.all()
        else:
            pessoas = [aula.tutor]

        for outro in pessoas:
            if outro == usuario:
                continue

            nome = outro.nome or outro.username

            if busca:
                onde_procurar = normalizar(f"{nome} {outro.username} {aula.disciplina.nome}")
                if normalizar(busca) not in onde_procurar:
                    continue

            ultima = Chat.objects.filter(aula=aula).filter(
                Q(usuario_from=usuario, usuario_to=outro) |
                Q(usuario_from=outro, usuario_to=usuario)
            ).order_by("-horario").first()

            if ultima:
                texto = ultima.mensagem
                horario = ultima.horario
            else:
                texto = "Nenhuma mensagem ainda"
                horario = None

            conversas.append({
                "usuario": outro,
                "disciplina": aula.disciplina.nome,
                "ultima_mensagem": texto,
                "horario": horario,
                "aula_id": aula.id,
            })

    conversas.sort(
        key=lambda c: c["horario"].timestamp() if c["horario"] else 0,
        reverse=True
    )

    return render(request, "chat.html", {
        "conversas": conversas,
        "papel_ativo": papel,
        "busca": busca,
    })


# CRIAR AULA
@login_required
def criar_aula(request):
    form = AulaForm(request.POST or None)

    if form.is_valid():
        aula = form.save(commit=False)
        aula.tutor = request.user
        aula.save()
        messages.success(request, "Aula criada com sucesso!")
        return redirect('feed')

    return render(request, 'criar-aula.html', {'form': form})

def participa_da_aula(usuario, aula):
    e_tutor = aula.tutor == usuario
    e_aluno = aula.alunos.filter(id=usuario.id).exists()
    return e_tutor or e_aluno

@login_required
def conversas(request, aula_id, usuario_id):
    eu = request.user
    outro = get_object_or_404(Usuario, id=usuario_id)
    aula = get_object_or_404(Aula, id=aula_id)
    if outro == eu or not participa_da_aula(eu, aula) or not participa_da_aula(outro, aula):
        return redirect('chat')

    mensagens = Chat.objects.filter(aula=aula).filter(
        Q(usuario_from=eu, usuario_to=outro) |
        Q(usuario_from=outro, usuario_to=eu)
    ).order_by('horario')

    if request.method == 'POST':
        texto = request.POST.get('mensagem', '').strip()

        if texto:
            Chat.objects.create(
                aula=aula,
                usuario_from=eu,
                usuario_to=outro,
                mensagem=texto,
            )

    return render(request, 'conversas.html', {
        'mensagens': mensagens,
        'outro': outro,
        'aula': aula,
    })

@login_required
def editar_aula(request, aula_id):
    aula = get_object_or_404(
        Aula,
        id=aula_id,
        tutor=request.user
    )

    if aula.horario < timezone.now():
        messages.error(
            request,
            "Não é possível editar uma aula que já aconteceu."
        )
        return redirect('historico_tutor')

    form = AulaForm(
        request.POST or None,
        instance=aula,
        initial={'disciplina': aula.disciplina.nome}
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(
            f"{reverse('minhas_aulas')}?papel=tutor"
        )

    return render(
        request,
        'criar-aula.html',
        {'form': form, 'aula': aula, 'editando': True}
    )

@login_required
@require_POST
def excluir_aula(request, aula_id):
    aula = get_object_or_404(
        Aula,
        id=aula_id,
        tutor=request.user
    )

    if aula.horario < timezone.now():
        messages.error(
            request,
            "Não é possível excluir uma aula que já aconteceu."
        )
        return redirect('historico_tutor')

    aula.delete()

    return redirect(
        f"{reverse('minhas_aulas')}?papel=tutor"
    )

