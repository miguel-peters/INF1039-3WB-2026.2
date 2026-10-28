import unicodedata
 
from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.db.models import Q
from django.utils import timezone
from django.utils.html import format_html, format_html_join
 
from .models import Aula, Curso, Disciplina, Usuario

 
def normalizar(texto):
    decomposto = unicodedata.normalize('NFD', texto)
    sem_acento = ''.join(c for c in decomposto if unicodedata.category(c) != 'Mn')
    return ' '.join(sem_acento.casefold().split())
 
 
def _achar_ou_criar(modelo, nome):
    alvo = normalizar(nome)
    for objeto in modelo.objects.all():
        if normalizar(objeto.nome) == alvo:
            return objeto
    return modelo.objects.create(nome=' '.join(nome.split()))
 
 
class DatalistInput(forms.TextInput):
 
    def __init__(self, sugestoes=(), attrs=None):
        super().__init__(attrs)
        self.sugestoes = sugestoes
 
    def _opcoes(self):
        itens = self.sugestoes() if callable(self.sugestoes) else self.sugestoes
        return format_html_join('', '<option value="{}">', ((item,) for item in itens))
 
    def render(self, name, value, attrs=None, renderer=None):
        attrs = dict(attrs or {})
        lista_id = f'lista-{attrs.get("id") or name}'
        attrs['list'] = lista_id
        campo = super().render(name, value, attrs, renderer)
        return format_html('{}<datalist id="{}">{}</datalist>', campo, lista_id, self._opcoes())
 
 
class VariosDatalistInput(DatalistInput):
 
    def __init__(self, sugestoes=(), quantidade=3, attrs=None):
        super().__init__(sugestoes, attrs)
        self.quantidade = quantidade
 
    def value_from_datadict(self, data, files, name):
        return data.getlist(name) if hasattr(data, 'getlist') else data.get(name, [])
 
    def render(self, name, value, attrs=None, renderer=None):
        valores = [v for v in (value or []) if v]
        valores += [''] * max(self.quantidade - len(valores), 0)
        lista_id = f'lista-{name}'
        campos = []
        for posicao, valor in enumerate(valores):
            attrs_campo = dict(attrs or {})
            attrs_campo['list'] = lista_id
            if posicao:  # só o primeiro campo leva o id (ids repetidos são inválidos)
                attrs_campo.pop('id', None)
            campos.append(forms.TextInput.render(self, name, valor, attrs_campo, renderer))
        return format_html(
            '{}<datalist id="{}">{}</datalist>',
            format_html_join('', '{}', ((campo,) for campo in campos)),
            lista_id,
            self._opcoes(),
        )
 
 
class ListaDeTextosField(forms.Field):

    def to_python(self, value):
        itens, vistos = [], set()
        for texto in value or []:
            for parte in str(texto).split(','):
                parte = ' '.join(parte.split())
                if parte and normalizar(parte) not in vistos:
                    vistos.add(normalizar(parte))
                    itens.append(parte)
        return itens
 

class LoginForm(forms.Form):

    email = forms.EmailField(label='E-mail')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
 
    def clean(self):
        dados = super().clean()
        email, senha = dados.get('email'), dados.get('senha')
        if email and senha:
            usuario = Usuario.objects.filter(email__iexact=email).first()
            user = authenticate(username=usuario.username, password=senha) if usuario else None
            if user is None:
                raise forms.ValidationError('E-mail ou senha incorretos.')
            self._user = user
        return dados
 
    def get_user(self):
        return getattr(self, '_user', None)
 
class EsqueciSenhaForm(PasswordResetForm):

    email = forms.EmailField(label='E-mail', max_length=254)
 
    def clean_email(self):
        email = self.cleaned_data['email']
        if not Usuario.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError('Não encontramos nenhuma conta com esse e-mail.')
        return email
 
 
class NovaSenhaForm(SetPasswordForm):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Nova senha'
        self.fields['new_password2'].label = 'Confirme a nova senha'

class CadastroForm(forms.Form):

    email = forms.EmailField(label='E-mail')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)
 
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if Usuario.objects.filter(Q(email__iexact=email) | Q(username__iexact=email)).exists():
            raise forms.ValidationError('Já existe uma conta com esse e-mail.')
        return email
 
    def clean(self):
        dados = super().clean()
        senha, confirmar = dados.get('senha'), dados.get('confirmar_senha')
        if senha and confirmar and senha != confirmar:
            self.add_error('confirmar_senha', 'As senhas não são iguais.')
        if senha:
            try:
                password_validation.validate_password(senha)
            except forms.ValidationError as erro:
                self.add_error('senha', erro)
        return dados
 
    def save(self):
        email = self.cleaned_data['email']
        # O e-mail também é o username (o Django exige um username)
        return Usuario.objects.create_user(username=email, email=email, password=self.cleaned_data['senha'])
 
 
class CompletarCadastroForm(forms.Form):

    nome = forms.CharField(label='Nome', max_length=150)
    curso = forms.CharField(
        label='Curso',
        max_length=100,
        widget=DatalistInput(sugestoes=lambda: Curso.objects.values_list('nome', flat=True)),
    )
    materias = ListaDeTextosField(
        label='Matérias de interesse',
        required=False,
        widget=VariosDatalistInput(
            sugestoes=lambda: Disciplina.objects.values_list('nome', flat=True),
            quantidade=5,
        ),
    )
 
    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        if usuario is not None and not self.is_bound:
            self.initial['nome'] = usuario.nome
            self.initial['curso'] = usuario.curso.nome if usuario.curso else ''
            self.initial['materias'] = list(usuario.disciplinas.values_list('nome', flat=True))
 
    def clean_nome(self):
        return ' '.join(self.cleaned_data['nome'].split())
 
    def clean_curso(self):
        return ' '.join(self.cleaned_data['curso'].split())
 
    def save(self):
        usuario = self.usuario
        usuario.nome = self.cleaned_data['nome']
        usuario.curso = _achar_ou_criar(Curso, self.cleaned_data['curso'])
        usuario.save()
        usuario.disciplinas.set([_achar_ou_criar(Disciplina, nome) for nome in self.cleaned_data['materias']])
        return usuario

 
