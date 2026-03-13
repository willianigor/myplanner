import customtkinter as ctk

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(self, text="Configurações", font=ctk.CTkFont(size=24, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Exemplo de opção de tema
        self.theme_label = ctk.CTkLabel(self, text="Tema da Aplicação:")
        self.theme_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        self.theme_menu = ctk.CTkOptionMenu(self, values=["System", "Dark", "Light"],
                                             command=self.change_appearance_mode_event)
        self.theme_menu.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")
        self.theme_menu.set(ctk.get_appearance_mode())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Muda o tema da aplicação."""
        ctk.set_appearance_mode(new_appearance_mode)
