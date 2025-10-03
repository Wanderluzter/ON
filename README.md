# 🌱 Emotional Tracker API

API RESTful para rastrear e organizar informações de bem-estar emocional, diários, emoções, centros de apoio e avaliações psicossociais.

---

## 🚀 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [MongoDB Atlas](https://www.mongodb.com/atlas) — banco NoSQL
- [PyMongo](https://pymongo.readthedocs.io/) — driver MongoDB
- [Passlib (bcrypt)](https://passlib.readthedocs.io/) — hash de senhas
- [Python-Jose](https://python-jose.readthedocs.io/) — autenticação JWT
- [Decouple](https://pypi.org/project/python-decouple/) — variáveis de ambiente

---

## ⚙️ Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/emotional-tracker-api.git
cd emotional-tracker-api
pip install -r requirements.txt
```

---

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com os seguintes valores:

```env
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
SECRET_KEY=chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## ▶️ Executando a API

```bash
uvicorn main:app --reload
```

A API ficará disponível em:
```
http://127.0.0.1:8000
```

Documentação interativa:  
- Swagger UI → `http://127.0.0.1:8000/docs`  
- ReDoc → `http://127.0.0.1:8000/redoc`  

---

## 📌 Endpoints da API

Base URL:
```
/api/v1
```

### 🔑 Autenticação
- **POST** `/auth/register` → Registrar usuário
- **POST** `/auth/token` → Login com `x-www-form-urlencoded`
- **GET** `/me` → Perfil do usuário autenticado

### 👤 Usuários
- **GET** `/users` → Listar todos os usuários
- **GET** `/users/{id}` → Buscar usuário por ID
- **PUT** `/users/{id}` → Atualizar usuário
- **DELETE** `/users/{id}` → Remover usuário

### 📔 Diários
- **POST** `/diaries` → Criar diário
- **GET** `/diaries/user/{user_id}` → Listar diários do usuário

### 😊 Emoções
- **POST** `/emotions` → Criar emoção
- **GET** `/emotions/user/{user_id}` → Listar emoções

### 🏥 Centros de Apoio
- **POST** `/supportcenters` → Criar centro de apoio

### 📝 Avaliações
- **POST** `/assessments` → Criar avaliação
- **GET** `/assessments/user/{user_id}` → Listar avaliações

---

## 🗂️ Modelo de Dados (MongoDB)

### `users`
```json
{
  "_id": "ObjectId",
  "nome": "string",
  "email": "string",
  "idade": "int",
  "password_hash": "string",
  "created_at": "datetime"
}
```

### `diaries`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "data": "YYYY-MM-DD",
  "texto": "string"
}
```

### `emotions`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "tipo": "string",
  "intensidade": "int (1-10)"
}
```

### `supportcenters`
```json
{
  "_id": "ObjectId",
  "nome": "string",
  "telefone": "string",
  "endereco": "string"
}
```

### `assessments`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "avaliacao": "string",
  "data": "YYYY-MM-DD"
}
```

### `logs`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "acao": "string",
  "detalhes": "string",
  "timestamp": "datetime"
}
```

---

## 🔒 Autenticação e Autorização

- **JWT** assinado com `SECRET_KEY` e `HS256`
- Expiração configurável (default: 60 min)
- Usuários só acessam seus próprios dados (`diaries`, `emotions`, `assessments`)
- Todas as ações são registradas em **logs de auditoria**

---

## 🧪 Exemplos de Uso (cURL)

### Registrar usuário
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register   -H "Content-Type: application/json"   -d '{"nome":"Leo","email":"leo@email.com","idade":25,"senha":"senha123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token   -H "Content-Type: application/x-www-form-urlencoded"   -d "username=leo@email.com&password=senha123"
```

### Obter perfil
```bash
curl -X GET http://127.0.0.1:8000/api/v1/me   -H "Authorization: Bearer <TOKEN>"
```

---