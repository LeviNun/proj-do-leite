import flet as ft
import sqlite3

# Conectando ao banco de dados e criando a tabela, se ainda não existir
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
            
            data_semeio DATE NOT NULL,
            data_lembrete DATE,
            data_germinacao DATE,
            procedencia TEXT NOT NULL
        )
        ''')

    conn.commit()
    conn.close()

def main(page: ft.Page):

    # Criando o diálogo de sucesso
    dialog = ft.AlertDialog(
        title=ft.Text("Sucesso"),
        content=ft.Text("Planta salva com sucesso!"),
        on_dismiss=lambda e: print("Dialog foi fechado"),
    )

    def salvar_planta(e):
        # Coletar os dados do formulário
        nome_comum = input_nome_comum.value
        nome_cientifico = input_nome_cientifico.value
        recipiente_tubete = dropdown_recipiente.value
        tamanho = input_tamanho.value
        lote = input_lote.value
        
        data_semeio = input_data_semeio.value
        data_lembrete = input_data_lembrete.value
        data_germinacao = input_data_germinacao.value
        procedencia = input_procedencia.value

        # Inserir os dados no banco de dados
        conn = sqlite3.connect('plantas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO plantas (nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote,  data_semeio, data_lembrete, data_germinacao, procedencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote,   data_semeio, data_lembrete, data_germinacao, procedencia))
        conn.commit()
        conn.close()

        # Exibir o diálogo de sucesso
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Inputs do formulário
    input_nome_comum = ft.TextField(label="Nome Comum")
    input_nome_cientifico = ft.TextField(label="Nome Científico")
    dropdown_recipiente = ft.Dropdown(label="Recipiente Tubete", options=[ft.dropdown.Option("sim"), ft.dropdown.Option("não")])
    input_tamanho = ft.TextField(label="Tamanho")
    input_lote = ft.TextField(label="Lote")
   
    input_data_semeio = ft.TextField(label="Data de Semeio", hint_text="DD-MM-AAAA")
    input_data_lembrete = ft.TextField(label="Data de Lembrete", hint_text="DD-MM-AAAA")
    input_data_germinacao = ft.TextField(label="Data de Germinação", hint_text="DD-MM-AAAA")
    input_procedencia = ft.TextField(label="Procedência")

    # Botão para salvar a planta
    btn_salvar = ft.ElevatedButton("Salvar", on_click=salvar_planta)

    def salvar_planta(e):
        # Coletar os dados do formulário
        nome_comum = input_nome_comum.value
        nome_cientifico = input_nome_cientifico.value
        recipiente_tubete = dropdown_recipiente.value
        tamanho = input_tamanho.value
        lote = input_lote.value
        data_semeio = input_data_semeio.value
        data_lembrete = input_data_lembrete.value
        data_germinacao = input_data_germinacao.value
        procedencia = input_procedencia.value

        # Inserir os dados no banco de dados
        conn = sqlite3.connect('plantas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO plantas (nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote,  data_semeio, data_lembrete, data_germinacao, procedencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote, data_semeio, data_lembrete, data_germinacao, procedencia))
        conn.commit()
        conn.close()


    # Adicionar tudo à página
    page.add(
        input_nome_comum,
        input_nome_cientifico,
        dropdown_recipiente,
        input_tamanho,
        input_lote,
        
        input_data_semeio,
        input_data_lembrete,
        input_data_germinacao,
        input_procedencia,
        btn_salvar,
    )


    




# Inicializa o aplicativo Flet
ft.app(target=main)
