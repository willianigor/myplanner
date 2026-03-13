import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MatplotlibChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.figure = Figure(dpi=100)
        self.figure.set_facecolor("#f0f0f0") # Cor de fundo padrão do sistema
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        self._set_theme_colors()

    def _set_theme_colors(self):
        """Ajusta as cores do gráfico com base no tema do CTk."""
        is_dark = ctk.get_appearance_mode() == "Dark"
        
        bg_color = "#2b2b2b" if is_dark else "#ffffff"
        text_color = "white" if is_dark else "black"
        grid_color = "#404040" if is_dark else "#cccccc"

        self.figure.set_facecolor(bg_color)
        
        plt.rcParams.update({
            'text.color': text_color,
            'axes.labelcolor': text_color,
            'xtick.color': text_color,
            'ytick.color': text_color,
            'axes.edgecolor': text_color,
            'axes.facecolor': bg_color,
            'savefig.facecolor': bg_color,
        })
    
    def plot_pie_chart(self, labels: list, sizes: list, title: str):
        """Desenha um gráfico de pizza."""
        self._set_theme_colors()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'color': plt.rcParams['text.color']})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(title, color=plt.rcParams['text.color'])
        self.canvas.draw()

    def plot_bar_chart(self, x_labels: list, data: dict, title: str):
        """
        Desenha um gráfico de barras.
        'data' é um dicionário onde as chaves são as séries (ex: 'Receitas')
        e os valores são as listas de alturas das barras.
        """
        self._set_theme_colors()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        width = 0.35
        x = range(len(x_labels))
        
        i = 0
        for series_name, values in data.items():
            offset = width * i
            ax.bar([pos + offset for pos in x], values, width, label=series_name)
            i += 1
            
        ax.set_ylabel('Valor (R$)')
        ax.set_title(title)
        ax.set_xticks([pos + width / (len(data)) for pos in x])
        ax.set_xticklabels(x_labels)
        ax.legend()
        ax.yaxis.grid(True, color=plt.rcParams['axes.edgecolor'], linestyle='--', linewidth=0.5)

        self.figure.tight_layout()
        self.canvas.draw()
