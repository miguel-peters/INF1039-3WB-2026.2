from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Curso(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Papel(models.Model):
    nome = models.CharField(max_length=50, unique=True) 

    class Meta:
        verbose_name_plural = 'papéis'

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    papel = models.ForeignKey(Papel, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    preferencias = models.TextField(blank=True)
    # Tabela de ligação Usuário/Disciplina: o Django cria a tabela intermediária sozinho
    disciplinas = models.ManyToManyField(Disciplina, blank=True, related_name='usuarios')

    def __str__(self):
        return self.nome or self.username


class Aula(models.Model):
    class Modo(models.TextChoices):
        PRESENCIAL = 'presencial', 'Presencial'
        ONLINE = 'online', 'Online'

   
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aulas_criadas')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name='aulas')

    alunos = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='aulas_inscritas')
    data_lancamento = models.DateTimeField(auto_now_add=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    horario = models.DateTimeField()
    local = models.CharField(max_length=200, blank=True)
    quantidade_alunos = models.PositiveSmallIntegerField(default=1) 
    modo = models.CharField(max_length=10, choices=Modo.choices, default=Modo.PRESENCIAL)

    @property
    def vagas_restantes(self):
        return self.quantidade_alunos - self.alunos.count()

    def __str__(self):
        return f'{self.disciplina} com {self.tutor}'


class Chat(models.Model):
   
    usuario_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    usuario_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    mensagem = models.TextField()
    horario = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['horario']

    def __str__(self):
        return f'{self.usuario_from} → {self.usuario_to}: {self.mensagem[:30]}'
