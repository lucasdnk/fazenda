# Sistema de Gestão Agrícola

Sistema desktop para gestão agrícola desenvolvido com PyQt5.

## Estrutura do Projeto

```
fazenda/
├── src/                    # Código fonte
│   ├── ui/                 # Interface do usuário
│   ├── services/          # Serviços e lógica de negócio
│   ├── config/            # Configurações
│   └── backend/           # Servidor backend
├── requirements.txt       # Dependências
└── main.py               # Ponto de entrada
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando o Projeto

1. Primeiro, inicie o servidor backend:
   ```bash
   # Em um terminal
   python src/backend/app.py
   ```

2. Em outro terminal, inicie a aplicação desktop:
   ```bash
   python main.py
   ```

## Credenciais para Teste

O backend inclui dois usuários para teste:
- Username: admin, Senha: admin123
- Username: user, Senha: user123
 
