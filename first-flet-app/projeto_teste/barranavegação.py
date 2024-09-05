import flet as ft
from flet import padding, alignment

def main(page: ft.Page):
    h1_title = ft.Text(
        "PRODUÇÃO DE ESPÉCIE",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLACK
    )
    
    # Função para lidar com o clique em um item da barra lateral
    def on_option_click(e):
        option_text = e.control.text
        if option_text == "Calendário":
            content.value = "Conteúdo do Calendário"
        elif option_text == "Germinação":
            content.value = "Conteúdo da Germinação"
        elif option_text == "Mudas Produzidas":
            content.value = "Conteúdo das Mudas Produzidas"
        elif option_text == "Relatórios":
            content.value = "Conteúdo dos Relatórios"
        page.update()

    # Criando a barra lateral com opções
    sidebar = ft.Container(
        bgcolor=ft.colors.WHITE,
        width=200,
        height=page.window_height,
        padding=padding.only(top=10),
        alignment=alignment.center,
        content=ft.Column(
            [
                ft.ElevatedButton("Calendário", on_click=on_option_click, bgcolor=ft.colors.BLACK, color=ft.colors.WHITE),
                ft.ElevatedButton("Germinação", on_click=on_option_click, bgcolor=ft.colors.BLACK, color=ft.colors.WHITE),
                ft.ElevatedButton("Mudas Produzidas", on_click=on_option_click, bgcolor=ft.colors.BLACK, color=ft.colors.WHITE),
                ft.ElevatedButton("Relatórios", on_click=on_option_click, bgcolor=ft.colors.BLACK, color=ft.colors.WHITE)
                # Adicione mais opções conforme necessário
            ],
            horizontal_alignment='center',
            alignment='center'
        )
    )

    # Conteúdo principal
    content = ft.Text(
        "PRODUÇÃO DE ESPÉCIE",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLACK
    )

    # Adicionando a barra lateral e o conteúdo principal ao layout da página
    page.add(
        ft.Row(
            [
                sidebar,  # Barra lateral
                ft.VerticalDivider(width=1),  # Separador vertical
                ft.Container(
                    expand=True,
                    content=content  # Conteúdo principal da página
                ),
            ],
            expand=True,
        )
    )

# Executando o aplicativo
ft.app(target=main)
