"""
Backend Flask para o Sistema de Gestão Agrícola
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições cross-origin

# Chave secreta para JWT - Em produção, deve ser uma chave segura e ambiente
SECRET_KEY = "sua_chave_secreta"

# Simulação de banco de dados de usuários com roles
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "permissions": [
            "dashboard",
            "manage_farms",
            "manage_crops",
            "reports",
            "settings",
            "users"
        ]
    },
    "user": {
        "password": "user123",
        "role": "user",
        "permissions": [
            "dashboard",
            "view_farms",
            "view_crops",
            "view_reports"
        ]
    }
}

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and USERS[username]["password"] == password:
        user_data = USERS[username]
        # Gera o token JWT com informações do usuário
        token = jwt.encode(
            {
                'user': username,
                'role': user_data["role"],
                'permissions': user_data["permissions"],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return jsonify({
            'token': token,
            'role': user_data["role"],
            'permissions': user_data["permissions"]
        })
    
    return jsonify({'message': 'Usuário ou senha inválidos'}), 401

if __name__ == '__main__':
    print("Servidor rodando em http://localhost:5000")
    print("Usuários disponíveis para teste:")
    print("  - Username: admin, Senha: admin123 (Administrador)")
    print("  - Username: user, Senha: user123 (Usuário comum)")
    app.run(debug=True) 