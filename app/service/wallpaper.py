from nicegui import ui

_wallpapers = [
    {'type': 'color', 'value': '#121212'},
    {'type': 'image', 'value': '/static/img/wallpapers/1.png'},
]

_current = 0

def init():
    apply_background()

    def _sync_state(e):
        global _current
        idx = int(e.args.get('index', 0))
        if not (0 <= idx < len(_wallpapers)):
            idx = 0
        _current = idx
        apply_background()

    ui.on('wallpaper:init', _sync_state)
    ui.run_javascript("""
        const key = 'wallpaper';
        if (!localStorage.getItem(key)) localStorage.setItem(key, '0');
        getFrontend().send_event('wallpaper:init', {
            index: parseInt(localStorage.getItem(key))
        });
    """)

def apply_background():
    wp = _wallpapers[_current]
    if wp['type'] == 'color':
        ui.query('body').style(f'''
            background-color: {wp['value']};
            background-image: none;
        ''')
    else:
        ui.query('body').style(f'''
            background-image: url("{wp['value']}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        ''')

def next():
    global _current
    _current = (_current + 1) % len(_wallpapers)
    ui.run_javascript(f'localStorage.setItem("wallpaper", "{_current}");')
    apply_background()

def set(index: int):
    global _current
    if 0 <= index < len(_wallpapers):
        _current = index
        ui.run_javascript(f'localStorage.setItem("wallpaper", "{_current}");')
        apply_background()

def get_current_index() -> int:
    return _current
