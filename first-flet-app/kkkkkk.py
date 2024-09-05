import flet as ft
import sqlite3
    
# Função para criar o banco de dados e a tabela, se não existir
def create_database():
    conn = sqlite3.connect('plantas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plantas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_comum TEXT NOT NULL,
            nome_cientifico TEXT NOT NULL,
            recipiente_tubete TEXT CHECK(recipiente_tubete IN ('sim', 'não')) NOT NULL,
            tamanho TEXT NOT NULL,
            lote TEXT NOT NULL,
            qtd_semeada INTEGER NOT NULL,
            qtd_prod INTEGER NOT NULL,
            data_semeio DATE NOT NULL,
            data_lembrete DATE,
            data_germinacao DATE,
            procedencia TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def main(page: ft.Page):

    # Chama a função para criar o banco de dados e a tabela
    create_database()

    # Função para salvar a planta no banco de dados
    def salvar_planta(e):
        # Coletar os dados do formulário
        nome_comum = input_nome_comum.value
        nome_cientifico = input_nome_cientifico.value
        recipiente_tubete = dropdown_recipiente.value
        tamanho = input_tamanho.value
        lote = input_lote.value
        qtd_semeada = int(input_qtd_semeada.value)
        qtd_prod = int(input_qtd_prod.value)
        data_semeio = input_data_semeio.value
        data_lembrete = input_data_lembrete.value
        data_germinacao = input_data_germinacao.value
        procedencia = input_procedencia.value

        # Inserir os dados no banco de dados
        conn = sqlite3.connect('plantas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO plantas (nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote, qtd_semeada, qtd_prod, data_semeio, data_lembrete, data_germinacao, procedencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote, qtd_semeada, qtd_prod, data_semeio, data_lembrete, data_germinacao, procedencia))
        conn.commit()
        conn.close()

        # Exibir uma mensagem de sucesso
        page.dialog = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text("Planta salva com sucesso!"),
        )
        page.dialog.open = True
        page.update()

    def exibir_dados(e):
        # Conectar ao banco de dados e buscar os dados
        conn = sqlite3.connect('plantas.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plantas')
        rows = cursor.fetchall()
        conn.close()

        # Criar uma nova página para exibir os dados
        def dados_page(page: ft.Page):
            # Criar as linhas da tabela
            table_rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0]))),
                        ft.DataCell(ft.Text(row[1])),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                        ft.DataCell(ft.Text(row[4])),
                        ft.DataCell(ft.Text(str(row[5]))),
                        ft.DataCell(ft.Text(str(row[6]))),
                        ft.DataCell(ft.Text(row[7])),
                        ft.DataCell(ft.Text(row[8])),
                        ft.DataCell(ft.Text(row[9])),
                        ft.DataCell(ft.Text(row[10]))
                    ]
                ) for row in rows
            ]

            # Criar a tabela com os dados
            tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nome Comum")),
                    ft.DataColumn(ft.Text("Nome Científico")),
                    ft.DataColumn(ft.Text("Recipiente Tubete")),
                    ft.DataColumn(ft.Text("Tamanho")),
                    ft.DataColumn(ft.Text("Lote")),
                    ft.DataColumn(ft.Text("Qtd. Semeada")),
                    ft.DataColumn(ft.Text("Qtd. Produzida")),
                    ft.DataColumn(ft.Text("Data de Semeio")),
                    ft.DataColumn(ft.Text("Data de Lembrete")),
                    ft.DataColumn(ft.Text("Data de Germinação")),
                    ft.DataColumn(ft.Text("Procedência")),
                ],
                rows=table_rows,
            )

            # Adicionar a tabela à nova página
            page.add(
                ft.Column(
                    controls=[
                        tabela,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go('/main'))
                    ]
                )
            )
            page.update()

        # Navegar para a nova página de dados
        page.go('/dados', dados_page)

    # Inputs do formulário
    input_nome_comum = ft.TextField(label="Nome Comum")
    input_nome_cientifico = ft.TextField(label="Nome Científico")
    dropdown_recipiente = ft.Dropdown(label="Recipiente Tubete", options=[ft.dropdown.Option("sim"), ft.dropdown.Option("não")])
    input_tamanho = ft.TextField(label="Tamanho")
    input_lote = ft.TextField(label="Lote")
    input_qtd_semeada = ft.TextField(label="Quantidade Semeada", keyboard_type=ft.KeyboardType.NUMBER)
    input_qtd_prod = ft.TextField(label="Quantidade Produzida", keyboard_type=ft.KeyboardType.NUMBER)
    input_data_semeio = ft.TextField(label="Data de Semeio", hint_text="AAAA-MM-DD")
    input_data_lembrete = ft.TextField(label="Data de Lembrete", hint_text="AAAA-MM-DD")
    input_data_germinacao = ft.TextField(label="Data de Germinação", hint_text="AAAA-MM-DD")
    input_procedencia = ft.TextField(label="Procedência")

    # Botão para salvar a planta
    btn_salvar = ft.ElevatedButton("Salvar", on_click=salvar_planta)

    # Botão para exibir os dados
    btn_exibir = ft.ElevatedButton("Exibir Dados", on_click=exibir_dados)

    # Adicionar tudo à página principal com rolagem
    page.add(
        ft.ListView(
            controls=[
                input_nome_comum,
                input_nome_cientifico,
                dropdown_recipiente,
                input_tamanho,
                input_lote,
                input_qtd_semeada,
                input_qtd_prod,
                input_data_semeio,
                input_data_lembrete,
                input_data_germinacao,
                input_procedencia,
                btn_salvar,
                btn_exibir,
            ],
            expand=True,
        )
    )

    # Inicializa a navegação para a página principal
    page.go('/main')

# Inicializa o aplicativo Flet
ft.app(target=main)
