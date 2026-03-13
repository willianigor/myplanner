import customtkinter as ctk
from tkinter import messagebox
from app.services.transaction_service import TransactionService
from app.services.category_service import CategoryService, TransactionType
from app.services.account_service import AccountService
from app.models.transaction import Transaction
from app.ui.dialogs.transaction_dialog import TransactionDialog
from app.utils.formatters import format_currency
from datetime import date

class TransactionsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = TransactionService()
        self.category_service = CategoryService()
        self.account_service = AccountService()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._create_widgets()
        self._load_filter_options()
        self._load_transactions()

    def _create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(self, text="Gestão de Transações", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Frame de Filtros e Ações
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        ctk.CTkLabel(filters_frame, text="De:").pack(side="left", padx=(10, 5))
        self.start_date_entry = ctk.CTkEntry(filters_frame, placeholder_text="DD/MM/AAAA", width=120)
        self.start_date_entry.pack(side="left", padx=5)

        ctk.CTkLabel(filters_frame, text="Até:").pack(side="left", padx=(10, 5))
        self.end_date_entry = ctk.CTkEntry(filters_frame, placeholder_text="DD/MM/AAAA", width=120)
        self.end_date_entry.pack(side="left", padx=5)

        self.filter_button = ctk.CTkButton(filters_frame, text="Filtrar", width=100, command=self._load_transactions)
        self.filter_button.pack(side="left", padx=10)
        
        self.add_button = ctk.CTkButton(filters_frame, text="+ Nova Transação", width=160, command=self._add_transaction)
        self.add_button.pack(side="right", padx=10, pady=10)

        # Lista de transações
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def _load_filter_options(self):
        # Placeholder para carregar categorias e contas nos filtros se necessário
        # Por simplicidade, os filtros de categoria/conta foram omitidos do layout inicial
        pass

    def _load_transactions(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # Coleta de filtros (simplificado por enquanto)
            transactions = self.service.get_transactions(limit=200) # Pega as 200 mais recentes
            for trans in transactions:
                self._create_transaction_entry(trans)
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar as transações: {e}")

    def _create_transaction_entry(self, trans: Transaction):
        entry_frame = ctk.CTkFrame(self.scrollable_frame)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(0, weight=1)

        # Cores e Sinais
        value_color = "red" if trans.transaction_type == TransactionType.EXPENSE else "green"
        signal = "-" if trans.transaction_type == TransactionType.EXPENSE else "+"
        
        # Linha 1: Descrição e Valor
        top_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5,0))
        top_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(top_frame, text=trans.description, font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(top_frame, text=f"{signal} {format_currency(trans.value)}", text_color=value_color, font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="e")
        
        # Linha 2: Categoria e Conta
        mid_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        mid_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)
        mid_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(mid_frame, text=f"Categoria: {trans.category.name}", text_color="gray").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(mid_frame, text=f"Conta: {trans.account.name}", text_color="gray").grid(row=0, column=1, sticky="e")
        
        # Linha 3: Data e Botões
        bottom_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,5))
        bottom_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(bottom_frame, text=f"Data: {trans.transaction_date.strftime('%d/%m/%Y')}", text_color="gray").grid(row=0, column=0, sticky="w")
        
        buttons = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        buttons.grid(row=0, column=1, sticky="e")
        ctk.CTkButton(buttons, text="Editar", width=60, command=lambda t=trans: self._edit_transaction(t)).pack(side="left", padx=5)
        ctk.CTkButton(buttons, text="Excluir", width=60, fg_color=("#F44336", "#C62828"), hover_color=("#E53935", "#B71C1C"), command=lambda t=trans: self._delete_transaction(t)).pack(side="left")

    def _add_transaction(self):
        dialog = TransactionDialog(self, title="Adicionar Nova Transação")
        result = dialog.get_input()
        if result:
            try:
                self.service.create_transaction(result)
                messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
                self._load_transactions()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e), parent=self)

    def _edit_transaction(self, trans: Transaction):
        dialog = TransactionDialog(self, title=f"Editar Transação", transaction=trans)
        result = dialog.get_input()
        if result:
            try:
                self.service.update_transaction(transaction_id=trans.id, data=result)
                messagebox.showinfo("Sucesso", "Transação atualizada com sucesso!")
                self._load_transactions()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e), parent=self)

    def _delete_transaction(self, trans: Transaction):
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a transação '{trans.description}'?"):
            try:
                self.service.delete_transaction(transaction_id=trans.id)
                messagebox.showinfo("Sucesso", "Transação excluída com sucesso!")
                self._load_transactions()
            except Exception as e:
                messagebox.showerror("Erro ao Excluir", f"Ocorreu um erro: {e}")

    def on_show(self):
        """Método para ser chamado quando a view é exibida."""
        print("A view de Transações está sendo exibida. Recarregando...")
        self._load_transactions()
