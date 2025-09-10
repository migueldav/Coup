from nicegui import ui

def build(parent, game):
    parent.clear()
    names = getattr(game, 'player_names', [])
    current = None
    try:
        current = game.current_player()
    except Exception:
        current = None
    with parent:
        with ui.card().classes('w-48 p-2 bg-gray-800').style('z-index:40;'):
            ui.label('Ordem de Turnos').classes('text-sm text-gray-300')
            with ui.row().classes('items-start gap-4 mt-3'):
                ui.html('<div style="width:2px;height:140px;background:#374151;margin-right:6px"></div>')
                with ui.column().classes('gap-2'):
                    for n in names[:4]:
                        if n == current:
                            ui.label(n).classes('text-white font-bold')
                        else:
                            ui.label(n).classes('text-gray-400')
