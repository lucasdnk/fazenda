from flask import Flask, request, jsonify
from datetime import datetime
from typing import Dict, List
import uuid
import logging
from functools import wraps
from user_management import UserManager, UserRole
from database import get_db, User, Farm, Field, Crop, Activity
from sqlalchemy.orm import Session
from config import config

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = config.JWT_SECRET_KEY
user_manager = UserManager()

# Criar usuário admin inicial
try:
    admin = user_manager.create_user(
        username="admin",
        email="admin@example.com",
        password="admin123",
        role=UserRole.ADMIN
    )
    logger.info("Usuário admin criado com sucesso")
except ValueError as e:
    logger.info("Usuário admin já existe")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token é obrigatório'}), 401

        token = token.split(' ')[1] if len(token.split(' ')) > 1 else token
        user_data = user_manager.verify_token(token)
        
        if not user_data:
            return jsonify({'error': 'Token inválido'}), 401

        return f(user_data, *args, **kwargs)
    return decorated

# Rota de login
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        logger.debug(f"Tentativa de login para usuário: {data.get('username')}")
        token = user_manager.authenticate(data['username'], data['password'])
        if token:
            logger.info(f"Login bem sucedido para usuário: {data.get('username')}")
            return jsonify({'token': token})
        logger.warning(f"Login falhou para usuário: {data.get('username')}")
        return jsonify({'error': 'Credenciais inválidas'}), 401
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        return jsonify({'error': 'Erro no servidor'}), 500

# Simulando um banco de dados com dicionários
farms_db = {}
fields_db = {}
crops_db = {}
activities_db = {}

class Farm:
    def __init__(self, name: str, location: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.created_at = datetime.now()

class Field:
    def __init__(self, farm_id: str, name: str, area: float):
        self.id = str(uuid.uuid4())
        self.farm_id = farm_id
        self.name = name
        self.area = area
        self.created_at = datetime.now()

class Crop:
    def __init__(self, field_id: str, crop_type: str, planting_date: datetime):
        self.id = str(uuid.uuid4())
        self.field_id = field_id
        self.crop_type = crop_type
        self.planting_date = planting_date
        self.status = "active"
        self.created_at = datetime.now()

class Activity:
    def __init__(self, field_id: str, activity_type: str, description: str):
        self.id = str(uuid.uuid4())
        self.field_id = field_id
        self.activity_type = activity_type
        self.description = description
        self.status = "pending"
        self.created_at = datetime.now()

# Rotas protegidas
@app.route('/farms', methods=['POST'])
@token_required
def create_farm(current_user):
    try:
        data = request.json
        db = next(get_db())
        farm = Farm(name=data['name'], location=data['location'])
        db.add(farm)
        db.commit()
        return jsonify({
            'id': farm.id,
            'name': farm.name,
            'location': farm.location,
            'created_at': farm.created_at
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/farms', methods=['GET'])
@token_required
def list_farms(current_user):
    return jsonify(list(farms_db.values()))

@app.route('/farms/<farm_id>', methods=['GET'])
@token_required
def get_farm(current_user, farm_id):
    farm = farms_db.get(farm_id)
    if farm:
        return jsonify(farm)
    return jsonify({"error": "Fazenda não encontrada"}), 404

# Rotas para Talhões
@app.route('/fields', methods=['POST'])
@token_required
def create_field(current_user):
    data = request.json
    if data['farm_id'] not in farms_db:
        return jsonify({"error": "Fazenda não encontrada"}), 404
    
    field = Field(data['farm_id'], data['name'], data['area'])
    fields_db[field.id] = field.__dict__
    return jsonify(field.__dict__), 201

@app.route('/farms/<farm_id>/fields', methods=['GET'])
@token_required
def list_farm_fields(current_user, farm_id):
    if farm_id not in farms_db:
        return jsonify({"error": "Fazenda não encontrada"}), 404
    
    farm_fields = [field for field in fields_db.values() if field['farm_id'] == farm_id]
    return jsonify(farm_fields)

# Rotas para Culturas
@app.route('/crops', methods=['POST'])
def create_crop():
    data = request.json
    if data['field_id'] not in fields_db:
        return jsonify({"error": "Talhão não encontrado"}), 404
    
    planting_date = datetime.strptime(data['planting_date'], '%Y-%m-%d')
    crop = Crop(data['field_id'], data['crop_type'], planting_date)
    crops_db[crop.id] = crop.__dict__
    return jsonify(crop.__dict__), 201

@app.route('/fields/<field_id>/crops', methods=['GET'])
def list_field_crops(field_id):
    if field_id not in fields_db:
        return jsonify({"error": "Talhão não encontrado"}), 404
    
    field_crops = [crop for crop in crops_db.values() if crop['field_id'] == field_id]
    return jsonify(field_crops)

# Rotas para Atividades
@app.route('/activities', methods=['POST'])
def create_activity():
    data = request.json
    if data['field_id'] not in fields_db:
        return jsonify({"error": "Talhão não encontrado"}), 404
    
    activity = Activity(data['field_id'], data['activity_type'], data['description'])
    activities_db[activity.id] = activity.__dict__
    return jsonify(activity.__dict__), 201

@app.route('/fields/<field_id>/activities', methods=['GET'])
def list_field_activities(field_id):
    if field_id not in fields_db:
        return jsonify({"error": "Talhão não encontrado"}), 404
    
    field_activities = [activity for activity in activities_db.values() if activity['field_id'] == field_id]
    return jsonify(field_activities)

@app.route('/activities/<activity_id>', methods=['PUT'])
def update_activity_status(activity_id):
    if activity_id not in activities_db:
        return jsonify({"error": "Atividade não encontrada"}), 404
    
    data = request.json
    activities_db[activity_id]['status'] = data['status']
    return jsonify(activities_db[activity_id])

if __name__ == '__main__':
    logger.info("Iniciando o servidor Flask...")
    try:
        app.run(
            host=config.API_HOST,
            port=config.API_PORT,
            debug=config.API_DEBUG
        )
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {str(e)}")
