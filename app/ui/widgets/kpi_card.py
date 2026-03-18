# app/ui/widgets/kpi_card.py
import customtkinter as ctk
from app.ui.theme import Theme

class KPICard(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.COLOR_SURFACE,
            corner_radius=12,
            **kwargs
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=15, weight="bold"),
            text_color=Theme.COLOR_TEXT_SECONDARY
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.value_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=32, weight="bold"),
            text_color=Theme.COLOR_TEXT_PRIMARY
        )
        self.value_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

    def set_value(self, value_text, color=None):
        """Atualiza o valor exibido no card e, opcionalmente, sua cor."""
        self.value_label.configure(text=value_text)
        if color:
            self.value_label.configure(text_color=color)
