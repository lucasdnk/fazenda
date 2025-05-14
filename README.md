# Sistema de Gerenciamento de Fazenda

Sistema desenvolvido em Python para gerenciamento completo de uma fazenda, incluindo controle de maquinário, funcionários, finanças e produção.

## Funcionalidades

- **Maquinário**: Cadastro e gerenciamento de máquinas e equipamentos, com controle de manutenções.
- **Funcionários**: Cadastro e gerenciamento de funcionários, incluindo informações pessoais e salários.
- **Financeiro**: Controle de despesas e Entradas, com categorização e relatórios.
- **Produção**: Acompanhamento de safras e produção agrícola, com cálculo de custos e lucros.

## Requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Bibliotecas Python conforme listadas em `requirements.txt`

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/fazenda.git
   cd fazenda
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Instale e configure o PostgreSQL:
   - [Download PostgreSQL](https://www.postgresql.org/download/)
   - Crie um banco de dados chamado "fazenda" (o sistema tentará criar automaticamente se não existir)
   - Anote o usuário, senha, host e porta

5. Configure o ambiente:
   - Copie o arquivo `env.example` para `.env`:
     ```
     cp env.example .env    # Linux/macOS
     copy env.example .env  # Windows
     ```
   - Edite o arquivo `.env` com as configurações do seu banco de dados

6. Execute o aplicativo:
   ```
   python main.py
   ```

## Estrutura do Projeto

- `database/`: Módulos relacionados ao banco de dados
  - `models.py`: Definição dos modelos de dados
  - `db.py`: Configuração de conexão com o banco de dados
- `ui/`: Interfaces gráficas
  - `main_window.py`: Janela principal da aplicação
  - `tabs/`: Abas da interface gráfica
- `main.py`: Ponto de entrada da aplicação

## Uso

Ao iniciar o aplicativo, você verá uma interface com quatro abas principais:

1. **Maquinário**: Gerencie todos os equipamentos da fazenda
2. **Funcionários**: Cadastre e gerencie a equipe
3. **Financeiro**: Controle despesas e Entradas
4. **Produção**: Registre e acompanhe a produção agrícola

## Solução de Problemas

### Erro de conexão com o banco de dados

Se você receber erros de conexão com o banco de dados:

1. Verifique se o PostgreSQL está instalado e em execução
2. Confira as configurações no arquivo `.env`
3. Certifique-se de que o banco de dados "fazenda" existe (ou altere o nome no arquivo `.env`)
4. Verifique se o usuário tem permissões adequadas no banco de dados

### Erro ao instalar PyQt5

Em alguns sistemas, pode haver problemas ao instalar o PyQt5:

1. Certifique-se de ter instalado o Qt e suas dependências:
   - Windows: Instale o [Qt](https://www.qt.io/download) ou use `pip install PyQt5-Qt5`
   - Linux: Instale pacotes como `qt5-base-dev` (Ubuntu/Debian) ou equivalentes
   - macOS: Use `brew install qt@5`

2. Em caso de erro com `qmake`, adicione o diretório do Qt ao PATH ou instale apenas a versão básica:
   ```
   pip install PyQt5==5.15.9
   ```

3. Logs detalhados da aplicação são salvos em `fazenda.log` e podem ajudar a identificar problemas.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para reportar problemas ou enviar pull requests. 