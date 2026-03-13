from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.core.database import SessionLocal
from datetime import date
from typing import Optional

class TransactionService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_transactions(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[TransactionType] = None,
        category_id: Optional[int] = None,
        account_id: Optional[int] = None,
        limit: int = 100
    ) -> list[Transaction]:
        """
        Retorna uma lista de transações com base em filtros.
        """
        query = self.db.query(Transaction)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)

        return query.order_by(desc(Transaction.transaction_date)).limit(limit).all()

    def create_transaction(self, data: dict) -> Transaction:
        """
        Cria uma nova transação a partir de um dicionário de dados.
        """
        # Validação
        required_fields = ["description", "value", "transaction_date", "transaction_type", "category_id", "account_id"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Campo obrigatório '{field}' ausente.")

        new_transaction = Transaction(**data)
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        return new_transaction

    def update_transaction(self, transaction_id: int, data: dict) -> Transaction | None:
        """
        Atualiza uma transação existente.
        """
        transaction = self.db.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            for key, value in data.items():
                setattr(transaction, key, value)
            self.db.commit()
            self.db.refresh(transaction)
        return transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """Deleta uma transação."""
        transaction = self.db.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            self.db.delete(transaction)
            self.db.commit()
            return True
        return False
    
    def get_monthly_summary(self, year: int, month: int) -> dict:
        """
        Retorna um resumo de receitas e despesas para um determinado mês/ano.
        """
        total_income = self.db.query(func.sum(Transaction.value)).filter(
            func.extract('year', Transaction.transaction_date) == year,
            func.extract('month', Transaction.transaction_date) == month,
            Transaction.transaction_type == TransactionType.INCOME
        ).scalar() or 0.0

        total_expense = self.db.query(func.sum(Transaction.value)).filter(
            func.extract('year', Transaction.transaction_date) == year,
            func.extract('month', Transaction.transaction_date) == month,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).scalar() or 0.0

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense
        }

