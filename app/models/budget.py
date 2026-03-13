from __future__ import annotations
import typing
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from app.models.base import Base

if typing.TYPE_CHECKING:
    from app.models.category import Category

class Budget(Base):
    """
    Modelo para orçamento mensal por categoria.
    Define um valor planejado de gastos para uma categoria em um mês/ano específico.
    """
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # O orçamento é definido para um mês e ano específicos
    month: Mapped[int] = mapped_column(Integer, nullable=False) # 1-12
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    planned_value: Mapped[float] = mapped_column(Float, nullable=False)

    # Chave estrangeira para a categoria
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # Relacionamento
    category: Mapped["Category"] = relationship(back_populates="budgets")

    # Garante que só exista uma entrada de orçamento por categoria, por mês e ano.
    __table_args__ = (
        UniqueConstraint('category_id', 'month', 'year', name='_category_month_year_uc'),
    )

    def __repr__(self) -> str:
        return f"<Budget(id={self.id}, category_id={self.category_id}, month={self.month}/{self.year}, planned={self.planned_value})>"
