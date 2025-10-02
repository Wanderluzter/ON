# 📌 Emotional Tracker API

API desenvolvida em **FastAPI + MongoDB** para monitoramento emocional e psicossocial dos usuários.  
Permite registro de diários, avaliações emocionais, centros de apoio e controle de acessos via JWT.  

---

## 🚀 Tecnologias Utilizadas
- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend
- [MongoDB Atlas](https://www.mongodb.com/atlas) - Banco de dados NoSQL
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/) - Autenticação JWT
- [Pydantic](https://docs.pydantic.dev/) - Validação de dados
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI  

---

## ⚙️ Arquitetura

```        
        [Mobile App / Frontend]
                  |
                  v
         ┌───────────────────┐
         │   FastAPI (API)   │
         │                   │
         │  • Autenticação   │
         │  • Endpoints      │
         │  • Validação JWT  │
         │  • Logs/Auditoria │
         └─────────┬─────────┘
                   │
                   v
        ┌───────────────────────┐
        │    MongoDB Atlas      │
        │                       │
        │  • users              │
        │  • assessments        │
        │  • diaries            │
        │  • emotions           │
        │  • supportcenters     │
        │  • logs               │
        └───────────────────────┘

```

---

## 📂 Estrutura do Projeto

```
.
├── main.py              # Ponto de entrada da aplicação
├── auth/                # Módulos de autenticação
├── routes/              # Rotas (diários, emoções, etc)
├── models/              # Schemas e modelos
├── utils/               # Funções auxiliares (ex: logger)
├── requirements.txt     # Dependências
└── README.md            # Documentação
```

---

## 🔑 Autenticação

A API utiliza **JWT (Bearer Token)**.  
1. O usuário se registra em `/auth/register`.  
2. Faz login em `/auth/login`.  
3. Recebe um `access_token`.  
4. Usa esse token no header `Authorization` para acessar as rotas protegidas:  

```
Authorization: Bearer <seu_token>
```

---

## 📌 Endpoints Principais

### 👤 Usuários
- `POST /auth/register` → Cadastro  
- `POST /auth/login` → Login (gera token)  
- `GET /me` → Retorna dados do usuário autenticado  

### 📔 Diários
- `POST /diaries/` → Criar diário  
- `GET /diaries/` → Listar diários  
- `PUT /diaries/{id}` → Editar diário  
- `DELETE /diaries/{id}` → Remover diário  

### 📝 Avaliações
- `POST /assessments/` → Criar avaliação  
- `GET /assessments/` → Listar avaliações  

### 😊 Emoções
- `POST /emotions/` → Registrar emoção  
- `GET /emotions/` → Listar emoções  

### 🏥 Centros de Apoio
- `GET /supportcenters/` → Listar  

### 📊 Logs (admin)
- `GET /logs/` → Ver logs de atividades  

---

## 🗄️ Modelo de Dados (MongoDB)

Exemplo de documento **assessment**:

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "humor": "triste",
  "intensidade": 7,
  "observacao": "muito estresse",
  "created_at": "2025-10-02T15:30:00Z"
}
```

---

## ▶️ Como Rodar Localmente

### Pré-requisitos
- Python 3.10+
- MongoDB Atlas (ou local)
- Git instalado  

### Passos

```bash
# Clone o repositório
git clone git@github.com:Wanderluzter/ON.git

# Acesse a pasta
cd ON

# Crie um ambiente virtual
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
uvicorn main:app --reload
```

A API estará disponível em:  
👉 `http://127.0.0.1:8000/docs`

---

## 📜 Licença
Este projeto está sob a licença MIT.  
