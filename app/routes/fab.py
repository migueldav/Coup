from nicegui import ui
from app.components import help
from app.services import sound, wallpaper

def build():
    def toggle_mute():
        muted = sound.toggle_mute()
        volume_button.props('icon=volume_off' if muted else 'icon=volume_up')
    
    def update_volume_icon(muted=None):
        state = muted if muted is not None else sound.is_muted()
        volume_button.props('icon=volume_off' if state else 'icon=volume_up')

    wallpaper.init()
    sound.init()
    ui.on('sound:init', update_volume_icon)
    hd, open_help = help.build()

    with ui.column().classes('absolute bottom-4 left-4'):
        with ui.fab('sym_o_chevron_right', color='emerald-600', direction='right'):
            ui.fab_action('wallpaper', color='emerald-600', on_click=lambda: (wallpaper.next(), sound.play("fab.mp3")), auto_close=False)
            volume_button = ui.fab_action('volume_up', color='emerald-600', on_click=toggle_mute, auto_close=False)
            update_volume_icon()
            ui.fab_action('help', color='emerald-600', on_click=open_help, auto_close=False)
