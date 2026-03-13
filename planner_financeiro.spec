# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

# Adiciona o diretório raiz ao path para garantir que as importações funcionem
block_cipher = None
sys.path.append(str(Path.cwd()))

# --- Coleta de Arquivos de Dados ---
# Coleta os arquivos de dados do customtkinter e matplotlib
datas = collect_data_files('customtkinter')
datas += collect_data_files('matplotlib')

# Adiciona a pasta 'app' inteira como dados. Isso preserva a estrutura
# de pastas (app/data, app/ui, etc.), o que é crucial para nosso
# resource_path funcionar corretamente.
datas += [('app', 'app')]


# --- Análise e Configuração Principal ---
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'customtkinter',
        'matplotlib',
        'pandas',
        'sqlalchemy.dialects.sqlite'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- Configuração do Executável ---
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PlannerFinanceiro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # False para app de janela (sem terminal)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None # Você pode adicionar um caminho para um arquivo .ico aqui
)

# --- Coleta de Binários e DLLs ---
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PlannerFinanceiro',
)
