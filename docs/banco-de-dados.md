# Banco de Dados - DevDesk

## Relacionamentos

Empresa 1:N Usuários
Empresa 1:N Projetos
Projeto N:N Usuários
Projeto 1:N Tarefas
Tarefa 1:N Comentários

## Desenho simples

EMPRESA
  ├── USUARIOS
  └── PROJETOS
        ├── PROJETO_USUARIOS
        └── TAREFAS
              └── COMENTARIOS