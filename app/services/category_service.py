from sqlalchemy.orm import Session
from app.models.category import Category, TransactionType
from app.core.database import SessionLocal

class CategoryService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_all_categories(self) -> list[Category]:
        """Retorna todas as categorias, ordenadas por nome."""
        return self.db.query(Category).order_by(Category.name).all()

    def get_categories_by_type(self, transaction_type: TransactionType) -> list[Category]:
        """Retorna todas as categorias de um tipo específico (receita ou despesa)."""
        return self.db.query(Category).filter_by(transaction_type=transaction_type).order_by(Category.name).all()

    def create_category(self, name: str, transaction_type: TransactionType, color: str = None, icon: str = None) -> Category:
        """Cria e salva uma nova categoria."""
        
        # Validação simples
        if not name or not transaction_type:
            raise ValueError("Nome e tipo da transação são obrigatórios.")

        # Verifica se já existe uma categoria com o mesmo nome
        existing_category = self.db.query(Category).filter(Category.name.ilike(name)).first()
        if existing_category:
            raise ValueError(f"A categoria '{name}' já existe.")

        new_category = Category(
            name=name.strip(),
            transaction_type=transaction_type,
            color=color,
            icon=icon
        )
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def update_category(self, category_id: int, name: str, transaction_type: TransactionType, color: str = None, icon: str = None) -> Category | None:
        """Atualiza uma categoria existente."""
        category = self.db.query(Category).filter_by(id=category_id).first()
        if category:
            category.name = name.strip()
            category.transaction_type = transaction_type
            category.color = color
            category.icon = icon
            self.db.commit()
            self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        """Deleta uma categoria, se não estiver em uso."""
        category = self.db.query(Category).filter_by(id=category_id).first()
        if category:
            # Regra de negócio: não permitir exclusão se a categoria estiver em uso
            if category.transactions:
                raise ValueError("Não é possível excluir a categoria pois ela está associada a transações existentes.")
            
            self.db.delete(category)
            self.db.commit()
            return True
        return False
    
    def get_or_create_initial_categories(self):
        """Cria um conjunto de categorias iniciais se o banco estiver vazio."""
        if self.db.query(Category).count() == 0:
            initial_categories = [
                # Despesas
                {"name": "Moradia", "type": TransactionType.EXPENSE, "color": "#FF6347"},
                {"name": "Alimentação", "type": TransactionType.EXPENSE, "color": "#FFD700"},
                {"name": "Transporte", "type": TransactionType.EXPENSE, "color": "#4682B4"},
                {"name": "Saúde", "type": TransactionType.EXPENSE, "color": "#32CD32"},
                {"name": "Lazer", "type": TransactionType.EXPENSE, "color": "#9370DB"},
                {"name": "Educação", "type": TransactionType.EXPENSE, "color": "#1E90FF"},
                {"name": "Vestuário", "type": TransactionType.EXPENSE, "color": "#FF69B4"},
                {"name": "Impostos", "type": TransactionType.EXPENSE, "color": "#A9A9A9"},
                {"name": "Outras Despesas", "type": TransactionType.EXPENSE, "color": "#808080"},
                
                # Receitas
                {"name": "Salário", "type": TransactionType.INCOME, "color": "#00BFFF"},
                {"name": "Renda Extra", "type": TransactionType.INCOME, "color": "#ADFF2F"},
                {"name": "Investimentos", "type": TransactionType.INCOME, "color": "#DAA520"},
                {"name": "Outras Receitas", "type": TransactionType.INCOME, "color": "#D3D3D3"},
            ]
            for cat_data in initial_categories:
                self.create_category(name=cat_data["name"], transaction_type=cat_data["type"], color=cat_data["color"])
            print("Categorias iniciais criadas com sucesso.")

