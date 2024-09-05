import flet as ft
from flet import *
from datetime import datetime
import sqlite3

def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_maximized = True
    page.window_resizable = True

    # Função para navegar entre páginas
    def navegar_para_pagina(page_name):
        if page_name == "Germinação":
            page.controls.clear()
            page.add(especie_prod)
        elif page_name == "Adicionar Espécie":
            page.controls.clear()
            page.add(adicionar_especie_form)
        elif page_name == "Calendário":
            page.controls.clear()
            page.add(calendario)
        elif page_name == "Visualizar Espécies":
            page.controls.clear()
            page.add(visualizar_especies_page())

    # Funções de Login e Registro
    def logar(e):
        page.remove(registro)
        page.add(login)
        page.update()

    def registrar(e):
        page.remove(login)
        page.add(registro)
        page.update()

    def abrir_segunda_tela(e):
        page.remove(login)
        page.add(segundo_tela)
        page.update()

    def validar_login(e):
        if username_input.value == "user" and password_input.value == "pass":
            abrir_segunda_tela(e)
        else:
            error_message.value = "Usuário ou senha inválidos"
            page.update()

    # Função para adicionar espécie ao banco de dados
    def adicionar_especie(e):
        try:
            # Conectando ao banco de dados
            conn = sqlite3.connect('plantass.db')
            cursor = conn.cursor()

            # Criar a tabela se não existir
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

            # Inserir dados na tabela
            cursor.execute('''
                INSERT INTO plantas (
                    nome_comum, nome_cientifico, recipiente_tubete, tamanho, lote, data_semeio, data_lembrete, data_germinacao, procedencia
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nome_comum_input.value,
                nome_cientifico_input.value,
                recipiente_tubete_input.value,
                tamanho_input.value,
                lote_input.value,
                data_semeio_input.value,
                data_lembrete_input.value,
                data_germinacao_input.value,
                procedencia_input.value
            ))

            conn.commit()
        except sqlite3.Error as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao acessar o banco de dados: {e}"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
        finally:
            if 'conn' in locals() and conn:
                conn.close()

        # Limpar campos do formulário
        nome_comum_input.value = ""
        nome_cientifico_input.value = ""
        recipiente_tubete_input.value = ""
        tamanho_input.value = ""
        lote_input.value = ""
        data_semeio_input.value = ""
        data_lembrete_input.value = ""
        data_germinacao_input.value = ""
        procedencia_input.value = ""

        # Mostrar mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Espécie adicionada com sucesso!"), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    # Função para buscar dados do banco de dados
    def get_plantas():
        try:
            conn = sqlite3.connect('plantass.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM plantas")
            plantas = cursor.fetchall()
            return plantas
        except sqlite3.Error as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao acessar o banco de dados: {e}"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    # Função para criar a tabela de exibição
    def criar_tabela(plantass):
        
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome Comum")),
            ft.DataColumn(ft.Text("Nome Científico")),
            ft.DataColumn(ft.Text("Recipiente Tubete")),
            ft.DataColumn(ft.Text("Tamanho")),
            ft.DataColumn(ft.Text("Lote")),
            ft.DataColumn(ft.Text("Data Semeio")),
            ft.DataColumn(ft.Text("Data Lembrete")),
            ft.DataColumn(ft.Text("Data Germinação")),
            ft.DataColumn(ft.Text("Procedência"))
        ]
        rows = []
        for planta in plantass:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(planta[0]))),
                ft.DataCell(ft.Text(planta[1])),
                ft.DataCell(ft.Text(planta[2])),
                ft.DataCell(ft.Text(planta[3])),
                ft.DataCell(ft.Text(planta[4])),
                ft.DataCell(ft.Text(planta[5])),
                ft.DataCell(ft.Text(planta[6])),
                ft.DataCell(ft.Text(planta[7] if planta[7] else "")),
                ft.DataCell(ft.Text(planta[8] if planta[8] else "")),
                ft.DataCell(ft.Text(planta[9])),
            ]))
        tabela = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.colors.BLACK),
            column_spacing=20,
            data_row_height=40,
            # Opcional: adicionar paginação, ordenação, etc.
        )
        return tabela

    # Função para criar a página de visualização das espécies
    def visualizar_especies_page():
        plantas = get_plantas()
        tabela = criar_tabela(plantas)
        return ft.Column([
            ft.Row([
                ft.Text("Visualizar Espécies", size=30, weight="bold"),
                ft.Spacer(),
                ft.ElevatedButton("Voltar", on_click=lambda _: navegar_para_pagina("Germinação"))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(
                content=tabela,
                expand=True,
                padding=10,
                scroll=ft.ScrollMode.AUTO
            )
        ], alignment="start", expand=True)

    # Elementos do formulário de login
    username_input = ft.TextField(
        bgcolor=ft.colors.WHITE,
        hint_text='Digite seu usuário',
        width=300,
        height=40,
        border_radius=40,
        prefix_icon=ft.icons.PERSON,
        text_vertical_align=1,
        keyboard_type=ft.KeyboardType.NAME
    )

    password_input = ft.TextField(
        bgcolor=ft.colors.WHITE,
        hint_text='Digite sua senha',
        width=300,
        height=40,
        border_radius=40,
        prefix_icon=ft.icons.LOCK,
        text_vertical_align=1,
        password=True,
        can_reveal_password=True,
        keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD
    )

    error_message = ft.Text(value="", color=ft.colors.RED)

    login_button = ft.ElevatedButton(
        text='Login',
        bgcolor=ft.colors.LIGHT_BLUE_ACCENT,
        color=ft.colors.BLACK,
        on_hover=ft.colors.BLACK,
        width=300,
        height=40,
        on_click=validar_login
    )

    # Tela de login
    login = ft.Column([
        ft.Container(
            bgcolor=ft.colors.LIGHT_BLUE_ACCENT_100,
            width=page.window_width - 10,
            height=page.window_height - 60,
            border_radius=10,
            animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_IN_BACK),
            content=ft.Column([
                ft.Container(
                    bgcolor=ft.colors.BLACK,
                    width=400,
                    height=350,
                    border_radius=10,
                    content=ft.Column([
                        ft.Container(
                            padding=ft.padding.only(top=10, bottom=12),
                            content=ft.Column([
                                ft.Text(
                                    color=ft.colors.WHITE,
                                    value='Login',
                                    weight='bold',
                                    size=25
                                )
                            ])
                        ),
                        ft.Column([
                            username_input,
                            password_input,
                            login_button,
                            error_message,
                            ft.Row([
                                ft.TextButton('Recuperar conta'),
                                ft.TextButton('Criar nova conta', on_click=registrar)
                            ], width=300, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=8)
                    ], horizontal_alignment='center', alignment='center')
                )
            ], horizontal_alignment='center', alignment='center')
        ),
    ])

    # Tela de registro
    registro = ft.Column([
        ft.Container(
            bgcolor=ft.colors.LIGHT_BLUE_ACCENT_100,
            width=page.window_width - 10,
            height=page.window_height - 60,
            border_radius=10,
            content=ft.Column([
                ft.Container(
                    bgcolor=ft.colors.BLACK,
                    width=400,
                    height=450,
                    border_radius=10,
                    content=ft.Column([
                        ft.Container(
                            padding=ft.padding.only(top=10, bottom=12),
                            content=ft.Column([
                                ft.Text(
                                    color=ft.colors.WHITE,
                                    value='Registro',
                                    weight='bold',
                                    size=25
                                )
                            ])
                        ),
                        ft.Column([
                            ft.TextField(
                                bgcolor=ft.colors.WHITE,
                                hint_text='Digite seu usuário',
                                width=300,
                                height=40,
                                border_radius=40,
                                prefix_icon=ft.icons.PERSON,
                                text_vertical_align=1,
                                keyboard_type=ft.KeyboardType.NAME
                            ),
                            ft.TextField(
                                bgcolor=ft.colors.WHITE,
                                hint_text='Digite seu email',
                                width=300,
                                height=40,
                                border_radius=40,
                                prefix_icon=ft.icons.EMAIL,
                                text_vertical_align=1,
                                keyboard_type=ft.KeyboardType.EMAIL
                            ),
                            ft.TextField(
                                bgcolor=ft.colors.WHITE,
                                hint_text='Digite sua senha',
                                width=300,
                                height=40,
                                border_radius=40,
                                prefix_icon=ft.icons.LOCK,
                                text_vertical_align=1,
                                password=True,
                                can_reveal_password=True,
                                keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD
                            ),
                            ft.TextField(
                                bgcolor=ft.colors.WHITE,
                                hint_text='Confirme sua senha',
                                width=300,
                                height=40,
                                border_radius=40,
                                prefix_icon=ft.icons.LOCK,
                                text_vertical_align=1,
                                password=True,
                                can_reveal_password=True,
                                keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD
                            ),
                            ft.ElevatedButton(
                                text='Registrar',
                                bgcolor=ft.colors.LIGHT_BLUE_ACCENT,
                                color=ft.colors.BLACK,
                                on_hover=ft.colors.BLACK,
                                width=300,
                                height=40
                                # Adicionar handler para registro, se necessário
                            ),
                            ft.Row([
                                ft.TextButton('Recuperar conta'),
                                ft.TextButton('Já tenho uma conta', on_click=logar)
                            ], width=300, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=8)
                    ], horizontal_alignment='center', alignment='center')
                )
            ], horizontal_alignment='center', alignment='center')
        )
    ])

    # Elementos do formulário para adicionar espécie
    nome_comum_input = ft.TextField(
        hint_text="Nome comum",
        width=300,
        height=40
    )
    nome_cientifico_input = ft.TextField(
        hint_text="Nome científico",
        width=300,
        height=40
    )
    recipiente_tubete_input = ft.Dropdown(
        options=[ft.dropdown.Option("sim"), ft.dropdown.Option("não")],
        width=300,
        height=40,
        hint_text="Recipiente Tubete"
    )
    tamanho_input = ft.TextField(
        hint_text="Tamanho",
        width=300,
        height=40
    )
    lote_input = ft.TextField(
        hint_text="Lote",
        width=300,
        height=40
    )
    data_semeio_input = ft.TextField(
        hint_text="Data de semeio (YYYY-MM-DD)",
        width=300,
        height=40
    )
    data_lembrete_input = ft.TextField(
        hint_text="Data de lembrete (YYYY-MM-DD)",
        width=300,
        height=40
    )
    data_germinacao_input = ft.TextField(
        hint_text="Data de germinação (YYYY-MM-DD)",
        width=300,
        height=40
    )
    procedencia_input = ft.TextField(
        hint_text="Procedência",
        width=300,
        height=40
    )

    # Formulário para adicionar espécie
    adicionar_especie_form = ft.Column([
        ft.Container(
            width=page.window_width - 40,
            content=ft.Column([
                ft.Text("Adicionar Espécie", size=30, weight="bold"),
                nome_comum_input,
                nome_cientifico_input,
                recipiente_tubete_input,
                tamanho_input,
                lote_input,
                data_semeio_input,
                data_lembrete_input,
                data_germinacao_input,
                procedencia_input,
                ft.ElevatedButton("Adicionar", on_click=adicionar_especie, bgcolor=ft.colors.LIGHT_GREEN)
            ], spacing=15)
        )
    ], alignment="center", horizontal_alignment="center")

    # Página para visualização das espécies
    def visualizar_especies_page():
        plantas = get_plantas()
        tabela = criar_tabela(plantas)
        return ft.Column([
            ft.Row([
                ft.Text("Visualizar Espécies", size=30, weight="bold"),
                ft.Spacer(),
                ft.ElevatedButton("Voltar", on_click=lambda _: navegar_para_pagina("Germinação"))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(
                content=tabela,
                expand=True,
                padding=10,
                scroll=ft.ScrollMode.AUTO
            )
        ], alignment="start", expand=True)

    # Tela de produção de espécie
    especie_prod = ft.Column([
        ft.Container(
            bgcolor=ft.colors.WHITE,
            width=page.window_width,
            height=page.window_height,
            alignment=alignment.top_center,
            border_radius=10,
            content=ft.Column([
                ft.Container(
                    border_radius=10,
                    bgcolor=ft.colors.WHITE,
                    padding=padding.only(top=0),
                    alignment=alignment.center,
                    width=page.window_width,
                    height=page.window_height,
                    content=ft.Column([
                        ft.Text(
                            'PRODUÇÃO DE ESPÉCIE',
                            size=35,
                            weight='bold',
                            color=ft.colors.BLACK,
                        ),
                        ft.ElevatedButton("Adicionar Espécie", bgcolor=ft.colors.BLACK, width=200, height=100,
                                          on_click=lambda _: navegar_para_pagina("Adicionar Espécie"), color=ft.colors.WHITE),
                        ft.ElevatedButton("Visualizar Espécies", bgcolor=ft.colors.BLACK, width=200, height=100,
                                          on_click=lambda _: navegar_para_pagina("Visualizar Espécies"), color=ft.colors.WHITE),
                    ], horizontal_alignment=ft.alignment.top_right, alignment='center', spacing=20),
                ),
            ], horizontal_alignment='center', alignment='center')
        ),
        ft.ElevatedButton(
            text='Sei não',
            bgcolor=ft.colors.LIGHT_BLUE_ACCENT,
            color=ft.colors.BLACK,
            on_hover=ft.colors.BLACK,
            width=300,
            height=40,
        )
    ])

    # Placeholder para a página de calendário
    calendario = ft.Text("Calendário", size=30)

    # Tela secundária após login
    segundo_tela = ft.Column([
        ft.Container(
            bgcolor=ft.colors.LIGHT_BLUE_ACCENT_100,
            width=page.window_width - 10,
            height=page.window_height - 60,
            border_radius=10,
            animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_IN_BACK),
            content=ft.Column([
                ft.Container(
                    bgcolor=ft.colors.BLACK,
                    width=300,
                    height=400,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(
                            color=ft.colors.WHITE,
                            value='Selecione uma opção',
                            weight='bold',
                            size=25
                        ),
                        ft.ElevatedButton("Germinação", bgcolor=ft.colors.BLACK, width=200, height=100,
                                          on_click=lambda _: navegar_para_pagina("Germinação"), color=ft.colors.WHITE),
                        ft.ElevatedButton("Calendário", bgcolor=ft.colors.BLACK, width=200, height=100,
                                          on_click=lambda _: navegar_para_pagina("Calendário"), color=ft.colors.WHITE),
                        ft.ElevatedButton("Visualizar Espécies", bgcolor=ft.colors.BLACK, width=200, height=100,
                                          on_click=lambda _: navegar_para_pagina("Visualizar Espécies"), color=ft.colors.WHITE),
                    ], horizontal_alignment='center', alignment='center', spacing=10)
                )
            ], horizontal_alignment='center', alignment='center')
        )
    ])

    # Função para redimensionar controles
    def resize_controls(e):
        login.controls[0].width = page.window_width - 10
        login.controls[0].height = page.window_height - 60
        registro.controls[0].width = page.window_width - 10
        registro.controls[0].height = page.window_height - 60
        page.update()

    page.on_resize.subscribe(resize_controls)

    # Adicionar a tela de login inicialmente
    page.add(login)

ft.app(target=main)
