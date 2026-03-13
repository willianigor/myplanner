import customtkinter as ctk
from tkinter import messagebox
from app.models.transaction import Transaction
from app.models.category import TransactionType
from app.services.category_service import CategoryService
from app.services.account_service import AccountService
from datetime import date

class TransactionDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str, transaction: Transaction = None):
        super().__init__(master)
        self.transient(master)
        self.title(title)
        self.geometry("500x550")
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.grid_columnconfigure(1, weight=1)

        self.result = None
        self.transaction = transaction

        # --- Serviços ---
        self.category_service = CategoryService()
        self.account_service = AccountService()
        
        # --- Listas de dados ---
        self.categories = []
        self.accounts = self.account_service.get_all_accounts()

        # --- Widgets ---
        self._create_widgets()
        self._load_initial_data()
        
        self.description_entry.focus()
        self.grab_set()

    def _create_widgets(self):
        # ... (criação de labels e entries) ...
        ctk.CTkLabel(self, text="Descrição:").grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.description_entry = ctk.CTkEntry(self, width=300)
        self.description_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        ctk.CTkLabel(self, text="Valor (R$):").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.value_entry = ctk.CTkEntry(self, placeholder_text="0.00")
        self.value_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Data:").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.date_entry = ctk.CTkEntry(self, placeholder_text="DD/MM/AAAA")
        self.date_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Tipo:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.type_menu = ctk.CTkOptionMenu(self, values=["Despesa", "Receita"], command=self._on_type_change)
        self.type_menu.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(self, text="Categoria:").grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.category_menu = ctk.CTkOptionMenu(self, values=["Selecione uma categoria"])
        self.category_menu.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Conta:").grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.account_menu = ctk.CTkOptionMenu(self, values=[acc.name for acc in self.accounts] or ["Nenhuma conta encontrada"])
        self.account_menu.grid(row=5, column=1, padx=20, pady=10, sticky="ew")
        
        # --- Botões ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(self.buttons_frame, text="Salvar", command=self._on_save).grid(row=0, column=0, padx=(0, 5), sticky="e")
        ctk.CTkButton(self.buttons_frame, text="Cancelar", command=self._on_cancel, fg_color="gray").grid(row=0, column=1, padx=(5, 0), sticky="w")
        
    def _load_initial_data(self):
        # Preenche os campos se for uma edição
        if self.transaction:
            self.description_entry.insert(0, self.transaction.description)
            self.value_entry.insert(0, f"{self.transaction.value:.2f}".replace(".", ","))
            self.date_entry.insert(0, self.transaction.transaction_date.strftime("%d/%m/%Y"))
            
            trans_type_str = "Receita" if self.transaction.transaction_type == TransactionType.INCOME else "Despesa"
            self.type_menu.set(trans_type_str)
            self._update_category_menu(self.transaction.transaction_type)
            
            self.category_menu.set(self.transaction.category.name)
            self.account_menu.set(self.transaction.account.name)
        else:
            # Define valores padrão para criação
            self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
            self.type_menu.set("Despesa")
            self._update_category_menu(TransactionType.EXPENSE)

    def _on_type_change(self, new_type_str: str):
        trans_type = TransactionType.INCOME if new_type_str == "Receita" else TransactionType.EXPENSE
        self._update_category_menu(trans_type)

    def _update_category_menu(self, trans_type: TransactionType):
        self.categories = self.category_service.get_categories_by_type(trans_type)
        cat_names = [cat.name for cat in self.categories] or ["Nenhuma categoria encontrada"]
        self.category_menu.configure(values=cat_names)
        self.category_menu.set(cat_names[0])

    def _on_save(self):
        # ... (Validação e coleta de dados) ...
        try:
            desc = self.description_entry.get().strip()
            value_str = self.value_entry.get().strip().replace(",", ".")
            date_str = self.date_entry.get().strip()
            
            if not desc or not value_str or not date_str:
                raise ValueError("Descrição, valor e data são obrigatórios.")

            value = float(value_str)
            trans_date = date(int(date_str[6:]), int(date_str[3:5]), int(date_str[:2]))
            
            trans_type_str = self.type_menu.get()
            trans_type = TransactionType.INCOME if trans_type_str == "Receita" else TransactionType.EXPENSE

            cat_name = self.category_menu.get()
            category = next((cat for cat in self.categories if cat.name == cat_name), None)
            
            acc_name = self.account_menu.get()
            account = next((acc for acc in self.accounts if acc.name == acc_name), None)

            if not category or not account:
                raise ValueError("Categoria ou Conta inválida.")

            self.result = {
                "description": desc, "value": value, "transaction_date": trans_date,
                "transaction_type": trans_type, "category_id": category.id, "account_id": account.id
            }
            self.destroy()

        except (ValueError, IndexError) as e:
            messagebox.showerror("Erro de Validação", f"Por favor, verifique os dados: {e}", parent=self)

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def get_input(self):
        self.wait_window()
        return self.result
