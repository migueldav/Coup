import os
from nicegui import ui

base_dir = os.path.dirname(__file__)
static_path = os.path.join(base_dir, 'static')
if os.path.isdir(static_path):
    from fastapi.staticfiles import StaticFiles
    from nicegui import app
    app.mount("/static", StaticFiles(directory=static_path), name="static")

_test_lobby_id = None

try:
    import app.services.game_service as game_service
    if hasattr(game_service, 'create_test_game'):
        try:
            _test_lobby_id = game_service.create_test_game(6)
        except Exception:
            _test_lobby_id = None
    if not _test_lobby_id and hasattr(game_service, 'create_game'):
        try:
            _test_lobby_id = game_service.create_game([f'Jogador {i+1}' for i in range(6)])
        except Exception:
            _test_lobby_id = None
except Exception:
    _test_lobby_id = None

if not _test_lobby_id:
    _test_lobby_id = 'test-lobby'

try:
    import app.routes.game
except Exception:
    try:
        import app.routes
    except Exception:
        pass

@ui.page('/')
def index():
    ui.navigate.to(f'/game/{_test_lobby_id}')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Coup - Game Layout', port=8000)
