from django.contrib import admin
from .models import Workspace, Projeto, Tarefa, Comentario

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'criado_em')
    search_fields = ('nome', 'tipo')
    list_filter = ('tipo',)

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'workspace', 'status', 'prazo_entrega', 'criado_em')
    list_filter = ('status', 'workspace')
    search_fields = ('nome', 'descricao')

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'projeto', 'responsavel', 'prioridade', 'status', 'prazo_entrega')
    list_filter = ('status', 'prioridade', 'projeto', 'responsavel')
    search_fields = ('titulo', 'descricao')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'tarefa', 'criado_em')
    list_filter = ('criado_em', 'autor', 'tarefa')
    search_fields = ('texto', 'autor__username', 'tarefa__titulo')
