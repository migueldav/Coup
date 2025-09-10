import uuid
from typing import Dict, Optional
from app.services.coup import CoupGame

CARD_IMG_PLACEHOLDER = '/static/img/cartas/carta.png'
COIN_IMG = '/static/img/moedas/2.png'

GAMES: Dict[str, CoupGame] = {}

def create_game(player_names: list[str]) -> str:
    lobby_id = str(uuid.uuid4())[:6]
    game = CoupGame(player_names=player_names)
    GAMES[lobby_id] = game
    return lobby_id

def get_game(lobby_id: str) -> Optional[CoupGame]:
    return GAMES.get(lobby_id)

def remove_game(lobby_id: str) -> None:
    GAMES.pop(lobby_id, None)

def make_player_state(game, name: str) -> dict:
    ps = game.players.get(name)
    if not ps:
        return {'name': name, 'coins': 0, 'influences': [], 'avatar': '/static/img/cartas/carta.png'}
    return {'name': ps.name, 'coins': ps.coins, 'influences': ps.influences, 'avatar': '/static/img/cartas/carta.png'}
