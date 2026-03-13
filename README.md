# Planner Financeiro Desktop

![Banner](https://img.freepik.com/premium-vector/financial-dashboard-user-interface-design-template_7109-58.jpg)

**Planner Financeiro** é uma aplicação desktop completa para gestão de finanças pessoais, desenvolvida em Python com uma interface moderna e amigável. O objetivo é fornecer uma ferramenta visual, prática e inteligente para o controle financeiro do dia a dia.

Este projeto foi pensado para ser um produto real, robusto e fácil de usar, mesmo para usuários sem grande familiaridade com finanças ou tecnologia.

---

## ✨ Funcionalidades Principais

- **Dashboard Intuitivo:** Tenha uma visão geral da sua saúde financeira com cards de resumo e gráficos dinâmicos.
- **Gestão de Transações:** Adicione, edite, e exclua suas receitas e despesas de forma simples.
- **Contas e Categorias:** Organize suas finanças criando contas (banco, carteira) e categorias personalizadas.
- **Gráficos Visuais:** Acompanhe suas despesas por categoria com um gráfico de pizza e veja a evolução de suas receitas vs. despesas ao longo dos meses.
- **Relatórios e Exportação:** Exporte todos os seus dados para os formatos **CSV** e **Excel** para análises mais profundas.
- **Interface Moderna:** UI limpa, agradável e com suporte a tema claro e escuro, construída com CustomTkinter.
- **Persistência Local:** Todos os seus dados são salvos localmente em um banco de dados SQLite, garantindo privacidade e acesso offline.
- **Dados de Exemplo:** A aplicação gera dados iniciais na primeira execução para facilitar a demonstração e o entendimento das funcionalidades.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11 ou mais recente (compatível com 3.12, 3.13, 3.14+)
- **Interface Gráfica (UI):** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Banco de Dados:** SQLite
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (para mapeamento objeto-relacional seguro e robusto)
- **Gráficos:** [Matplotlib](https://matplotlib.org/)
- **Manipulação de Dados e Exportação:** [Pandas](https://pandas.pydata.org/) & [openpyxl](https://openpyxl.readthedocs.io/en/stable/)

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar o Planner Financeiro em sua máquina local.

### **Pré-requisitos**

- Python 3.11 ou a versão mais recente disponível instalada. Você pode baixar em [python.org](https://www.python.org/downloads/).

### **1. Clone o Repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd planner_financeiro
```

### **2. Crie um Ambiente Virtual (Recomendado)**

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### **3. Instale as Dependências**

Use o arquivo `requirements.txt` para instalar todas as bibliotecas necessárias.

```bash
pip install -r requirements.txt
```

### **4. Execute a Aplicação**

Com tudo instalado, basta executar o arquivo `main.py`.

```bash
python main.py
```

A aplicação será iniciada, e o banco de dados `planner.db` será criado automaticamente no diretório `app/data/` com algumas categorias e contas de exemplo.

---

## 📦 Gerando o Executável (.exe) para Windows

O projeto está configurado para ser facilmente empacotado em um executável para Windows usando o script `build.bat`.

1.  **Navegue até a pasta do projeto** pelo terminal.
2.  **Execute o script de build:**

    ```bash
    .\build.bat
    ```

3.  O script irá automaticamente instalar as dependências, executar o PyInstaller com as configurações corretas e criar a pasta `dist`.

4.  Ao final do processo, a aplicação completa estará na pasta `dist/PlannerFinanceiro`. Você pode copiar esta pasta para qualquer lugar e executar o `PlannerFinanceiro.exe` que está dentro dela.

---
*Este projeto foi desenvolvido como um portfólio de desenvolvimento de software, demonstrando boas práticas de arquitetura, design de UI/UX e implementação de funcionalidades complexas em Python.*
