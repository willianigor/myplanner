import customtkinter as ctk
from app.services.report_service import ReportService
from app.ui.widgets.matplotlib_chart import MatplotlibChart
from app.ui.widgets.kpi_card import KPICard
from app.utils.formatters import format_currency
from app.ui.theme import Theme
from datetime import date

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.service = ReportService()

        # Layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=0) # Linha dos KPIs com peso 0
        self.grid_rowconfigure(1, weight=1) # Linha dos gráficos com peso 1

        # Widgets
        self._create_widgets()

    def _create_widgets(self):
        # --- Linha de KPIs ---
        self._create_summary_cards()

        # --- Linha de Gráficos ---
        self.pie_chart = MatplotlibChart(self)
        self.pie_chart.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")
        
        self.bar_chart = MatplotlibChart(self)
        self.bar_chart.grid(row=1, column=1, padx=(10, 20), pady=(10, 20), sticky="nsew")

    def _create_summary_cards(self):
        """Cria os cards de KPI usando o novo widget KPICard."""
        kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        kpi_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.balance_card = KPICard(kpi_frame, title="Saldo Total Atual")
        self.balance_card.grid(row=0, column=0, padx=10, sticky="ew")

        self.income_card = KPICard(kpi_frame, title="Receitas do Mês")
        self.income_card.grid(row=0, column=1, padx=10, sticky="ew")

        self.expense_card = KPICard(kpi_frame, title="Despesas do Mês")
        self.expense_card.grid(row=0, column=2, padx=10, sticky="ew")

    def on_show(self):
        """Atualiza todos os dados do dashboard quando a view é exibida."""
        self._update_summary_cards()
        self._update_pie_chart()
        self._update_bar_chart()

    def _update_summary_cards(self):
        total_balance = self.service.get_total_balance()
        month_summary = self.service.get_current_month_summary()
        
        self.balance_card.set_value(format_currency(total_balance))
        self.income_card.set_value(format_currency(month_summary.get("income", 0)), color=Theme.COLOR_SUCCESS)
        self.expense_card.set_value(format_currency(month_summary.get("expense", 0)), color=Theme.COLOR_ERROR)

    def _update_pie_chart(self):
        today = date.today()
        expenses_data = self.service.get_expenses_by_category(today.year, today.month)
        
        if not expenses_data:
            self.pie_chart.figure.clear()
            ax = self.pie_chart.figure.add_subplot(111)
            self.pie_chart._apply_theme_to_axes(ax) # Aplica tema mesmo para o texto
            ax.text(0.5, 0.5, "Sem dados de despesas para este mês", ha='center', va='center', color=Theme.COLOR_TEXT_SECONDARY, fontsize=12)
            self.pie_chart.canvas.draw()
            return

        labels = [item[0] for item in expenses_data]
        sizes = [item[1] for item in expenses_data]
        self.pie_chart.plot_pie_chart(labels, sizes, f"Despesas de {today.strftime('%B/%Y')}")

    def _update_bar_chart(self):
        trend_data = self.service.get_monthly_income_expense_trend()
        
        if not trend_data:
            self.bar_chart.figure.clear()
            ax = self.bar_chart.figure.add_subplot(111)
            self.bar_chart._apply_theme_to_axes(ax) # Aplica tema mesmo para o texto
            ax.text(0.5, 0.5, "Não há dados suficientes para o gráfico de tendência", ha='center', va='center', color=Theme.COLOR_TEXT_SECONDARY, fontsize=12)
            self.bar_chart.canvas.draw()
            return

        labels = list(trend_data.keys())
        incomes = [d['income'] for d in trend_data.values()]
        expenses = [d['expense'] for d in trend_data.values()]
        
        data_for_chart = { "Receitas": incomes, "Despesas": expenses }
        
        # Passando as cores do nosso tema para o gráfico de barras
        bar_colors = [Theme.COLOR_SUCCESS, Theme.COLOR_ERROR]
        
        self.bar_chart.plot_bar_chart(labels, data_for_chart, "Receitas vs. Despesas (Últimos 6 Meses)", colors=bar_colors)

