import sys
import os
from pathlib import Path

def resource_path(relative_path: str) -> Path:
    """
    Retorna o caminho absoluto para um recurso, funcionando tanto em modo de
    desenvolvimento quanto empacotado com PyInstaller.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        # Se não estiver empacotado, o caminho base é o diretório raiz do projeto
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / relative_path
