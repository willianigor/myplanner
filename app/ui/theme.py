# app/ui/theme.py

import customtkinter as ctk

# Paleta de Cores Refinada - Inspirada em SaaS Premium (Tons Escuros Azulados)
class Theme:
    """
    Classe que centraliza as configurações de tema e a paleta de cores da aplicação.
    A paleta foi escolhida para transmitir profissionalismo, confiança e clareza.
    """
    # Cores Primárias e de Destaque
    COLOR_PRIMARY = "#3D82E3"  # Azul corporativo, para ações principais e destaque
    COLOR_SECONDARY = "#2C3E50" # Azul ardósia escuro, para elementos secundários
    
    # Cores de Fundo e Superfície
    COLOR_BACKGROUND = "#1B263B" # Fundo principal, azul-noite muito escuro
    COLOR_SURFACE = "#23314A"    # Cor de superfície para cards, inputs e áreas de conteúdo

    # Cores de Texto
    COLOR_TEXT_PRIMARY = "#F0F2F5"   # Branco suave para texto principal
    COLOR_TEXT_SECONDARY = "#A0AEC0" # Cinza azulado claro para texto secundário

    # Cores Semânticas
    COLOR_SUCCESS = "#28a745" # Verde para sucesso (mantido para semântica universal)
    COLOR_ERROR = "#E53E3E"   # Vermelho para erros
    COLOR_WARNING = "#DD6B20" # Laranja/Âmbar para alertas
    
    FONT_FAMILY = "Segoe UI"
    
def apply_theme():
    """Aplica o tema e a paleta de cores globais à aplicação CustomTkinter."""
    ctk.set_appearance_mode("Dark")
    
    # Define o tema de cores padrão para 'blue', que se alinha com a nossa
    # nova cor primária e garante que os componentes do CustomTkinter 
    # (como hover, checkboxes, etc.) usem uma cor base consistente.
    ctk.set_default_color_theme("blue") 
