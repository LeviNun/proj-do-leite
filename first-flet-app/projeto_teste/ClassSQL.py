import flet as ft
import psycopg2
from functools import partial
import time
from datetime import datetime


def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_maximized = True
    page.window_resizable = True

    def connect_db():
        try:
            connection = psycopg2.connect(
                host="localhost",         # Endereço do servidor PostgreSQL
                database="BioFabrica", # Nome do banco de dados
                user="root",         # Usuário do banco de dados
                password=""  # Senha do banco de dados
            )
            return connection
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None

    def navegar_para_pagina(page_name):
        if page_name == "Espécie":
            page.controls.clear()
            page.add(especie_prod)
        elif page_name == "Calendário":
            page.controls.clear()
            page.add(calendario)

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
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                           (username_input.value, password_input.value))
            user = cursor.fetchone()
            if user:
                abrir_segunda_tela(e)
            else:
                error_message.value = "Usuário ou senha inválidos"
            connection.close()
        else:
            error_message.value = "Não foi possível conectar ao banco de dados"
        page.update()

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

    # Outras funções e telas seguem aqui...

    def resize_controls(e):
        login.controls[0].width = page.window_width - 10
        login.controls[0].height = page.window_height - 60
        registro.controls[0].width = page.window_width - 10
        registro.controls[0].height = page.window_height - 60
        page.update()

    page.on_resize.subscribe(resize_controls)

    page.add(login)


ft.app(target=main)
