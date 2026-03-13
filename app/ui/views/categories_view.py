import customtkinter as ctk
from tkinter import messagebox
from app.services.category_service import CategoryService, TransactionType
from app.models.category import Category

class CategoriesView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = CategoryService()

        # Layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Título da View
        title_label = ctk.CTkLabel(self, text="Gestão de Categorias", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Frame de Receitas
        self.income_frame = self._create_category_frame(self, "Receitas", TransactionType.INCOME)
        self.income_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

        # Frame de Despesas
        self.expense_frame = self._create_category_frame(self, "Despesas", TransactionType.EXPENSE)
        self.expense_frame.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        
        self._load_all_categories()

    def _create_category_frame(self, master, title: str, trans_type: TransactionType):
        frame = ctk.CTkFrame(master)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(header_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, sticky="w")
        
        add_button = ctk.CTkButton(header_frame, text="Adicionar Nova", width=120, command=lambda: self._add_category(trans_type))
        add_button.grid(row=0, column=1, sticky="e")
        
        scrollable_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scrollable_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Guardar referência ao scrollable_frame para poder preenchê-lo depois
        setattr(self, f"{trans_type.value}_scrollable_frame", scrollable_frame)
        
        return frame

    def _load_all_categories(self):
        # Limpar frames
        for child in self.income_scrollable_frame.winfo_children():
            child.destroy()
        for child in self.expense_scrollable_frame.winfo_children():
            child.destroy()
            
        # Carregar categorias
        income_categories = self.service.get_categories_by_type(TransactionType.INCOME)
        expense_categories = self.service.get_categories_by_type(TransactionType.EXPENSE)

        for cat in income_categories:
            self._create_category_entry(self.income_scrollable_frame, cat)
        
        for cat in expense_categories:
            self._create_category_entry(self.expense_scrollable_frame, cat)

    def _create_category_entry(self, master, category: Category):
        entry_frame = ctk.CTkFrame(master)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(0, weight=1)

        name_label = ctk.CTkLabel(entry_frame, text=category.name, anchor="w")
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        edit_button = ctk.CTkButton(entry_frame, text="Editar", width=60, command=lambda c=category: self._edit_category(c))
        edit_button.grid(row=0, column=1, padx=5, pady=5)

        delete_button = ctk.CTkButton(entry_frame, text="Excluir", width=60, fg_color=("#F44336", "#C62828"), hover_color=("#E53935", "#B71C1C"), command=lambda c=category: self._delete_category(c))
        delete_button.grid(row=0, column=2, padx=(0, 10), pady=5)

    def _add_category(self, trans_type: TransactionType):
        dialog = ctk.CTkInputDialog(text=f"Digite o nome da nova categoria de {trans_type.value}:", title="Adicionar Categoria")
        new_name = dialog.get_input()

        if new_name:
            try:
                self.service.create_category(name=new_name, transaction_type=trans_type)
                messagebox.showinfo("Sucesso", "Categoria adicionada com sucesso!")
                self._load_all_categories()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e))

    def _edit_category(self, category: Category):
        dialog = ctk.CTkInputDialog(text=f"Editando a categoria '{category.name}'.\nDigite o novo nome:", title="Editar Categoria")
        new_name = dialog.get_input()

        if new_name:
            try:
                self.service.update_category(category_id=category.id, name=new_name, transaction_type=category.transaction_type)
                messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
                self._load_all_categories()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e))

    def _delete_category(self, category: Category):
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a categoria '{category.name}'?\nEsta ação não pode ser desfeita."):
            try:
                self.service.delete_category(category_id=category.id)
                messagebox.showinfo("Sucesso", "Categoria excluída com sucesso!")
                self._load_all_categories()
            except ValueError as e:
                messagebox.showerror("Erro ao Excluir", str(e))
            except Exception as e:
                messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro inesperado: {e}")
