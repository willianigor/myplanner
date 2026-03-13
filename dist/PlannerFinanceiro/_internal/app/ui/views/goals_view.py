import customtkinter as ctk

class GoalsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(self, text="Metas Financeiras", font=ctk.CTkFont(size=24, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
