
# Projeto - Emotional Tracker

## Como executar localmente com Docker

1. Clone o repositório do projeto:  
   ```bash
   git clone https://github.com/seu-usuario/emotional-tracker.git
   ```  

2. Entre na pasta do projeto:  
   ```bash
   cd emotional-tracker
   ```  

3. Copie o arquivo de exemplo de variáveis de ambiente:  
   ```bash
   cp .env.example .env
   ```  
   Ajuste as variáveis conforme necessário.

4. Suba os containers usando Docker Compose:  
   ```bash
   docker-compose up --build
   ```  

5. A aplicação estará disponível em:  
   ```
   http://localhost:8000
   ```

---

## Pipeline CI/CD

- **Ferramenta utilizada:** GitHub Actions (pode ser adaptado para Jenkins, Azure DevOps ou CircleCI)  
- **Etapas do pipeline:**  
  1. Build automático da aplicação  
  2. Execução de testes automatizados existentes (pytest ou outro framework)  
  3. Deploy automático em **staging** (branch `staging`)  
  4. Deploy automático em **produção** (branch `main`)  

- **Funcionamento:**  
  - Ao dar push em `staging`, a aplicação é construída, testada e implantada automaticamente em um ambiente de testes.  
  - Ao dar push em `main`, a aplicação é implantada em produção, garantindo que apenas código validado seja liberado.  

---

## Containerização

- **Dockerfile:** define a imagem base da aplicação, instala dependências, copia o código e expõe a porta da API.  
- **docker-compose.yml:** orquestra múltiplos serviços (ex: aplicação + banco de dados), configura volumes para persistência, variáveis de ambiente e rede interna entre os containers.  
- **Estratégias adotadas:**  
  - Persistência dos dados do banco usando volumes Docker  
  - Variáveis de ambiente externas via `.env`  
  - Separação de serviços para facilitar manutenção e escalabilidade  

---

## Prints do funcionamento

Inclua aqui evidências visuais do projeto funcionando:  
- Print do pipeline rodando (build, testes e deploy)  
- Print do ambiente **staging**  
- Print do ambiente **produção**  

*(Você pode usar links ou imagens locais)*

---

## Tecnologias utilizadas

- Python 3.x  
- FastAPI  
- MongoDB  
- Docker / Docker Compose  
- GitHub Actions (ou outra ferramenta de CI/CD)  
- Pytest (ou outro framework de testes)  
