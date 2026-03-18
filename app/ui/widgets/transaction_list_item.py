# app/ui/widgets/transaction_list_item.py
import customtkinter as ctk
from app.models.transaction import Transaction, TransactionType
from app.ui.theme import Theme
from app.utils.formatters import format_currency

class TransactionListItem(ctk.CTkFrame):
    def __init__(self, master, transaction: Transaction, on_edit, on_delete, **kwargs):
        super().__init__(master, fg_color=Theme.COLOR_SURFACE, corner_radius=10, **kwargs)

        self.transaction = transaction
        self.on_edit = on_edit
        self.on_delete = on_delete

        # --- Indicador de Cor ---
        indicator_color = Theme.COLOR_SUCCESS if transaction.transaction_type == TransactionType.INCOME else Theme.COLOR_ERROR
        self.indicator = ctk.CTkFrame(self, width=5, fg_color=indicator_color, corner_radius=0)
        self.indicator.pack(side="left", fill="y", padx=(0, 10))

        # --- Conteúdo Principal ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(1, weight=0) # Coluna do valor
        
        # Linha 1: Descrição e Categoria
        description_text = f"{transaction.description}"
        category_text = f"CAT: {transaction.category.name}"
        self.desc_label = ctk.CTkLabel(self.main_content, text=description_text, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=16, weight="bold"), anchor="w")
        self.desc_label.grid(row=0, column=0, sticky="w")
        self.category_label = ctk.CTkLabel(self.main_content, text=category_text, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12), text_color=Theme.COLOR_TEXT_SECONDARY, anchor="w")
        self.category_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # Linha 2: Data e Conta
        date_text = transaction.transaction_date.strftime('%d/%m/%Y')
        account_text = f"CONTA: {transaction.account.name}"
        self.date_label = ctk.CTkLabel(self.main_content, text=date_text, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12), text_color=Theme.COLOR_TEXT_SECONDARY, anchor="w")
        self.date_label.grid(row=2, column=0, sticky="w")
        
        # Valor
        signal = "+" if transaction.transaction_type == TransactionType.INCOME else "-"
        self.value_label = ctk.CTkLabel(self.main_content, text=f"{signal} {format_currency(transaction.value)}", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=20, weight="bold"), text_color=indicator_color)
        self.value_label.grid(row=0, column=1, rowspan=3, sticky="e", padx=(20, 10))

        # --- Botões de Ação (Inicialmente ocultos) ---
        self.action_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.edit_button = ctk.CTkButton(self.action_buttons_frame, text="✏️", width=30, height=30, command=self._on_edit_click, font=ctk.CTkFont(size=20), fg_color=Theme.COLOR_SECONDARY, hover_color=Theme.COLOR_PRIMARY)
        self.edit_button.pack(side="left", padx=(0, 5))
        
        self.delete_button = ctk.CTkButton(self.action_buttons_frame, text="🗑️", width=30, height=30, command=self._on_delete_click, font=ctk.CTkFont(size=20), fg_color=Theme.COLOR_SECONDARY, hover_color=Theme.COLOR_ERROR)
        self.delete_button.pack(side="left")

        # --- Comportamento de Hover ---
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        # Propaga o evento para os widgets filhos para que o hover funcione corretamente
        for widget in self.winfo_children():
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            if isinstance(widget, ctk.CTkFrame):
                 for child in widget.winfo_children():
                    child.bind("<Enter>", self._on_enter)
                    child.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        self.configure(fg_color=Theme.COLOR_SECONDARY)
        self.action_buttons_frame.pack(side="right", padx=20, pady=10)

    def _on_leave(self, event=None):
        # Verifica se o mouse ainda está dentro dos limites do frame principal
        if not self.winfo_containing(event.x_root, event.y_root) == self:
            self.configure(fg_color=Theme.COLOR_SURFACE)
            self.action_buttons_frame.pack_forget()

    def _on_edit_click(self):
        if self.on_edit:
            self.on_edit(self.transaction)

    def _on_delete_click(self):
        if self.on_delete:
            self.on_delete(self.transaction)
