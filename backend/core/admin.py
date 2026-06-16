from django.contrib import admin
from .models import Workspace, Projeto, Tarefa, Comentario

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'criado_em')
    search_fields = ('nome',)

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'workspace', 'status', 'prazo_entrega')
    list_filter = ('status', 'workspace')

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'projeto', 'responsavel', 'prioridade', 'status')
    list_filter = ('status', 'prioridade', 'projeto')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'autor', 'criado_em')
