# API de Gerenciamento de Usuários com FastAPI e SQLite

Esta é uma API RESTful simples para gerenciamento de usuários, desenvolvida em Python utilizando o framework FastAPI e o banco de dados SQLite. Ela implementa as operações CRUD (Create, Read, Update, Delete) para a entidade `Usuário`.

## Funcionalidades

- **Criação de Usuários**: Adiciona novos usuários ao banco de dados.
- **Leitura de Usuários**: Lista todos os usuários ou busca um usuário específico por ID.
- **Atualização de Usuários**: Modifica os dados de um usuário existente.
- **Exclusão de Usuários**: Remove um usuário do banco de dados.

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework web moderno e rápido para construir APIs com Python 3.7+ baseado em tipagem padrão do Python.
- **Pydantic**: Biblioteca para validação de dados e gerenciamento de configurações usando tipagem do Python.
- **SQLite**: Banco de dados leve e serverless, ideal para aplicações pequenas e médias.
- **Uvicorn**: Servidor ASGI de alta performance para aplicações Python.

## Estrutura do Projeto

```
. (raiz do projeto)
├── main.py         # Código principal da API FastAPI
├── banco_usuarios.db # Arquivo do banco de dados SQLite (gerado automaticamente)
└── README.md       # Este arquivo
```

## Como Rodar a API

Siga os passos abaixo para configurar e executar a API em seu ambiente local.

### Pré-requisitos

Certifique-se de ter o Python 3.7+ instalado em sua máquina.

### 1. Clonar o Repositório (se aplicável)

Se você recebeu este projeto via um repositório Git, clone-o:

```bash
git clone <URL_DO_REPOSITORIO>
cd <nome_do_repositorio>
```

### 2. Instalar Dependências

Navegue até o diretório raiz do projeto e instale as dependências necessárias usando `pip`:

```bash
pip install fastapi uvicorn pydantic email-validator
```

### 3. Iniciar o Servidor da API

Execute o arquivo `main.py` usando `uvicorn`:

```bash
uvicorn main:app --reload
```

- `--reload`: Reinicia o servidor automaticamente a cada alteração no código (útil para desenvolvimento).

A API estará disponível em `http://127.0.0.1:8000`.

## Documentação Interativa (Swagger UI / ReDoc)

FastAPI gera automaticamente documentação interativa para sua API. Você pode acessá-la nos seguintes URLs:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

Use a documentação do Swagger UI para testar os endpoints diretamente no navegador.

## Endpoints da API

A seguir, uma descrição dos endpoints disponíveis:

### `POST /usuarios/`

- **Descrição**: Cria um novo usuário.
- **Corpo da Requisição (JSON)**:
  ```json
  {
    "nome": "Nome do Usuário",
    "email": "email@example.com"
  }
  ```
- **Resposta (201 Created)**:
  ```json
  {
    "id": 1,
    "nome": "Nome do Usuário",
    "email": "email@example.com"
  }
  ```

### `GET /usuarios/`

- **Descrição**: Retorna uma lista de todos os usuários cadastrados.
- **Resposta (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "nome": "Nome do Usuário",
      "email": "email@example.com"
    }
  ]
  ```

### `GET /usuarios/{user_id}`

- **Descrição**: Retorna os detalhes de um usuário específico pelo seu ID.
- **Parâmetros de Path**:
  - `user_id` (inteiro): O ID do usuário.
- **Resposta (200 OK)**:
  ```json
  {
    "id": 1,
    "nome": "Nome do Usuário",
    "email": "email@example.com"
  }
  ```
- **Resposta (404 Not Found)**: Se o usuário não for encontrado.

### `PUT /usuarios/{user_id}`

- **Descrição**: Atualiza os dados de um usuário existente pelo seu ID.
- **Parâmetros de Path**:
  - `user_id` (inteiro): O ID do usuário a ser atualizado.
- **Corpo da Requisição (JSON)**:
  ```json
  {
    "nome": "Novo Nome",
    "email": "novo.email@example.com"
  }
  ```
- **Resposta (200 OK)**:
  ```json
  {
    "id": 1,
    "nome": "Novo Nome",
    "email": "novo.email@example.com"
  }
  ```
- **Resposta (404 Not Found)**: Se o usuário não for encontrado.

### `DELETE /usuarios/{user_id}`

- **Descrição**: Remove um usuário do banco de dados pelo seu ID.
- **Parâmetros de Path**:
  - `user_id` (inteiro): O ID do usuário a ser excluído.
- **Resposta (204 No Content)**: Se o usuário for excluído com sucesso.
- **Resposta (404 Not Found)**: Se o usuário não for encontrado.

## Testes

O arquivo `test_api.py` contém testes automatizados para verificar o funcionamento de todos os endpoints da API. Para executá-los:

```bash
python3 test_api.py
```

Este script iniciará a API, executará os testes e encerrará o servidor automaticamente.
