from nicegui import ui, app

_muted = False

def init():
    @app.on_connect
    def _init_sound(socket_id: str):
        ui.run_javascript("""
            if (!localStorage.getItem("mute")) {
                localStorage.setItem("mute", "false");
            }
            getFrontend().send_event("sound:init", {
                muted: localStorage.getItem("mute") === "true"
            });
        """)

    def _sync_state(e):
        global _muted
        _muted = e.args['muted']

    ui.on('sound:init', _sync_state)

def play(sound_file: str):
    if _muted:
        return
    ui.run_javascript(f"""
        if (!window.sounds) window.sounds = {{}};
        if (!window.sounds["{sound_file}"]) {{
            window.sounds["{sound_file}"] = new Audio("/static/sounds/{sound_file}");
        }}
        window.sounds["{sound_file}"].currentTime = 0;
        window.sounds["{sound_file}"].play();
    """)

def toggle_mute():
    global _muted
    _muted = not _muted
    ui.run_javascript(f'localStorage.setItem("mute", "{str(_muted).lower()}");')
    return _muted

def is_muted() -> bool:
    return _muted
