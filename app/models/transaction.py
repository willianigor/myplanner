from __future__ import annotations
import typing
from sqlalchemy import String, Float, Date, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.category import TransactionType
from datetime import date

if typing.TYPE_CHECKING:
    from app.models.account import Account
    from app.models.category import Category

class Transaction(Base):
    """
    Modelo unificado para transações (receitas e despesas).
    """
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLAlchemyEnum(TransactionType), nullable=False)
    
    # Chaves estrangeiras
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))

    # Relacionamentos
    category: Mapped["Category"] = relationship(back_populates="transactions")
    account: Mapped["Account"] = relationship(back_populates="transactions")
    
    # Campos específicos para despesas
    is_paid: Mapped[bool | None] = mapped_column() # Status de pagamento para despesas
    due_date: Mapped[date | None] = mapped_column(Date) # Data de vencimento

    # Campos para recorrência (simplificado)
    is_recurring: Mapped[bool] = mapped_column(default=False)
    
    notes: Mapped[str | None] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, desc='{self.description}', value={self.value})>"
