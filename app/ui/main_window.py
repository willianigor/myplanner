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
from app.ui.theme import Theme

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Planner Financeiro")
        self.geometry("1200x780")
        self.minsize(960, 600)
        
        # Aplica a cor de fundo principal da janela
        self.configure(fg_color=Theme.COLOR_BACKGROUND)

        # Configuração do grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.views = {}
        self.current_view = None

    def create_widgets(self):
        """Cria e posiciona os widgets principais da aplicação."""
        
        # --- Sidebar ---
        self.sidebar_frame = Sidebar(master=self, controller=self, corner_radius=0)

        # --- Container para as Views ---
        self.main_view_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_view_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
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
            # As views devem ter o fundo da cor de "superfície"
            view = ViewClass(self.main_view_container, fg_color=Theme.COLOR_SURFACE)
            self.views[name] = view
            view.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Exibir a view inicial
        self.show_view("dashboard")

    def show_view(self, view_name):
        """
        Eleva a view especificada para o topo e notifica a sidebar para
        atualizar seu estado visual.
        """
        selected_view = self.views.get(view_name)
        if selected_view:
            # Eleva a view para o topo
            selected_view.tkraise()
            
            # Notifica a sidebar sobre a mudança
            self.sidebar_frame.set_active_view(view_name)

            # Chama o método on_show se a view o tiver
            if hasattr(selected_view, "on_show") and callable(getattr(selected_view, "on_show")):
                selected_view.on_show()

