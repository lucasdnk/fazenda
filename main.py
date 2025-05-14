import sys
import os
import logging
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from database import init_db
from ui import MainWindow

# Configurar logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fazenda.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Verifica se a conexão com o banco de dados pode ser estabelecida."""
    try:
        init_db()
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        return True
    except Exception as e:
        db_name = os.getenv('DB_NAME', 'fazenda')
        error_msg = f"Não foi possível conectar ao banco de dados. Verifique as configurações.\n\n"
        error_msg += f"Detalhes do erro: {str(e)}\n\n"
        error_msg += "Verifique se:\n"
        error_msg += "1. PostgreSQL está instalado e em execução\n"
        error_msg += "2. As configurações no arquivo .env estão corretas\n"
        error_msg += f"3. O banco de dados '{db_name}' existe\n"
        error_msg += "\nConsulte README.md para instruções de configuração."
        
        logger.error(f"Erro de conexão com o banco de dados: {str(e)}")
        
        QMessageBox.critical(
            None,
            "Erro de Conexão",
            error_msg
        )
        return False

def create_database_if_not_exists():
    """Tenta criar o banco de dados se não existir."""
    try:
        # Variáveis do banco de dados
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "postgres")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "fazenda")
        
        # Criar conexão para o PostgreSQL sem especificar um banco de dados
        postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
        engine = create_engine(postgres_url)
        
        # Verificar se o banco de dados existe e criar se não existir
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        if not database_exists(database_url):
            logger.info(f"Banco de dados '{db_name}' não encontrado. Tentando criar...")
            create_database(database_url)
            logger.info(f"Banco de dados '{db_name}' criado com sucesso.")
            return True
        return True
    except Exception as e:
        logger.error(f"Erro ao verificar/criar banco de dados: {str(e)}")
        return False

def main():
    """Função principal que inicia o aplicativo."""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    logger.info("Iniciando aplicação Sistema de Gerenciamento de Fazenda")
    
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo consistente em todas as plataformas
    app.setApplicationName("Sistema de Gerenciamento de Fazenda")
    
    # Criar pasta de recursos se não existir
    os.makedirs('ui/resources', exist_ok=True)
    
    # Mostrar splash screen se o arquivo existir
    splash = None
    splash_path = "ui/resources/splash.png"
    if os.path.exists(splash_path):
        splash_pixmap = QPixmap(splash_path)
        if not splash_pixmap.isNull():
            splash = QSplashScreen(splash_pixmap, Qt.WindowType.WindowStaysOnTopHint)
            splash.show()
            app.processEvents()
    
    # Tentar criar o banco se não existir
    create_database_if_not_exists()
    
    # Verificar conexão com o banco de dados
    db_connected = check_database_connection()
    
    # Esconder splash screen se estiver ativo
    if splash:
        splash.close()
    
    if not db_connected:
        return 1
    
    # Criar e mostrar a janela principal
    main_window = MainWindow()
    main_window.show()
    
    logger.info("Aplicação iniciada com sucesso")
    
    # Executar o loop principal
    return app.exec()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.critical(f"Erro fatal na aplicação: {str(e)}", exc_info=True)
        QMessageBox.critical(
            None,
            "Erro Fatal",
            f"Ocorreu um erro fatal na aplicação:\n\n{str(e)}\n\nConsulte o arquivo de log para mais detalhes."
        )
        sys.exit(1) 