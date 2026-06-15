# Banco de Dados - DevDesk

## Relacionamentos

Workspace 1:N Usuários
Workspace 1:N Projetos
Projeto N:N Usuários
Projeto 1:N Tarefas
Tarefa 1:N Comentários

## Desenho simples

```text
WORKSPACE
  ├── USUARIOS
  └── PROJETOS
        ├── PROJETO_USUARIOS
        └── TAREFAS
              └── COMENTARIOS