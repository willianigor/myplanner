import tkinter

# --- PATCH DE COMPATIBILIDADE PYTHON 3.14 ---
# Corrige erro "_tkinter.TclError: bad screen distance" causado
# por floats sendo passados para o Canvas no Python 3.14/Tcl mais novo.
_original_canvas_init = tkinter.Canvas.__init__
def _patched_canvas_init(self, master=None, cnf={}, **kw):
    for key in ['width', 'height']:
        if key in kw and isinstance(kw[key], float):
            kw[key] = int(kw[key])
        if cnf and key in cnf and isinstance(cnf[key], float):
            cnf[key] = int(cnf[key])
    _original_canvas_init(self, master, cnf, **kw)
tkinter.Canvas.__init__ = _patched_canvas_init

_original_misc_configure = tkinter.Misc.configure
def _patched_misc_configure(self, cnf=None, **kw):
    for key in ['width', 'height']:
        if key in kw and isinstance(kw[key], float):
            kw[key] = int(kw[key])
        if isinstance(cnf, dict) and key in cnf and isinstance(cnf[key], float):
            cnf[key] = int(cnf[key])
    return _original_misc_configure(self, cnf, **kw)
tkinter.Misc.configure = _patched_misc_configure
tkinter.Canvas.configure = _patched_misc_configure
# --------------------------------------------

from app.ui.main_window import MainWindow
from app.core.database import init_db
from app.utils.formatters import setup_locale
from app.services.category_service import CategoryService
from app.services.account_service import AccountService
from app.ui.theme import apply_theme

def main():
    """Função principal para iniciar a aplicação."""
    # 1. Aplica o tema visual da aplicação
    apply_theme()

    # 2. Configura o locale para formatação de moeda e datas
    setup_locale()

    # 3. Inicializa o banco de dados (cria tabelas se não existirem)
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados pronto.")
    
    # 4. Popula com dados iniciais se necessário
    print("Verificando dados iniciais...")
    CategoryService().get_or_create_initial_categories()
    AccountService().get_or_create_initial_accounts()
    print("Dados iniciais prontos.")

    # 5. Inicia a aplicação de interface gráfica
    app = MainWindow()
    app.create_widgets() # Cria os widgets após a inicialização
    app.mainloop()

if __name__ == "__main__":
    main()
