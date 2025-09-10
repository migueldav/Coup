from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
import random

CHARACTERS = [
    "Duque",
    "Assassino",
    "Capitão",
    "Embaixador",
    "Condessa",
    "Inquisidor",
]

class Action:
    INCOME = "Renda (1 moeda)"
    FOREIGN_AID = "Ajuda externa (2 moedas)"
    TAX = "Imposto (Duque) (3 moedas)"
    STEAL = "Roubar (Capitão)"
    EXCHANGE = "Trocar (Embaixador)"
    ASSASSINATE = "Assassinar (Assassino) (-3 moedas do alvo)"
    COUP = "Golpe (7 moedas)"
    INQUISIT = "Investigar (Inquisidor)"

BLOCKS = {
    Action.FOREIGN_AID: ["Duque"],
    Action.STEAL: ["Capitão", "Embaixador", "Inquisidor"],
    Action.ASSASSINATE: ["Condessa"],
}

CLAIMS = {
    Action.TAX: "Duque",
    Action.STEAL: "Capitão",
    Action.EXCHANGE: "Embaixador",
    Action.ASSASSINATE: "Assassino",
    Action.INQUISIT: "Inquisidor",
}

@dataclass
class PlayerState:
    name: str
    coins: int = 2
    influences: List[str] = field(default_factory=list)
    def alive(self) -> bool:
        return len(self.influences) > 0

@dataclass
class GameError(Exception):
    message: str
    payload: Optional[dict] = None

