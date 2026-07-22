from django.contrib.auth.models import User
from django.db import models


class Workspace(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    status = models.CharField(max_length=50)
    prazo_entrega = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE
    )
    responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    prioridade = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    prazo_entrega = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    tarefa = models.ForeignKey(
        Tarefa,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} em {self.tarefa.titulo}'


class Nota(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notas'
    )
    titulo = models.CharField(max_length=120, default='Minha nota')
    itens = models.JSONField(default=list, blank=True)
    itens_concluidos = models.JSONField(default=list, blank=True)
    pos_x = models.IntegerField(default=24)
    pos_y = models.IntegerField(default=120)
    fixada = models.BooleanField(default=False)
    visivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.titulo} - {self.usuario.username}'
