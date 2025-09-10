from nicegui import ui

def build(parent, append_log):
    parent.clear()
    with parent:
        with ui.row().classes('justify-center'):
            with ui.card().classes('w-full max-w-3xl p-3 bg-gray-800').style('text-align:center;'):
                ui.label('Ações Disponíveis').classes('text-sm text-gray-300 text-center')
                with ui.row().classes('gap-3 mt-2 justify-center'):
                    ui.button('Renda', on_click=lambda: (append_log('Renda executada'), ui.notify('Renda'))).classes('bg-slate-600 text-white')
                    ui.button('Ajuda Externa', on_click=lambda: (append_log('Ajuda Externa'), ui.notify('Ajuda Externa'))).classes('bg-slate-600 text-white')
                    ui.button('Assassinar', on_click=lambda: (append_log('Assassinar'), ui.notify('Assassinar'))).classes('bg-slate-600 text-white')

    parent.style('position: absolute; bottom: 1rem; left: 50%; transform: translateX(-50%); z-index: 40;')
