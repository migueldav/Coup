from nicegui import ui
from app.services import sound

def build():
    ui.button(
        'Voltar',
        icon='sym_o_arrow_back',
        color='emerald-600',
        on_click=lambda: (ui.navigate.back(), sound.play("botao.mp3"))
    ).classes('text-white px-4 py-2 rounded-lg')
