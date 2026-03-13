import locale

def setup_locale():
    """
    Configura o locale para o padrão brasileiro para formatação de moeda.
    Tenta diferentes padrões para máxima compatibilidade entre sistemas.
    """
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
        except locale.Error:
            print("Aviso: Locale 'pt_BR.UTF-8' ou 'Portuguese_Brazil.1252' não encontrado. "
                  "A formatação de moeda pode não funcionar como esperado.")
            # Fallback para um padrão que pode não ser o ideal mas evita crashes
            locale.setlocale(locale.LC_ALL, '')

def format_currency(value: float) -> str:
    """
    Formata um valor float para uma string de moeda no padrão BRL (R$).
    Exemplo: 1234.56 -> R$ 1.234,56

    Args:
        value: O valor numérico a ser formatado.

    Returns:
        A string formatada como moeda.
    """
    if value is None:
        value = 0.0
    try:
        return locale.currency(value, grouping=True, symbol='R$')
    except (TypeError, ValueError):
        return "R$ 0,00"

# Configura o locale assim que o módulo é importado
setup_locale()
