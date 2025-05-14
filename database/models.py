from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

class Maquinario(Base):
    __tablename__ = 'maquinario'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    modelo = Column(String(100))
    ano = Column(Integer)
    valor_aquisicao = Column(Numeric(10, 2))
    data_aquisicao = Column(Date)
    status = Column(String(50))  # Ativo, Em manutenção, Inativo
    observacoes = Column(Text)
    
    manutencoes = relationship("Manutencao", back_populates="maquinario")
    
    def __repr__(self):
        return f"<Maquinario(nome='{self.nome}', modelo='{self.modelo}')>"

class Manutencao(Base):
    __tablename__ = 'manutencao'
    
    id = Column(Integer, primary_key=True)
    maquinario_id = Column(Integer, ForeignKey('maquinario.id'))
    data = Column(Date, default=datetime.datetime.now)
    descricao = Column(Text, nullable=False)
    custo = Column(Numeric(10, 2))
    responsavel = Column(String(100))
    
    maquinario = relationship("Maquinario", back_populates="manutencoes")
    
    def __repr__(self):
        return f"<Manutencao(maquinario_id='{self.maquinario_id}', data='{self.data}')>"

class Funcionario(Base):
    __tablename__ = 'funcionario'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True)
    cargo = Column(String(100))
    data_contratacao = Column(Date)
    salario = Column(Numeric(10, 2))
    ativo = Column(Boolean, default=True)
    telefone = Column(String(20))
    endereco = Column(Text)
    
    pagamentos = relationship("Pagamento", back_populates="funcionario")
    
    def __repr__(self):
        return f"<Funcionario(nome='{self.nome}', cargo='{self.cargo}')>"

class Pagamento(Base):
    __tablename__ = 'pagamento'
    
    id = Column(Integer, primary_key=True)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))
    data = Column(Date, default=datetime.datetime.now)
    valor = Column(Numeric(10, 2), nullable=False)
    tipo = Column(String(50))  # Salário, Adiantamento, Bônus
    observacoes = Column(Text)
    
    funcionario = relationship("Funcionario", back_populates="pagamentos")
    
    def __repr__(self):
        return f"<Pagamento(funcionario_id='{self.funcionario_id}', valor='{self.valor}')>"

class Despesa(Base):
    __tablename__ = 'despesa'
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, default=datetime.datetime.now)
    categoria = Column(String(100))  # Insumos, Combustível, Manutenção, etc.
    forma_pagamento = Column(String(100))  # Dinheiro, Cartão, Transferência
    pago = Column(Boolean, default=True)
    observacoes = Column(Text)
    
    # Novas colunas
    fornecedor = Column(String(200))
    data_retirada = Column(Date)
    data_pagamento = Column(Date, default=datetime.datetime.now)
    usuario_adicionou = Column(String(100))
    data_adicionou = Column(Date, default=datetime.datetime.now)
    produto_retirado = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Despesa(descricao='{self.descricao}', valor='{self.valor}')>"

class Fornecedor(Base):
    __tablename__ = 'fornecedor'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False, unique=True)
    telefone = Column(String(20))
    email = Column(String(100))
    endereco = Column(Text)
    cnpj = Column(String(18))
    observacoes = Column(Text)
    data_cadastro = Column(Date, default=datetime.datetime.now)
    
    def __repr__(self):
        return f"<Fornecedor(nome='{self.nome}')>"

class Entrada(Base):
    __tablename__ = 'entrada'
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, default=datetime.datetime.now)
    categoria = Column(String(100))  # Venda de produtos, Serviços, etc.
    cliente = Column(String(100))
    recebido = Column(Boolean, default=True)
    observacoes = Column(Text)
    
    def __repr__(self):
        return f"<Entrada(descricao='{self.descricao}', valor='{self.valor}')>"

class Producao(Base):
    __tablename__ = 'producao'
    
    id = Column(Integer, primary_key=True)
    produto = Column(String(100), nullable=False)
    quantidade = Column(Float, nullable=False)
    unidade = Column(String(20))  # kg, ton, sacos, etc.
    data_inicio = Column(Date)
    data_fim = Column(Date)
    area = Column(Float)  # em hectares
    custo_total = Column(Numeric(10, 2))
    valor_venda = Column(Numeric(10, 2))
    observacoes = Column(Text)
    
    def __repr__(self):
        return f"<Producao(produto='{self.produto}', quantidade='{self.quantidade}')>" 