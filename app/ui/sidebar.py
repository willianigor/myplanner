import customtkinter as ctk
from app.ui.theme import Theme

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.buttons = {}

        # Configuração do Frame
        self.configure(width=220, fg_color=Theme.COLOR_SURFACE)
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(8, weight=1)  # Espaço para empurrar config para baixo

        # Título
        self.logo_label = ctk.CTkLabel(self, text="MyPlanner", text_color=Theme.COLOR_PRIMARY, font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 25))

        # Botões de Navegação
        nav_buttons = {
            1: ("dashboard", "Dashboard"),
            2: ("transactions", "Transações"),
            3: ("accounts", "Contas"),
            4: ("budgets", "Orçamentos"),
            5: ("goals", "Metas"),
            6: ("reports", "Relatórios"),
            7: ("categories", "Categorias"),
        }

        for row, (name, text) in nav_buttons.items():
            button = ctk.CTkButton(
                self,
                text=text,
                command=lambda n=name: self.controller.show_view(n),
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color=Theme.COLOR_TEXT_SECONDARY,
                hover_color=Theme.COLOR_SECONDARY,
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            button.grid(row=row, column=0, padx=20, pady=5, sticky="ew")
            self.buttons[name] = button

        # Botão de Configurações na parte inferior
        settings_button = ctk.CTkButton(
            self,
            text="Configurações",
            command=lambda: self.controller.show_view("settings"),
            height=40,
            corner_radius=8,
            fg_color="transparent",
            text_color=Theme.COLOR_TEXT_SECONDARY,
            hover_color=Theme.COLOR_SECONDARY,
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        settings_button.grid(row=9, column=0, padx=20, pady=(5, 20), sticky="ew")
        self.buttons["settings"] = settings_button

    def set_active_view(self, view_name):
        """Atualiza o estado visual dos botões, destacando o ativo."""
        for name, button in self.buttons.items():
            if name == view_name:
                # Botão ativo
                button.configure(fg_color=Theme.COLOR_PRIMARY, text_color=Theme.COLOR_TEXT_PRIMARY)
            else:
                # Botão inativo
                button.configure(fg_color="transparent", text_color=Theme.COLOR_TEXT_SECONDARY)
