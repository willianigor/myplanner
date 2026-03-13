import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
        self.configure(width=200)

        # Layout do frame do sidebar
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(8, weight=1) # Espaço para empurrar config para baixo

        # Título
        self.logo_label = ctk.CTkLabel(self, text="Planner", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Botões de Navegação
        self.dashboard_button = ctk.CTkButton(self, text="Dashboard", command=lambda: self.controller.show_view("dashboard"))
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.transactions_button = ctk.CTkButton(self, text="Transações", command=lambda: self.controller.show_view("transactions"))
        self.transactions_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.accounts_button = ctk.CTkButton(self, text="Contas", command=lambda: self.controller.show_view("accounts"))
        self.accounts_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.budgets_button = ctk.CTkButton(self, text="Orçamentos", command=lambda: self.controller.show_view("budgets"))
        self.budgets_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.goals_button = ctk.CTkButton(self, text="Metas", command=lambda: self.controller.show_view("goals"))
        self.goals_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.reports_button = ctk.CTkButton(self, text="Relatórios", command=lambda: self.controller.show_view("reports"))
        self.reports_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        self.categories_button = ctk.CTkButton(self, text="Categorias", command=lambda: self.controller.show_view("categories"))
        self.categories_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        # Botão de Configurações na parte inferior
        self.settings_button = ctk.CTkButton(self, text="Configurações", command=lambda: self.controller.show_view("settings"))
        self.settings_button.grid(row=9, column=0, padx=20, pady=(10, 20), sticky="ew")

    def get_buttons(self):
        """Retorna todos os botões para gerenciamento de estado (ex: destacar o ativo)."""
        return {
            "dashboard": self.dashboard_button,
            "transactions": self.transactions_button,
            "accounts": self.accounts_button,
            "budgets": self.budgets_button,
            "goals": self.goals_button,
            "reports": self.reports_button,
            "categories": self.categories_button,
            "settings": self.settings_button,
        }
