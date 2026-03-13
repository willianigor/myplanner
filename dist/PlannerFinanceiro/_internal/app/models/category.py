from __future__ import annotations
import typing
from sqlalchemy import String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import enum

if typing.TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.budget import Budget

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Category(Base):
    """
    Modelo para categorias de receitas e despesas.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLAlchemyEnum(TransactionType), nullable=False)
    
    # Opcional: para agrupar visualmente (ex: cor em gráficos)
    color: Mapped[str | None] = mapped_column(String(7))  # Formato hexadecimal, ex: #RRGGBB
    icon: Mapped[str | None] = mapped_column(String(50))

    # Relacionamentos
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")
    budgets: Mapped[list["Budget"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}', type='{self.transaction_type.value}')>"
