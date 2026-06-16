from django.db import models
from django.contrib.auth.models import User


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
    prazo_entrega = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo