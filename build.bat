@echo OFF
ECHO ======================================================
ECHO Preparando para construir o Planner Financeiro...
ECHO ======================================================

REM Verifica se a pasta do ambiente virtual existe
IF EXIST venv (
    ECHO --- Ativando ambiente virtual ---
    CALL venv\Scripts\activate.bat
) ELSE (
    ECHO --- Ambiente virtual 'venv' nao encontrado. Usando Python do sistema. ---
)

ECHO.
ECHO --- Verificando versao do Python ---
python --version

ECHO.
ECHO --- Instalando/Atualizando dependencias ---
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO #############################################
    ECHO # ERRO: Falha ao instalar as dependencias.  #
    ECHO # Abortando o build.                        #
    ECHO #############################################
    GOTO:EOF
)

ECHO.
ECHO --- Limpando builds anteriores (pastas build e dist) ---
IF EXIST build (
    rmdir /s /q build
)
IF EXIST dist (
    rmdir /s /q dist
)

ECHO.
ECHO --- Executando PyInstaller ---
pyinstaller planner_financeiro.spec
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO #############################################
    ECHO # ERRO: Falha no PyInstaller.               #
    ECHO # Verifique os logs acima para detalhes.    #
    ECHO #############################################
    GOTO:EOF
)


ECHO.
ECHO ======================================================
ECHO Build concluido com sucesso!
ECHO. 
ECHO O executavel esta em:
ECHO dist\PlannerFinanceiro
ECHO ======================================================

:EOF
PAUSE