class FiltroAulaForm(forms.Form):

    busca = forms.CharField(
        required=False,
        label='Buscar matéria',
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: calculo'}),
    )
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        required=False,
        empty_label='Todas',
        label='Disciplina',
    )
    modo = forms.ChoiceField(
        choices=[('', 'Todos os modos')] + Aula.Modo.choices,
        required=False,
        label='Modo',
    )
    so_preferencias = forms.BooleanField(required=False, label='Só as minhas preferências')
 
    def filtrar(self, aulas, usuario):

        if not self.is_valid():
            return aulas
        dados = self.cleaned_data
        if dados['disciplina']:
            aulas = aulas.filter(disciplina=dados['disciplina'])
        if dados['modo']:
            aulas = aulas.filter(modo=dados['modo'])
        if dados['so_preferencias']:
            aulas = aulas.filter(disciplina__in=usuario.disciplinas.all())
        if dados['busca']:
            termo = normalizar(dados['busca'])
            ids = [d.id for d in Disciplina.objects.all() if termo in normalizar(d.nome)]
            aulas = aulas.filter(disciplina_id__in=ids)
        return aulas
 
 
class AulaForm(forms.ModelForm):
 
    class Meta:
        model = Aula
        fields = ['disciplina', 'horario', 'preco', 'local', 'quantidade_alunos', 'modo']
        labels = {
            'disciplina': 'Disciplina',
            'horario': 'Data e horário',
            'preco': 'Preço por hora (R$)',
            'local': 'Local',
            'quantidade_alunos': 'Número de vagas',
            'modo': 'Modo',
        }
        help_texts = {
            'preco': 'Use 0 para aula gratuita.',
            'local': 'Obrigatório para aulas presenciais.',
        }
        widgets = {
            'horario': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'preco': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'quantidade_alunos': forms.NumberInput(attrs={'min': 1}),
        }
 
    def clean_horario(self):
        horario = self.cleaned_data['horario']
        if horario < timezone.now():
            raise forms.ValidationError('Escolha uma data e um horário no futuro.')
        return horario
 
    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if preco < 0:
            raise forms.ValidationError('O preço não pode ser negativo.')
        return preco
 
    def clean_quantidade_alunos(self):
        vagas = self.cleaned_data['quantidade_alunos']
        if vagas < 1:
            raise forms.ValidationError('A aula precisa ter pelo menos 1 vaga.')
        return vagas
 
    def clean(self):
        dados = super().clean()
        if dados.get('modo') == Aula.Modo.PRESENCIAL and not dados.get('local'):
            self.add_error('local', 'Informe o local para aulas presenciais.')
        return dados
 

class FiltroConversaForm(forms.Form):

    papel = forms.ChoiceField(
        choices=[('', 'Todas'), ('aluno', 'Como aluno'), ('tutor', 'Como tutor')],
        required=False,
        label='Conversas',
    )
    busca = forms.CharField(
        required=False,
        label='Buscar conversa',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nome'}),
    )
 
    def contatos(self, usuario):
        """Pessoas com quem o usuário já trocou mensagens, já com o filtro aplicado."""
        contatos = Usuario.objects.filter(
            Q(mensagens_enviadas__usuario_to=usuario) | Q(mensagens_recebidas__usuario_from=usuario)
        ).exclude(pk=usuario.pk).distinct()
 
        if self.is_valid():
            papel = self.cleaned_data['papel']
            if papel == 'aluno':
                contatos = contatos.filter(aulas_criadas__alunos=usuario)
            elif papel == 'tutor':
                contatos = contatos.filter(aulas_inscritas__tutor=usuario)
 
            termo = normalizar(self.cleaned_data['busca'])
            if termo:
                ids = [c.id for c in contatos if termo in normalizar(c.nome or c.username)]
                contatos = contatos.filter(id__in=ids)
 
        return contatos.distinct().order_by('nome')
 
 
class FiltroMinhasAulasForm(forms.Form):

    papel = forms.ChoiceField(
        choices=[('', 'Todas'), ('aluno', 'Que eu assisto'), ('tutor', 'Que eu dou')],
        required=False,
        label='Mostrar',
    )
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        required=False,
        empty_label='Todas',
        label='Disciplina',
    )
    modo = forms.ChoiceField(
        choices=[('', 'Todos os modos')] + Aula.Modo.choices,
        required=False,
        label='Modo',
    )
 
    def aulas(self, usuario):
        """As aulas do usuário, já com o filtro aplicado."""
        papel = self.cleaned_data['papel'] if self.is_valid() else ''
        if papel == 'aluno':
            aulas = Aula.objects.filter(alunos=usuario)
        elif papel == 'tutor':
            aulas = Aula.objects.filter(tutor=usuario)
        else:
            aulas = Aula.objects.filter(Q(tutor=usuario) | Q(alunos=usuario))
 
        if self.is_valid():
            if self.cleaned_data['disciplina']:
                aulas = aulas.filter(disciplina=self.cleaned_data['disciplina'])
            if self.cleaned_data['modo']:
                aulas = aulas.filter(modo=self.cleaned_data['modo'])
 
        return aulas.select_related('tutor', 'disciplina').distinct().order_by('horario')