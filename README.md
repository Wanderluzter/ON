# 🧠 Projeto - Emotional Tracker

## 🚀 Como executar localmente com Docker

### Clone o repositório:

```bash
git clone https://github.com/Wanderluzter/ON/tree/feature/ci-cd
```

### Entre na pasta do projeto:

```bash
cd ON
```

### Copie o arquivo de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

### Edite o arquivo `.env` conforme necessário
(ex: dados de conexão com o MongoDB, secret keys, etc).

### Construa e suba os containers:

```bash
docker-compose up --build
```

### Acesse a aplicação:

👉 [http://localhost:8000](http://localhost:8000)

### Documentação automática da API:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚙️ Pipeline CI/CD

### Ferramenta utilizada:

**GitHub Actions** — responsável pela automação de build, testes e deploy.

### Etapas do pipeline:

- **Build:** constrói a imagem Docker a partir do Dockerfile e valida dependências.  
- **Testes:** executa testes automatizados (ex: pytest) para garantir estabilidade.  
- **Deploy em Staging:**  
  - Ocorre automaticamente quando há push na branch `staging`.  
  - A imagem é enviada para o Docker Hub e implantada em um ambiente de testes (Azure Container App ou outra infraestrutura).  
- **Deploy em Produção:**
  - Apenas código validado e aprovado é liberado para o ambiente produtivo.  

### Funcionamento:

O **GitHub Actions** é acionado a cada push ou pull request.  
Ele executa o workflow configurado em `.github/workflows/ci-cd.yml`, garantindo que o código sempre esteja em um estado funcional e pronto para deploy.

---

## 🐳 Containerização

### Dockerfile (exemplo):

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Estratégias adotadas:

- **Imagem leve:** usa `python:3.10-slim` para otimizar tamanho e tempo de build.  
- **Isolamento completo:** a aplicação roda em container independente, garantindo reprodutibilidade.  
- **Variáveis de ambiente:** configuradas via `.env` e acessadas pelo container.  
- **Persistência de dados:** volumes Docker configurados no `docker-compose.yml` para não perder dados do MongoDB.  
- **Orquestração:** o `docker-compose.yml` gerencia múltiplos serviços (API + banco de dados).  

---

## 🧩 Tecnologias utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| **Linguagem** | Python 3.x |
| **Framework** | FastAPI |
| **Banco de Dados** | MongoDB |
| **Servidor ASGI** | Uvicorn |
| **Containerização** | Docker e Docker Compose |
| **Repositório de Imagens** | Docker Hub |
| **CI/CD** | GitHub Actions |
| **Infraestrutura de Deploy** | Azure Container Apps |
| **Testes Automatizados** | Pytest |
