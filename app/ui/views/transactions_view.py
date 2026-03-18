import customtkinter as ctk
from tkinter import messagebox
from app.services.transaction_service import TransactionService
from app.models.transaction import Transaction
from app.ui.dialogs.transaction_dialog import TransactionDialog
from app.ui.widgets.transaction_list_item import TransactionListItem
from app.ui.theme import Theme
from datetime import date, timedelta

class TransactionsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = TransactionService()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._create_widgets()
        self._load_transactions()

    def _create_widgets(self):
        # --- Barra de Título e Ação Principal ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="Histórico de Transações", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=24, weight="bold"))
        title_label.grid(row=0, column=0, sticky="w")
        
        self.add_button = ctk.CTkButton(
            header_frame,
            text="+ Nova Transação",
            command=self._add_transaction,
            height=35,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14, weight="bold"),
            fg_color=Theme.COLOR_PRIMARY,
            hover_color=Theme.COLOR_SECONDARY
        )
        self.add_button.grid(row=0, column=1, sticky="e")

        # --- Frame de Filtros ---
        filters_frame = ctk.CTkFrame(self, fg_color="transparent")
        filters_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # TODO: Adicionar filtros mais avançados de Categoria e Conta
        ctk.CTkLabel(filters_frame, text="Filtrar por data:").pack(side="left", padx=(0, 10))
        
        today = date.today()
        first_day_of_month = today.replace(day=1)

        self.start_date_entry = ctk.CTkEntry(filters_frame, placeholder_text="DD/MM/AAAA", width=120)
        self.start_date_entry.insert(0, first_day_of_month.strftime("%d/%m/%Y"))
        self.start_date_entry.pack(side="left", padx=5)

        ctk.CTkLabel(filters_frame, text="até").pack(side="left", padx=5)
        
        self.end_date_entry = ctk.CTkEntry(filters_frame, placeholder_text="DD/MM/AAAA", width=120)
        self.end_date_entry.insert(0, today.strftime("%d/%m/%Y"))
        self.end_date_entry.pack(side="left", padx=5)

        self.filter_button = ctk.CTkButton(filters_frame, text="Filtrar", width=100, command=self._load_transactions)
        self.filter_button.pack(side="left", padx=10)

        # --- Lista de transações ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def _load_transactions(self):
        # Limpa a lista atual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # TODO: Implementar a lógica de filtro por data
            transactions = self.service.get_transactions(limit=100)
            
            if not transactions:
                no_data_label = ctk.CTkLabel(self.scrollable_frame, text="Nenhuma transação encontrada.", font=ctk.CTkFont(size=16), text_color=Theme.COLOR_TEXT_SECONDARY)
                no_data_label.pack(pady=50)
                return

            # Cria um novo item para cada transação
            for i, trans in enumerate(transactions):
                item = TransactionListItem(
                    master=self.scrollable_frame,
                    transaction=trans,
                    on_edit=self._edit_transaction,
                    on_delete=self._delete_transaction
                )
                item.pack(fill="x", padx=5, pady=(0, 8))

        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar as transações: {e}")

    def _add_transaction(self):
        # TODO: Refatorar o TransactionDialog para o novo tema
        dialog = TransactionDialog(self, title="Adicionar Nova Transação")
        result = dialog.get_input()
        if result:
            try:
                self.service.create_transaction(result)
                self._load_transactions() # Recarrega a lista
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e), parent=self)

    def _edit_transaction(self, trans: Transaction):
        dialog = TransactionDialog(self, title=f"Editar Transação", transaction=trans)
        result = dialog.get_input()
        if result:
            try:
                self.service.update_transaction(transaction_id=trans.id, data=result)
                self._load_transactions()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e), parent=self)

    def _delete_transaction(self, trans: Transaction):
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a transação '{trans.description}'?", icon='warning'):
            try:
                self.service.delete_transaction(transaction_id=trans.id)
                self._load_transactions()
            except Exception as e:
                messagebox.showerror("Erro ao Excluir", f"Ocorreu um erro: {e}")

    def on_show(self):
        """Método para ser chamado quando a view é exibida."""
        self._load_transactions()
