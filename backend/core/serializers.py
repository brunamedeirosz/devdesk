from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comentario, Nota, Projeto, Tarefa, Workspace

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class ProjetoSerializer(serializers.ModelSerializer):
    workspace_nome = serializers.ReadOnlyField(source='workspace.nome')

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
    projeto_nome = serializers.ReadOnlyField(source='projeto.nome')
    responsavel_nome = serializers.ReadOnlyField(source='responsavel.username')

    class Meta:
        model = Tarefa
        fields = '__all__'


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'
        read_only_fields = ['usuario']
