import customtkinter as ctk
from app.models.account import Account

class AccountDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str, account: Account = None):
        super().__init__(master)
        self.transient(master)
        self.title(title)
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.grid_columnconfigure(1, weight=1)

        self.result = None
        self.account = account

        # --- Widgets ---
        self.name_label = ctk.CTkLabel(self, text="Nome da Conta:")
        self.name_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.name_entry = ctk.CTkEntry(self, width=250)
        self.name_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        self.type_label = ctk.CTkLabel(self, text="Tipo da Conta:")
        self.type_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.type_entry = ctk.CTkEntry(self, width=250, placeholder_text="Ex: Conta Corrente, Carteira")
        self.type_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.balance_label = ctk.CTkLabel(self, text="Saldo Inicial (R$):")
        self.balance_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.balance_entry = ctk.CTkEntry(self, width=250, placeholder_text="0.00")
        self.balance_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        # Preencher dados se for edição
        if account:
            self.name_entry.insert(0, account.name)
            self.type_entry.insert(0, account.account_type)
            self.balance_entry.insert(0, str(account.initial_balance))
            # Desabilitar saldo inicial na edição para evitar inconsistências
            self.balance_entry.configure(state="disabled")

        # --- Botões de Ação ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.save_button = ctk.CTkButton(self.buttons_frame, text="Salvar", command=self._on_save)
        self.save_button.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancelar", command=self._on_cancel, fg_color="gray")
        self.cancel_button.grid(row=0, column=1, padx=(5, 0), sticky="w")
        
        self.name_entry.focus()
        self.grab_set() # Torna a janela modal

    def _on_save(self):
        name = self.name_entry.get().strip()
        account_type = self.type_entry.get().strip()
        balance_str = self.balance_entry.get().strip().replace(",", ".")

        if not name or not account_type:
            messagebox.showerror("Erro de Validação", "Nome e Tipo da conta são obrigatórios.", parent=self)
            return
            
        try:
            balance = float(balance_str) if balance_str else 0.0
        except ValueError:
            messagebox.showerror("Erro de Validação", "Saldo inicial deve ser um número válido.", parent=self)
            return

        self.result = {
            "name": name,
            "account_type": account_type,
            "initial_balance": balance
        }
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def get_input(self):
        """Espera a janela ser destruída e retorna o resultado."""
        self.wait_window()
        return self.result
