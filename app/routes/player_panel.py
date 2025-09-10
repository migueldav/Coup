from nicegui import ui
from app.services.game_service import COIN_IMG

def build(parent, game, local_index=0):
    parent.clear()
    names = getattr(game, 'player_names', [])
    if not names:
        return
    local_name = names[local_index]
    p = game.players[local_name]
    with parent:
        with ui.card().classes('w-64 p-4 bg-gray-800').style('z-index:40;'):
            ui.label('Suas Influências').classes('text-sm text-gray-300')
            with ui.row().classes('gap-2 mt-2'):
                if p.influences:
                    for inf in p.influences[:2]:
                        ui.label(inf).classes('text-sm font-semibold text-white')
                else:
                    ui.label('Sem influências visíveis').classes('text-sm text-gray-400')
            with ui.row().classes('items-center gap-2 mt-4'):
                ui.image(COIN_IMG).classes('w-6 h-6')
                ui.label(str(p.coins)).classes('text-lg text-white')
