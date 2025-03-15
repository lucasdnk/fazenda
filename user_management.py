from enum import Enum
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import List, Dict
from config import config

# Definição dos níveis de permissão
class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    AGRONOMIST = "agronomist"
    OPERATOR = "operator"
    VIEWER = "viewer"

# Definição das permissões por função
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        "manage_users",
        "manage_farms",
        "manage_fields",
        "manage_crops",
        "manage_activities",
        "view_reports",
        "manage_roles"
    ],
    UserRole.MANAGER: [
        "manage_farms",
        "manage_fields",
        "manage_crops",
        "manage_activities",
        "view_reports"
    ],
    UserRole.AGRONOMIST: [
        "manage_crops",
        "manage_activities",
        "view_reports"
    ],
    UserRole.OPERATOR: [
        "view_activities",
        "update_activities"
    ],
    UserRole.VIEWER: [
        "view_farms",
        "view_fields",
        "view_crops",
        "view_activities"
    ]
}

class User:
    def __init__(self, username: str, email: str, role: UserRole):
        self.id = None
        self.username = username
        self.email = email
        self.password_hash = None
        self.role = role
        self.created_at = datetime.now()
        self.last_login = None
        self.active = True

    def set_password(self, password: str):
        # Usando SHA-256 com salt
        salt = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        self.password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        self.salt = salt

    def check_password(self, password: str) -> bool:
        # Verifica a senha usando o salt armazenado
        hashed = hashlib.sha256((password + self.salt).encode()).hexdigest()
        return hashed == self.password_hash

    def has_permission(self, permission: str) -> bool:
        return permission in ROLE_PERMISSIONS[self.role]

class UserManager:
    def __init__(self):
        self.users = {}
        self.SECRET_KEY = config.JWT_SECRET_KEY

    def create_user(self, username: str, email: str, password: str, role: UserRole) -> User:
        if username in self.users:
            raise ValueError("Usuário já existe")

        user = User(username, email, role)
        user.set_password(password)
        user.id = str(len(self.users) + 1)
        self.users[username] = user
        return user

    def authenticate(self, username: str, password: str) -> str:
        user = self.users.get(username)
        if user and user.check_password(password):
            user.last_login = datetime.now()
            return self.generate_token(user)
        return None

    def generate_token(self, user: User) -> str:
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': datetime.utcnow() + timedelta(days=config.JWT_EXPIRATION_DAYS)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    def verify_token(self, token: str) -> Dict:
        try:
            return jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
        except:
            return None 