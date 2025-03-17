"""
Serviço de autenticação para comunicação com o backend
"""
import requests
from typing import Tuple, Optional, Dict, Any

class AuthService:
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url

    def login(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Realiza o login do usuário
        
        Returns:
            Tuple contendo (sucesso, dados_usuario, mensagem_erro)
        """
        try:
            response = requests.post(
                f'{self.base_url}/auth/login',
                json={'username': username, 'password': password}
            )

            if response.status_code == 200:
                return True, response.json(), None
            return False, None, "Usuário ou senha inválidos"
            
        except Exception as e:
            return False, None, f"Erro ao conectar ao servidor: {str(e)}" 