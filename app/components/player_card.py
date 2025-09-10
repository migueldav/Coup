from nicegui import ui
from app.services.game_service import CARD_IMG_PLACEHOLDER, COIN_IMG

def build(container, name, state, left_pct, top_pct, card_class, card_h_class, n):
    style = f'position:absolute; left:{left_pct:.2f}%; top:{top_pct:.2f}%; transform: translate(-50%, -50%); z-index:30;'
    with container:
        with ui.card().classes(f'{card_class} {card_h_class} relative bg-gray-700 p-2 flex flex-col justify-between h-full').style(style):
            with ui.row().classes('items-center justify-between'):
                ui.label(name).classes('text-xs font-semibold max-w-[140px] whitespace-nowrap').style('line-height:1;')
                ui.image(COIN_IMG).classes('w-5 h-5').style('flex-shrink:0;')

            infs = state.get('influences', [])[:2]
            mini_h = 'height:72px' if n < 10 else 'height:64px'
            mini_style = f'width:calc(45% - 8px);{mini_h};display:flex;align-items:center;justify-content:center;border-radius:6px;overflow:hidden;'
            with ui.row().classes('w-full gap-2 mt-2').style('justify-content:center; min-height:64px;'):
                if len(infs) == 0:
                    with ui.card().classes('p-0').style(mini_style).props('outlined elevation=0'):
                        ui.label('-').classes('text-sm text-gray-400')
                elif len(infs) == 1:
                    with ui.card().classes('p-0').style(mini_style).props('outlined elevation=0'):
                        ui.image(CARD_IMG_PLACEHOLDER).classes('w-full h-full').style('object-fit:cover;')
                else:
                    for inf in infs:
                        with ui.card().classes('p-0').style(mini_style).props('outlined elevation=0'):
                            ui.image(CARD_IMG_PLACEHOLDER).classes('w-full h-full').style('object-fit:cover;')

            with ui.row().classes('items-center justify-between mt-3'):
                ui.label(f'Influências: {len(state.get("influences", []))}').classes('text-sm text-gray-300')
                ui.button('Ação', on_click=lambda n=name: ui.notify(f'{n} executou Ação')).props('size=sm')
