"""
Configurações globais da aplicação
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurações da API
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

# Configurações da interface
APP_NAME = "Sistema de Gestão Agrícola"
APP_VERSION = "1.0.0"

# Configurações de janela
WINDOW_DEFAULT_WIDTH = 400
WINDOW_DEFAULT_HEIGHT = 200
WINDOW_DEFAULT_X = 100
WINDOW_DEFAULT_Y = 100

# UI Settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200 