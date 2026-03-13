from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.database import SessionLocal
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.models.account import Account
from datetime import date, timedelta

class ReportService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_current_month_summary(self):
        """Retorna um resumo do mês atual."""
        today = date.today()
        start_of_month = today.replace(day=1)

        total_income = self.db.query(func.sum(Transaction.value)).filter(
            Transaction.transaction_date >= start_of_month,
            Transaction.transaction_type == TransactionType.INCOME
        ).scalar() or 0.0

        total_expense = self.db.query(func.sum(Transaction.value)).filter(
            Transaction.transaction_date >= start_of_month,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).scalar() or 0.0

        return {"income": total_income, "expense": total_expense}

    def get_total_balance(self):
        """Calcula o saldo total de todas as contas."""
        initial_balances = self.db.query(func.sum(Account.initial_balance)).scalar() or 0.0
        
        total_income = self.db.query(func.sum(Transaction.value)).filter(
            Transaction.transaction_type == TransactionType.INCOME
        ).scalar() or 0.0
        
        total_expense = self.db.query(func.sum(Transaction.value)).filter(
            Transaction.transaction_type == TransactionType.EXPENSE
        ).scalar() or 0.0

        return initial_balances + total_income - total_expense

    def get_expenses_by_category(self, year: int, month: int) -> list[tuple[str, float]]:
        """
        Retorna os gastos agregados por categoria para um determinado mês/ano.
        """
        start_date = date(year, month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        result = self.db.query(
            Category.name,
            func.sum(Transaction.value).label('total')
        ).join(Transaction, Category.id == Transaction.category_id).filter(
            Transaction.transaction_type == TransactionType.EXPENSE,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(Category.name).order_by(func.sum(Transaction.value).desc()).all()

        return result

    def get_monthly_income_expense_trend(self, months: int = 6) -> dict:
        """
        Retorna a tendência de receitas e despesas dos últimos 'months' meses.
        """
        today = date.today()
        results = {}

        for i in range(months - 1, -1, -1):
            target_month_date = today - timedelta(days=i * 30)
            month = target_month_date.month
            year = target_month_date.year
            month_key = f"{year}-{month:02d}"

            income = self.db.query(func.sum(Transaction.value)).filter(
                extract('year', Transaction.transaction_date) == year,
                extract('month', Transaction.transaction_date) == month,
                Transaction.transaction_type == TransactionType.INCOME
            ).scalar() or 0.0

            expense = self.db.query(func.sum(Transaction.value)).filter(
                extract('year', Transaction.transaction_date) == year,
                extract('month', Transaction.transaction_date) == month,
                Transaction.transaction_type == TransactionType.EXPENSE
            ).scalar() or 0.0
            
            results[month_key] = {"income": income, "expense": expense}

        return results