@dataclass
class CoupGame:
    player_names: List[str]
    copies_per_card: int = 3
    deck: List[str] = field(default_factory=list)
    discard: List[str] = field(default_factory=list)
    players: Dict[str, PlayerState] = field(default_factory=dict)
    turn_index: int = 0
    log: List[str] = field(default_factory=list)
    winner: Optional[str] = None
    pending_losses: Dict[str, int] = field(default_factory=dict)

    def start(self) -> None:
        if len(self.player_names) < 2:
            raise GameError("É necessário pelo menos 2 jogadores.")
        self.deck = []
        for c in CHARACTERS:
            self.deck.extend([c] * self.copies_per_card)
        random.shuffle(self.deck)
        self.players = {name: PlayerState(name=name, coins=2, influences=[self.deck.pop(), self.deck.pop()]) for name in self.player_names}
        self.turn_index = 0
        self.log.clear()
        self.discard.clear()
        self.winner = None
        self.pending_losses.clear()
        self.add_log("Jogo iniciado.")

    def current_player(self) -> str:
        return self.player_names[self.turn_index]

    def alive_players(self) -> List[str]:
        return [p for p in self.player_names if self.players[p].alive()]

    def next_turn(self) -> None:
        if self.is_game_over():
            return
        n = len(self.player_names)
        for _ in range(n):
            self.turn_index = (self.turn_index + 1) % n
            if self.players[self.player_names[self.turn_index]].alive():
                break
        self.add_log(f"Agora é a vez de {self.current_player()}.")

    def is_game_over(self) -> bool:
        alive = [p for p in self.players.values() if p.alive()]
        if len(alive) == 1:
            self.winner = alive[0].name
            return True
        return False

    def add_log(self, entry: str) -> None:
        self.log.append(entry)

    def available_actions(self, player: str) -> List[Tuple[str, bool]]:
        ps = self.players[player]
        if not ps.alive():
            return []
        actions = [
            (Action.INCOME, True),
            (Action.FOREIGN_AID, True),
            (Action.TAX, True),
            (Action.STEAL, len(self.alive_players()) > 1),
            (Action.EXCHANGE, True),
            (Action.INQUISIT, len(self.alive_players()) > 1),
        ]
        actions.append((Action.ASSASSINATE, ps.coins >= 3 and len(self.alive_players()) > 1))
        must_coup = ps.coins >= 10
        actions.append((Action.COUP, ps.coins >= 7 and len(self.alive_players()) > 1))
        if must_coup:
            actions = [(Action.COUP, True)] + [a for a in actions if a[0] != Action.COUP]
        return actions

    def perform_action(self, actor: str, action: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
        if self.is_game_over():
            raise GameError("O jogo já terminou.")
        if actor != self.current_player():
            raise GameError("Não é o turno desse jogador.")
        if action == Action.COUP and self.players[actor].coins < 7:
            raise GameError("Moedas insuficientes para Golpe.")
        if action == Action.ASSASSINATE and self.players[actor].coins < 3:
            raise GameError("Moedas insuficientes para Assassinar.")
        if self.players[actor].coins >= 10 and action != Action.COUP:
            raise GameError("Com 10 ou mais moedas, o jogador deve usar 'Golpe (7 moedas)'.")
        needs_target = action in (Action.STEAL, Action.ASSASSINATE, Action.COUP, Action.INQUISIT)
        target = ctx.get("target")
        if needs_target:
            if not target or target == actor or not self.players[target].alive():
                raise GameError("Alvo inválido para a ação.")
        else:
            target = None
        claim_card = CLAIMS.get(action)
        if claim_card:
            if not self._resolve_claim_challenges(actor, claim_card, ctx):
                self._end_of_turn_cleanup()
                return {"ok": True, "action_resolved": True, "log": self.log}
        if action in BLOCKS:
            block_info = ctx.get("block", {"by": None, "card": None})
            blocker = block_info.get("by")
            block_card = block_info.get("card")
            if blocker:
                if blocker not in self.player_names or not self.players[blocker].alive():
                    raise GameError("Bloqueador inválido.")
                if action != Action.FOREIGN_AID and blocker != target:
                    raise GameError("Somente o alvo pode bloquear essa ação.")
                if block_card not in BLOCKS[action]:
                    raise GameError("Carta de bloqueio inválida para esta ação.")
                self.add_log(f"{blocker} declarou bloqueio usando {block_card}.")
                if not self._resolve_claim_challenges(blocker, block_card, ctx, key="block_challenges"):
                    blocker = None
                    self.add_log("Bloqueio falhou após contestação.")
            if blocker:
                self.add_log(f"Ação '{action}' foi bloqueada por {blocker}.")
                self._end_of_turn_cleanup()
                return {"ok": True, "action_resolved": True, "log": self.log}
        if action == Action.INCOME:
            self.players[actor].coins += 1
            self.add_log(f"{actor} recebeu 1 moeda (Renda).")
        elif action == Action.FOREIGN_AID:
            self.players[actor].coins += 2
            self.add_log(f"{actor} recebeu 2 moedas (Ajuda externa).")
        elif action == Action.TAX:
            self.players[actor].coins += 3
            self.add_log(f"{actor} recebeu 3 moedas (Imposto do Duque).")
        elif action == Action.STEAL:
            stolen = min(2, self.players[target].coins)
            self.players[target].coins -= stolen
            self.players[actor].coins += stolen
            self.add_log(f"{actor} roubou {stolen} moedas de {target}.")
        elif action == Action.EXCHANGE:
            new_cards = [self._draw(), self._draw()] + list(self.players[actor].influences)
            choice = ctx.get("exchange_choice")
            if not isinstance(choice, list) or len(choice) != 2:
                raise GameError("exchange_choice deve ser a lista de 2 índices escolhidos.")
            if any(i < 0 or i >= len(new_cards) for i in choice):
                raise GameError("Índices inválidos em exchange_choice.")
            final = [new_cards[i] for i in choice]
            not_picked = [c for i, c in enumerate(new_cards) if i not in choice]
            self.players[actor].influences = final
            self.deck.extend(not_picked)
            random.shuffle(self.deck)
            self.add_log(f"{actor} trocou cartas (Embaixador).")
        elif action == Action.ASSASSINATE:
            self.players[actor].coins -= 3
            self._queue_loss(target, 1)
            self.add_log(f"{actor} assassinou uma influência de {target}.")
        elif action == Action.COUP:
            self.players[actor].coins -= 7
            self._queue_loss(target, 1)
            self.add_log(f"{actor} deu um Golpe em {target}.")
        elif action == Action.INQUISIT:
            if not self.players[target].influences:
                self.add_log(f"{actor} tentou investigar {target}, mas ele não tem cartas.")
            else:
                seen = random.choice(self.players[target].influences)
                self.add_log(f"{actor} investigou {target} e viu uma carta.")
                if ctx.get("inquisit_swap"):
                    self.players[target].influences.remove(seen)
                    self.players[target].influences.append(self._draw())
                    self._return_to_deck(seen)
                    self.add_log(f"{actor} forçou {target} a trocar uma carta.")
        self._end_of_turn_cleanup()
        return {"ok": True, "action_resolved": True, "log": self.log}

    def _resolve_claim_challenges(self, claimer: str, claimed_card: str, ctx: Dict[str, Any], key: str = "challenges") -> bool:
        challenges = ctx.get(key, {})
        order = self._players_in_order(start_after=claimer)
        for challenger in order:
            if not self.players[challenger].alive():
                continue
            will_challenge = bool(challenges.get(challenger, False))
            if not will_challenge:
                continue
            self.add_log(f"{challenger} contestou {claimer} sobre {claimed_card}.")
            has_card = claimed_card in self.players[claimer].influences
            if has_card:
                self.players[claimer].influences.remove(claimed_card)
                new_card = self._draw()
                self.players[claimer].influences.append(new_card)
                self._return_to_deck(claimed_card)
                self.add_log(f"{claimer} provou que tinha {claimed_card}. {challenger} perde 1 influência.")
                self._queue_loss(challenger, 1)
                return True
            else:
                self.add_log(f"{claimer} foi desafiado e perdeu (não tinha {claimed_card}).")
                self._queue_loss(claimer, 1)
                return False
        return True

    def _players_in_order(self, start_after: str) -> List[str]:
        idx = self.player_names.index(start_after)
        order = []
        n = len(self.player_names)
        for i in range(1, n):
            p = self.player_names[(idx + i) % n]
            order.append(p)
        return order

    def _queue_loss(self, player: str, amount: int) -> None:
        if not self.players[player].alive():
            return
        self.pending_losses[player] = self.pending_losses.get(player, 0) + amount

    def apply_loss_choice(self, player: str, index: int) -> None:
        if self.pending_losses.get(player, 0) <= 0:
            raise GameError("Não há perdas pendentes para este jogador.")
        infs = self.players[player].influences
        if not (0 <= index < len(infs)):
            raise GameError("Índice de carta inválido para perda.")
        lost = infs.pop(index)
        self.discard.append(lost)
        self.pending_losses[player] -= 1
        self.add_log(f"{player} perdeu {lost}.")
        if self.pending_losses[player] == 0:
            del self.pending_losses[player]

    def _draw(self) -> str:
        if not self.deck:
            if not self.discard:
                raise GameError("Baralho vazio e sem descarte para reciclar.")
            self.deck = self.discard[:]
            self.discard.clear()
            random.shuffle(self.deck)
        return self.deck.pop()

    def _return_to_deck(self, card: str) -> None:
        self.deck.append(card)
        random.shuffle(self.deck)

    def _end_of_turn_cleanup(self) -> None:
        if not self.pending_losses:
            if not self.is_game_over():
                self.next_turn()

__all__ = ["CoupGame", "Action", "GameError", "PlayerState"]
