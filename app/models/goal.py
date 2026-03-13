from sqlalchemy import String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from datetime import date

class Goal(Base):
    """
    Modelo para metas financeiras.
    """
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0)
    target_date: Mapped[date | None] = mapped_column(Date)
    
    # Prioridade pode ser usada para ordenação
    priority: Mapped[int] = mapped_column(default=1) # Ex: 1-Baixa, 2-Média, 3-Alta

    notes: Mapped[str | None] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"<Goal(id={self.id}, name='{self.name}', target={self.target_value})>"
