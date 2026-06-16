from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Workspace, Projeto, Tarefa, Comentario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    autor_nome = serializers.ReadOnlyField(source='autor.username')

    class Meta:
        model = Comentario
        fields = '__all__'
        read_only_fields = ['autor']

class TarefaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Tarefa
        fields = '__all__'
