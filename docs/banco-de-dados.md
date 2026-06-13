# Banco de Dados - DevDesk

## Visão Geral

O DevDesk é composto pelas seguintes entidades:

* Empresa
* Usuário
* Projeto
* Projeto_Usuarios
* Tarefa
* Comentário

---

## Tabela: empresas

Representa as empresas cadastradas na plataforma.

Campos:

* id
* nome
* cnpj
* criado_em

---

## Tabela: usuarios

Representa os usuários da plataforma.

Campos:

* id
* empresa_id
* nome
* email
* senha
* perfil
* criado_em

Perfis:

* administrador
* gestor
* colaborador

---

## Tabela: projetos

Representa os projetos da empresa.

Campos:

* id
* empresa_id
* nome
* descricao
* prazo_entrega
* status
* criado_em

Status:

* planejado
* em_andamento
* concluido
* cancelado

---

## Tabela: projeto_usuarios

Relaciona usuários aos projetos.

Campos:

* id
* projeto_id
* usuario_id

---

## Tabela: tarefas

Representa as tarefas de um projeto.

Campos:

* id
* projeto_id
* responsavel_id
* titulo
* descricao
* prioridade
* status
* prazo_entrega
* criado_em

Prioridades:

* baixa
* media
* alta

Status:

* pendente
* em_andamento
* concluida
* cancelada

---

## Tabela: comentarios

Comentários realizados dentro das tarefas.

Campos:

* id
* tarefa_id
* usuario_id
* comentario
* criado_em
