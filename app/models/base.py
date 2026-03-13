from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Classe base para todos os modelos do SQLAlchemy.
    Todos os modelos de dados da aplicação devem herdar desta classe.
    """
    pass
