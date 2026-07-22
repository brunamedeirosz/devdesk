from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets

from .models import Comentario, Nota, Projeto, Tarefa, Workspace
from .serializers import (
    ComentarioSerializer,
    NotaSerializer,
    ProjetoSerializer,
    RegistroUsuarioSerializer,
    TarefaSerializer,
    UserSerializer,
    WorkspaceSerializer,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistroUsuarioView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [permissions.AllowAny]


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.select_related('workspace').all()
    serializer_class = ProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.select_related('projeto', 'responsavel').prefetch_related('comentarios').all()
    serializer_class = TarefaSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.select_related('tarefa', 'autor').all()
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class NotaViewSet(viewsets.ModelViewSet):
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Nota.objects.filter(usuario=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
