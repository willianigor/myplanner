import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
from app.ui.theme import Theme

class MatplotlibChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        # Paleta de cores para gráficos, alinhada com o tema
        self.CHART_COLORS = [
            Theme.COLOR_PRIMARY,    # Azul principal
            "#17A2B8",              # Ciano
            Theme.COLOR_WARNING,    # Âmbar
            "#6f42c1",              # Índigo
            "#E83E8C",              # Rosa/Magenta
            "#4A90E2",              # Azul secundário
        ]
        
    def _apply_theme_to_axes(self, ax):
        """Aplica o estilo do tema a um objeto de eixos (ax)."""
        ax.set_facecolor(Theme.COLOR_SURFACE)
        self.figure.set_facecolor(Theme.COLOR_SURFACE)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(Theme.COLOR_TEXT_SECONDARY)
        ax.spines['bottom'].set_color(Theme.COLOR_TEXT_SECONDARY)

        ax.tick_params(axis='x', colors=Theme.COLOR_TEXT_SECONDARY)
        ax.tick_params(axis='y', colors=Theme.COLOR_TEXT_SECONDARY)

        ax.title.set_color(Theme.COLOR_TEXT_PRIMARY)
        ax.xaxis.label.set_color(Theme.COLOR_TEXT_SECONDARY)
        ax.yaxis.label.set_color(Theme.COLOR_TEXT_SECONDARY)

    def plot_pie_chart(self, labels: list, sizes: list, title: str, colors: list = None):
        """Desenha um gráfico de pizza com cores do tema."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self._apply_theme_to_axes(ax)

        if colors is None:
            colors = self.CHART_COLORS

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'color': Theme.COLOR_TEXT_SECONDARY},
            wedgeprops={'edgecolor': Theme.COLOR_SURFACE, 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.axis('equal')
        ax.set_title(title, color=Theme.COLOR_TEXT_PRIMARY, pad=20, fontdict={'size': 16, 'weight': 'bold'})
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_bar_chart(self, x_labels: list, data: dict, title: str, colors: list = None):
        """Desenha um gráfico de barras com cores do tema."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self._apply_theme_to_axes(ax)
        
        if colors is None:
            # Para o caso comum de Receita vs Despesa, usar as cores semânticas
            if len(data) == 2 and ('Receitas' in data and 'Despesas' in data):
                 colors = [Theme.COLOR_PRIMARY, Theme.COLOR_ERROR]
            else:
                colors = self.CHART_COLORS

        width = 0.4
        x = range(len(x_labels))
        
        num_series = len(data)
        bar_width = width / num_series
        
        for i, (series_name, values) in enumerate(data.items()):
            # Calcula o deslocamento para centralizar as barras
            offset = bar_width * (i - (num_series - 1) / 2)
            ax.bar([pos + offset for pos in x], values, bar_width, label=series_name, color=colors[i % len(colors)])
            
        ax.set_ylabel('Valor (R$)', color=Theme.COLOR_TEXT_SECONDARY)
        ax.set_title(title, color=Theme.COLOR_TEXT_PRIMARY, pad=20, fontdict={'size': 16, 'weight': 'bold'})
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels)
        
        ax.legend(facecolor=Theme.COLOR_SURFACE, edgecolor=Theme.COLOR_SURFACE, labelcolor=Theme.COLOR_TEXT_SECONDARY)
        
        ax.yaxis.grid(True, color=Theme.COLOR_SECONDARY, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)

        self.figure.tight_layout()
        self.canvas.draw()
