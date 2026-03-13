import customtkinter as ctk
from tkinter import messagebox
from app.services.account_service import AccountService
from app.models.account import Account
from app.ui.dialogs.account_dialog import AccountDialog
from app.utils.formatters import format_currency

class AccountsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = AccountService()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="Gestão de Contas", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, sticky="w")
        
        add_button = ctk.CTkButton(header_frame, text="Adicionar Conta", width=140, command=self._add_account)
        add_button.grid(row=0, column=1, sticky="e")

        # Lista de Contas
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self._load_accounts()

    def _load_accounts(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        accounts = self.service.get_all_accounts()
        for account in accounts:
            self._create_account_entry(account)

    def _create_account_entry(self, account: Account):
        entry_frame = ctk.CTkFrame(self.scrollable_frame)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)

        info_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        info_frame.grid_columnconfigure(1, weight=1)

        name_label = ctk.CTkLabel(info_frame, text=account.name, font=ctk.CTkFont(weight="bold"), anchor="w")
        name_label.grid(row=0, column=0, sticky="w")
        
        balance_label = ctk.CTkLabel(info_frame, text=f"Saldo Inicial: {format_currency(account.initial_balance)}", anchor="e")
        balance_label.grid(row=0, column=1, sticky="e")

        type_label = ctk.CTkLabel(info_frame, text=account.account_type, text_color="gray", anchor="w")
        type_label.grid(row=1, column=0, columnspan=2, sticky="w")

        buttons_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        edit_button = ctk.CTkButton(buttons_frame, text="Editar", width=60, command=lambda acc=account: self._edit_account(acc))
        edit_button.pack(side="left", padx=5)

        delete_button = ctk.CTkButton(buttons_frame, text="Excluir", width=60, fg_color=("#F44336", "#C62828"), hover_color=("#E53935", "#B71C1C"), command=lambda acc=account: self._delete_account(acc))
        delete_button.pack(side="left", padx=5)

    def _add_account(self):
        dialog = AccountDialog(self, title="Adicionar Nova Conta")
        result = dialog.get_input()
        if result:
            try:
                self.service.create_account(
                    name=result["name"],
                    account_type=result["account_type"],
                    initial_balance=result["initial_balance"]
                )
                messagebox.showinfo("Sucesso", "Conta adicionada com sucesso!")
                self._load_accounts()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e), parent=self)

    def _edit_account(self, account: Account):
        dialog = AccountDialog(self, title=f"Editar Conta: {account.name}", account=account)
        result = dialog.get_input()
        if result:
            try:
                self.service.update_account(
                    account_id=account.id,
                    name=result["name"],
                    account_type=result["account_type"],
                    initial_balance=result["initial_balance"] # O diálogo desabilita, mas passamos mesmo assim
                )
                messagebox.showinfo("Sucesso", "Conta atualizada com sucesso!")
                self._load_accounts()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e), parent=self)

    def _delete_account(self, account: Account):
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a conta '{account.name}'?"):
            try:
                self.service.delete_account(account_id=account.id)
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
                self._load_accounts()
            except ValueError as e:
                messagebox.showerror("Erro ao Excluir", str(e))
