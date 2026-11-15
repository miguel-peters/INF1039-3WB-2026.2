from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Curso, Papel, Disciplina, Usuario, Aula, Chat, Mensagem


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Dados da plataforma', {'fields': ('nome', 'curso', 'papel', 'preferencias', 'disciplinas')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Dados da plataforma', {'fields': ('email', 'nome', 'curso', 'papel')}),)


# Register your models here.
admin.site.register(Curso)
admin.site.register(Papel)
admin.site.register(Disciplina)
admin.site.register(Aula)
admin.site.register(Chat)
admin.site.register(Mensagem)
