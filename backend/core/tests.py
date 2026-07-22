from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comentario, Nota, Projeto, Tarefa, Workspace


class DevDeskApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bruna',
            email='bruna@example.com',
            password='devdesk123',
        )
        self.workspace = Workspace.objects.create(
            nome='Produto',
            tipo='Desenvolvimento',
        )
        self.projeto = Projeto.objects.create(
            workspace=self.workspace,
            nome='Portal DevDesk',
            descricao='Organizar entregas da equipe',
            status='Em Andamento',
            prazo_entrega=timezone.now() + timedelta(days=7),
        )

    def test_token_endpoint_returns_access_token(self):
        response = self.client.post('/api/token/', {
            'username': 'bruna',
            'password': 'devdesk123',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_registration_endpoint_creates_user(self):
        response = self.client.post('/api/registro/', {
            'username': 'ana',
            'email': 'ana@example.com',
            'password': 'devdesk123',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='ana').exists())
        self.assertNotIn('password', response.data)

    def test_users_endpoint_lists_basic_user_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/usuarios/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], 'bruna')

    def test_create_task_with_responsavel_returns_related_names(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/tarefas/', {
            'projeto': self.projeto.id,
            'responsavel': self.user.id,
            'titulo': 'Fechar Kanban',
            'descricao': 'Permitir troca de status',
            'prioridade': 'Alta',
            'status': 'A Fazer',
            'prazo_entrega': (timezone.now() + timedelta(days=2)).isoformat(),
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['projeto_nome'], 'Portal DevDesk')
        self.assertEqual(response.data['responsavel_nome'], 'bruna')

    def test_create_task_without_due_date(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/tarefas/', {
            'projeto': self.projeto.id,
            'responsavel': self.user.id,
            'titulo': 'Tarefa sem prazo',
            'descricao': 'Nem toda demanda precisa de data final.',
            'prioridade': 'Media',
            'status': 'A Fazer',
            'prazo_entrega': None,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['prazo_entrega'])

    def test_anonymous_user_cannot_create_task(self):
        response = self.client.post('/api/tarefas/', {
            'projeto': self.projeto.id,
            'responsavel': self.user.id,
            'titulo': 'Tarefa bloqueada',
            'descricao': 'Sem login nao pode criar.',
            'prioridade': 'Alta',
            'status': 'A Fazer',
            'prazo_entrega': (timezone.now() + timedelta(days=2)).isoformat(),
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_list_users(self):
        response = self.client.get('/api/usuarios/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_comment_task(self):
        tarefa = Tarefa.objects.create(
            projeto=self.projeto,
            responsavel=self.user,
            titulo='Testar comentarios',
            descricao='Adicionar feedback em tarefas',
            prioridade='Media',
            status='Em Andamento',
            prazo_entrega=timezone.now() + timedelta(days=1),
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/comentarios/', {
            'tarefa': tarefa.id,
            'texto': 'Comentario criado pela API.',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(response.data['autor_nome'], 'bruna')

    def test_authenticated_user_can_create_note(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/notas/', {
            'titulo': 'Checklist rapido',
            'itens': [{'id': '1', 'texto': 'Revisar tarefa'}],
            'itens_concluidos': [],
            'pos_x': 120,
            'pos_y': 180,
            'fixada': True,
            'visivel': True,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nota.objects.count(), 1)
        self.assertEqual(response.data['titulo'], 'Checklist rapido')

    def test_user_only_lists_own_notes(self):
        other_user = User.objects.create_user(username='ana', password='devdesk123')
        Nota.objects.create(usuario=self.user, titulo='Minha nota')
        Nota.objects.create(usuario=other_user, titulo='Nota de outra pessoa')
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/notas/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], 'Minha nota')

    def test_anonymous_user_cannot_access_notes(self):
        response = self.client.get('/api/notas/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
