from sqlalchemy.orm import Session
from app.models.account import Account
from app.core.database import SessionLocal

class AccountService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_all_accounts(self) -> list[Account]:
        """Retorna todas as contas, ordenadas por nome."""
        return self.db.query(Account).order_by(Account.name).all()

    def create_account(self, name: str, account_type: str, initial_balance: float = 0.0) -> Account:
        """Cria e salva uma nova conta."""
        if not name or not account_type:
            raise ValueError("Nome e tipo da conta são obrigatórios.")

        existing_account = self.db.query(Account).filter(Account.name.ilike(name)).first()
        if existing_account:
            raise ValueError(f"A conta '{name}' já existe.")

        new_account = Account(
            name=name.strip(),
            account_type=account_type,
            initial_balance=initial_balance
        )
        self.db.add(new_account)
        self.db.commit()
        self.db.refresh(new_account)
        return new_account

    def update_account(self, account_id: int, name: str, account_type: str, initial_balance: float) -> Account | None:
        """Atualiza uma conta existente."""
        account = self.db.query(Account).filter_by(id=account_id).first()
        if account:
            account.name = name.strip()
            account.account_type = account_type
            account.initial_balance = initial_balance
            self.db.commit()
            self.db.refresh(account)
        return account

    def delete_account(self, account_id: int) -> bool:
        """Deleta uma conta, se não estiver em uso."""
        account = self.db.query(Account).filter_by(id=account_id).first()
        if account:
            if account.transactions:
                raise ValueError("Não é possível excluir a conta pois ela está associada a transações existentes.")
            
            self.db.delete(account)
            self.db.commit()
            return True
        return False
        
    def get_or_create_initial_accounts(self):
        """Cria contas iniciais se nenhuma existir."""
        if self.db.query(Account).count() == 0:
            initial_accounts = [
                {"name": "Carteira", "type": "Dinheiro", "balance": 50.0},
                {"name": "Conta Corrente", "type": "Conta Bancária", "balance": 1500.0},
            ]
            for acc_data in initial_accounts:
                self.create_account(
                    name=acc_data["name"], 
                    account_type=acc_data["type"], 
                    initial_balance=acc_data["balance"]
                )
            print("Contas iniciais criadas com sucesso.")
