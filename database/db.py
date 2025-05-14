import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from .models import Base

# Configurar logging
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente (apenas se não foi carregado antes)
if "DB_USER" not in os.environ:
    load_dotenv()

# Configurações do banco de dados
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fazenda")

# String de conexão
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar engine com opções de pool para melhor gerenciamento de conexões
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica se a conexão é válida antes de usar
    pool_recycle=3600,   # Recicla conexões após 1 hora
    echo=False           # Se True, habilita log SQL para debugging
)

# Criar sessão
Session = sessionmaker(bind=engine)

def init_db():
    """Inicializa o banco de dados, criando as tabelas se não existirem."""
    try:
        Base.metadata.create_all(engine)
        logger.info("Banco de dados inicializado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        raise
    
def get_session():
    """Retorna uma nova sessão do banco de dados."""
    try:
        session = Session()
        return session
    except Exception as e:
        logger.error(f"Erro ao criar sessão do banco de dados: {str(e)}")
        raise 