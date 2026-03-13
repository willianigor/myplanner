import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.helpers import resource_path # MODIFICADO

# Define o caminho para o diretório de dados da aplicação usando a função auxiliar
DATA_DIR = resource_path("app/data") # MODIFICADO
DATA_DIR.mkdir(exist_ok=True)

# Define o caminho completo para o arquivo do banco de dados
DATABASE_URL = f"sqlite:///{DATA_DIR / 'planner.db'}"

# Cria a engine de conexão com o banco de dados
# O argumento connect_args é específico para o SQLite e é recomendado para
# evitar problemas de concorrência com threads.
engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Desativado para a build final
    connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões que será usada para criar sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Função para obter uma sessão de banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa o banco de dados, criando todas as tabelas.
    Esta função deve ser chamada na inicialização da aplicação.
    """
    # Importar todos os modelos aqui garante que eles sejam registrados no SQLAlchemy
    from app.models.base import Base
    from app.models.account import Account
    from app.models.category import Category
    from app.models.transaction import Transaction
    from app.models.goal import Goal
    from app.models.budget import Budget
    
    # Cria todas as tabelas no banco de dados que não existirem
    Base.metadata.create_all(bind=engine)
