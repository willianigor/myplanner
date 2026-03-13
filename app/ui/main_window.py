import customtkinter as ctk
from app.ui.sidebar import Sidebar
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.transactions_view import TransactionsView
from app.ui.views.budgets_view import BudgetsView
from app.ui.views.goals_view import GoalsView
from app.ui.views.reports_view import ReportsView
from app.ui.views.categories_view import CategoriesView
from app.ui.views.settings_view import SettingsView
from app.ui.views.accounts_view import AccountsView

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Planner Financeiro")
        self.geometry("1200x780")
        self.minsize(960, 600)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.views = {}
        self.sidebar_buttons = {}
        self.current_view = None

    def create_widgets(self):
        """Cria e posiciona os widgets principais da aplicação."""
        
        # --- Sidebar ---
        self.sidebar_frame = Sidebar(master=self, controller=self, corner_radius=0)
        self.sidebar_buttons = self.sidebar_frame.get_buttons()

        # --- Container para as Views ---
        self.main_view_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_view_container.grid(row=0, column=1, sticky="nsew")
        self.main_view_container.grid_rowconfigure(0, weight=1)
        self.main_view_container.grid_columnconfigure(0, weight=1)
        
        # --- Instanciar Views ---
        for ViewClass, name in [
            (DashboardView, "dashboard"),
            (TransactionsView, "transactions"),
            (AccountsView, "accounts"),
            (BudgetsView, "budgets"),
            (GoalsView, "goals"),
            (ReportsView, "reports"),
            (CategoriesView, "categories"),
            (SettingsView, "settings")
        ]:
            view = ViewClass(self.main_view_container)
            self.views[name] = view
            view.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Exibir a view inicial
        self.show_view("dashboard")

    def show_view(self, view_name):
        """
        Eleva a view especificada para o topo, atualiza o estado dos botões,
        e chama o método on_show, se existir.
        """
        # Itera sobre as views e eleva a que foi selecionada
        selected_view = self.views.get(view_name)
        if selected_view:
            selected_view.tkraise()
            # Chama o método on_show se a view o tiver
            if hasattr(selected_view, "on_show") and callable(getattr(selected_view, "on_show")):
                selected_view.on_show()

        # Atualiza o estado dos botões do sidebar
        for name, button in self.sidebar_buttons.items():
            if name == view_name:
                # Botão ativo
                button.configure(fg_color=button.cget("hover_color"))
            else:
                # Botão inativo
                button.configure(fg_color="transparent")
