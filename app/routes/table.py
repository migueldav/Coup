import math
from nicegui import ui
from app.services.game_service import make_player_state
from app.components import player_card

def render_table(container, game, append_log):
    container.clear()
    names = getattr(game, 'player_names', [])
    n = len(names) or 1

    if n <= 6:
        wrapper_width = '70vw'; wrapper_height = '45vh'; container_width_px = 800
    elif n <= 8:
        wrapper_width = '62vw'; wrapper_height = '38vh'; container_width_px = 680
    elif n == 9:
        wrapper_width = '58vw'; wrapper_height = '34vh'; container_width_px = 660
    else:
        wrapper_width = '48vw'; wrapper_height = '28vh'; container_width_px = 600

    with container:
        ui.html(f'<div id="table-wrapper" style="position:relative;width:{wrapper_width};height:{wrapper_height};max-width:{container_width_px}px;margin:3rem auto 0;"></div>')

    base_radius_pct = 20
    if n == 10:
        base_radius_pct = 14
    elif n == 9:
        base_radius_pct = 19

    threshold = 4
    if n < 7:
        per_extra_spacing_px = 18
    elif n <= 8:
        per_extra_spacing_px = 10
    elif n == 9:
        per_extra_spacing_px = 9
    else:
        per_extra_spacing_px = 7

    if n <= 4:
        card_class, card_h_class = 'w-48', 'h-36'
    elif n <= 6:
        card_class, card_h_class = 'w-44', 'h-32'
    elif n <= 8:
        card_class, card_h_class = 'w-40', 'h-32'
    elif n == 9:
        card_class, card_h_class = 'w-36', 'h-30'
    else:
        card_class, card_h_class = 'w-32', 'h-28'

    card_px_map = {'w-48': 192, 'w-44': 176, 'w-40': 160, 'w-36': 144, 'w-32': 128}
    card_w_px = card_px_map.get(card_class, 160)

    max_radius_px = (container_width_px / 2) - (card_w_px / 2) - 12
    base_radius_px = (base_radius_pct / 100.0) * container_width_px

    extra = max(0, n - threshold)
    extra_delta_px = 0.0
    if extra > 0:
        delta_angle = 2 * math.pi / n
        extra_delta_px = extra * (per_extra_spacing_px / (delta_angle if delta_angle != 0 else 1))

    desired_radius_px = base_radius_px + extra_delta_px
    if desired_radius_px > max_radius_px:
        desired_radius_px = max_radius_px

    radius_pct = (desired_radius_px / container_width_px) * 100

    vertical_factor = 0.85 + 0.03 * max(0, n - 4)
    vertical_factor = min(vertical_factor, 1.3)
    radius_pct_y = radius_pct * vertical_factor

    start_angle = 3 * math.pi / 2
    vertical_offset = -3 if n < 10 else -5

    for i, name in enumerate(names):
        angle = start_angle + (2 * math.pi * i / n)
        cosv, sinv = math.cos(angle), math.sin(angle)
        left_pct = 50 + cosv * radius_pct
        top_pct = 50 + sinv * radius_pct_y + vertical_offset
        st = make_player_state(game, name)
        player_card.build(container, name, st, left_pct, top_pct, card_class, card_h_class, n)

    if n >= 10:
        container.style("transform: scale(0.86); transform-origin: center;")
    elif n == 9:
        container.style("transform: scale(0.92); transform-origin: center;")
    else:
        container.style("")
