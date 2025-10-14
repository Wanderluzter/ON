🧠 Projeto - Emotional Tracker
🚀 Como executar localmente com Docker

Clone o repositório:

git clone https://github.com/seu-usuario/emotional-tracker.git


Entre na pasta do projeto:

cd emotional-tracker


Copie o arquivo de exemplo de variáveis de ambiente:

cp .env.example .env


Edite o arquivo .env conforme necessário (ex: dados de conexão com o MongoDB, secret keys, etc).

Construa e suba os containers:

docker-compose up --build


Acesse a aplicação:

http://localhost:8000


A documentação automática da API estará disponível em:

http://localhost:8000/docs

⚙️ Pipeline CI/CD

Ferramenta utilizada:

GitHub Actions — responsável pela automação de build, testes e deploy.

Pode ser facilmente adaptado para Azure DevOps, Jenkins ou CircleCI.

Etapas do pipeline:

Build: constrói a imagem Docker a partir do Dockerfile e valida dependências.

Testes: executa testes automatizados (ex: pytest) para garantir estabilidade.

Deploy em Staging:

Ocorre automaticamente quando há push na branch staging.

A imagem é enviada para o Docker Hub e implantada em um ambiente de testes (Azure Container App ou outra infraestrutura).

Deploy em Produção:

Ocorre com push na branch main.

Apenas código validado e aprovado é liberado para o ambiente produtivo.

Funcionamento:
O GitHub Actions é acionado a cada push ou pull request. Ele executa o workflow configurado em .github/workflows/ci-cd.yml, garantindo que o código sempre esteja em um estado funcional e pronto para deploy.

🐳 Containerização

Dockerfile (exemplo):

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


Estratégias adotadas:

Imagem leve: usa python:3.10-slim para otimizar tamanho e tempo de build.

Isolamento completo: a aplicação roda em container independente, garantindo reprodutibilidade.

Variáveis de ambiente: configuradas via .env e acessadas pelo container.

Persistência de dados: volumes Docker configurados no docker-compose.yml para não perder dados do MongoDB.

Orquestração: o docker-compose.yml gerencia múltiplos serviços (API + banco de dados).

🧾 Prints do funcionamento

Inclua aqui evidências do projeto em execução:

✅ Print do pipeline rodando no GitHub Actions (build → test → deploy)

🌐 Print da aplicação acessível em staging (ex: https://staging.emotionaltracker.azurecontainerapps.io)

🚀 Print da aplicação em produção

⚙️ Print do Docker em execução local (docker ps, http://localhost:8000/docs)

(Você pode usar links de imagens, GIFs ou capturas locais do sistema rodando.)

🧩 Tecnologias utilizadas

Linguagem: Python 3.x

Framework: FastAPI

Banco de Dados: MongoDB

Servidor ASGI: Uvicorn

Containerização: Docker e Docker Compose

Repositório de imagens: Docker Hub

CI/CD: GitHub Actions

Infraestrutura de deploy: Azure Container Apps

Testes automatizados: Pytest