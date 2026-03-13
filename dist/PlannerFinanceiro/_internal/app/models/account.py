from __future__ import annotations
import typing
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if typing.TYPE_CHECKING:
    from app.models.transaction import Transaction

class Account(Base):
    """
    Modelo para representar uma conta do usuário (ex: carteira, conta bancária).
    """
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    account_type: Mapped[str] = mapped_column(String(50))  # Ex: "Conta Corrente", "Carteira", "Investimentos"
    initial_balance: Mapped[float] = mapped_column(Float, default=0.0)

    # Relacionamento: uma conta pode ter várias transações
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, name='{self.name}')>"
