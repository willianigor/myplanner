import customtkinter as ctk
from app.services.report_service import ReportService
from app.ui.widgets.matplotlib_chart import MatplotlibChart
from app.utils.formatters import format_currency
from datetime import date

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = ReportService()

        # Layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Widgets
        self._create_widgets()
        self.on_show() # Carga inicial

    def _create_widgets(self):
        # Frame de Resumo
        summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        summary_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self._create_summary_cards(summary_frame)

        # Gráfico de Pizza
        self.pie_chart_frame = ctk.CTkFrame(self)
        self.pie_chart_frame.grid(row=1, column=0, padx=(20,10), pady=10, sticky="nsew")
        self.pie_chart_frame.grid_rowconfigure(0, weight=1)
        self.pie_chart_frame.grid_columnconfigure(0, weight=1)
        self.pie_chart = MatplotlibChart(self.pie_chart_frame)
        self.pie_chart.pack(fill="both", expand=True, padx=10, pady=10)

        # Gráfico de Barras
        self.bar_chart_frame = ctk.CTkFrame(self)
        self.bar_chart_frame.grid(row=1, column=1, padx=(10,20), pady=10, sticky="nsew")
        self.bar_chart_frame.grid_rowconfigure(0, weight=1)
        self.bar_chart_frame.grid_columnconfigure(0, weight=1)
        self.bar_chart = MatplotlibChart(self.bar_chart_frame)
        self.bar_chart.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_summary_cards(self, master):
        # Card Saldo Atual
        balance_card = ctk.CTkFrame(master)
        balance_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        balance_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(balance_card, text="Saldo Atual", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,0))
        self.balance_label = ctk.CTkLabel(balance_card, text="R$ 0,00", font=ctk.CTkFont(size=22))
        self.balance_label.pack(pady=(0,10))

        # Card Receitas do Mês
        income_card = ctk.CTkFrame(master)
        income_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        income_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(income_card, text="Receitas do Mês", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,0))
        self.income_label = ctk.CTkLabel(income_card, text="R$ 0,00", font=ctk.CTkFont(size=22), text_color="green")
        self.income_label.pack(pady=(0,10))

        # Card Despesas do Mês
        expense_card = ctk.CTkFrame(master)
        expense_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        expense_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(expense_card, text="Despesas do Mês", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,0))
        self.expense_label = ctk.CTkLabel(expense_card, text="R$ 0,00", font=ctk.CTkFont(size=22), text_color="red")
        self.expense_label.pack(pady=(0,10))

    def on_show(self):
        """Atualiza todos os dados do dashboard quando a view é exibida."""
        self._update_summary_cards()
        self._update_pie_chart()
        self._update_bar_chart()

    def _update_summary_cards(self):
        total_balance = self.service.get_total_balance()
        month_summary = self.service.get_current_month_summary()
        self.balance_label.configure(text=format_currency(total_balance))
        self.income_label.configure(text=format_currency(month_summary.get("income", 0)))
        self.expense_label.configure(text=format_currency(month_summary.get("expense", 0)))

    def _update_pie_chart(self):
        today = date.today()
        expenses_data = self.service.get_expenses_by_category(today.year, today.month)
        
        if not expenses_data:
            self.pie_chart.figure.clear()
            ax = self.pie_chart.figure.add_subplot(111)
            ax.text(0.5, 0.5, "Sem dados de despesas para este mês", ha='center', va='center')
            self.pie_chart.canvas.draw()
            return

        labels = [item[0] for item in expenses_data]
        sizes = [item[1] for item in expenses_data]
        self.pie_chart.plot_pie_chart(labels, sizes, f"Despesas de {today.strftime('%B/%Y')}")

    def _update_bar_chart(self):
        trend_data = self.service.get_monthly_income_expense_trend()
        
        if not trend_data:
            return

        labels = list(trend_data.keys())
        incomes = [d['income'] for d in trend_data.values()]
        expenses = [d['expense'] for d in trend_data.values()]
        
        data_for_chart = {
            "Receitas": incomes,
            "Despesas": expenses
        }
        self.bar_chart.plot_bar_chart(labels, data_for_chart, "Receitas vs. Despesas (Últimos 6 Meses)")

