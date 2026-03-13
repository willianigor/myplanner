import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from app.services.transaction_service import TransactionService

class ReportsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = TransactionService()
        self.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ctk.CTkLabel(self, text="Relatórios e Exportação", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=20, pady=20, anchor="w")

        # Frame de Exportação
        export_frame = ctk.CTkFrame(self)
        export_frame.pack(padx=20, pady=10, fill="x", expand=False)
        
        export_label = ctk.CTkLabel(export_frame, text="Exporte todas as suas transações para um arquivo local.", justify="left")
        export_label.pack(padx=15, pady=15, anchor="w")

        buttons_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
        buttons_frame.pack(padx=15, pady=(0, 15), anchor="w")

        csv_button = ctk.CTkButton(buttons_frame, text="Exportar para CSV", command=lambda: self._export_data('csv'))
        csv_button.pack(side="left", padx=(0, 10))

        excel_button = ctk.CTkButton(buttons_frame, text="Exportar para Excel", command=lambda: self._export_data('excel'))
        excel_button.pack(side="left")

    def _export_data(self, file_type: str):
        """Busca os dados e exporta para o formato especificado."""
        try:
            transactions = self.service.get_transactions(limit=99999) # Limite alto para pegar tudo
            if not transactions:
                messagebox.showinfo("Sem Dados", "Não há transações para exportar.", parent=self)
                return

            # Converter para DataFrame do Pandas
            data = [{
                "Descrição": t.description,
                "Valor": t.value,
                "Data": t.transaction_date.strftime('%Y-%m-%d'),
                "Tipo": t.transaction_type.value,
                "Categoria": t.category.name,
                "Conta": t.account.name,
                "Pago": t.is_paid,
                "Vencimento": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
                "Notas": t.notes
            } for t in transactions]
            df = pd.DataFrame(data)

            # Pedir ao usuário onde salvar o arquivo
            if file_type == 'csv':
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Salvar como CSV"
                )
                if file_path:
                    df.to_csv(file_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para:\n{file_path}", parent=self)

            elif file_type == 'excel':
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                    title="Salvar como Excel"
                )
                if file_path:
                    df.to_excel(file_path, index=False, sheet_name='Transações')
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para:\n{file_path}", parent=self)

        except Exception as e:
            messagebox.showerror("Erro na Exportação", f"Ocorreu um erro inesperado:\n{e}", parent=self)

