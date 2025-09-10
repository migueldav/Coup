from nicegui import ui
from app.services import sound

def build():
    help_dialog = ui.dialog()
    with help_dialog, ui.card().classes('w-full max-w-3xl p-4 bg-gray-800'):
        ui.markdown("""
# Regras do Jogo Coup

**Você é chefe de uma família em uma cidade-estado italiana, tentando controlar a corte através de manipulação, blefe e suborno. Seu objetivo: destruir a influência das outras famílias — apenas uma sobreviverá.**

---

## Preparação
- Cada jogador recebe 2 cartas de influência.
- Cada jogador recebe 2 moedas visíveis.

---

## Influência & Eliminação
- Cartas viradas representam sua influência. Ao perder influência, vire uma carta para cima à sua escolha.  
- Jogadores sem influências são exilados e fora da partida.

---

## Como Jogar
- Turnos em sentido horário; cada jogador realiza uma ação obrigatoriamente.  
- Outros jogadores podem contestar ou bloquear a ação.

---

## Ações Gerais (sempre disponíveis)
| Ação | Descrição |
|------|-----------|
| **Renda** | +1 moeda do Tesouro |
| **Ajuda Externa** | +2 moedas (pode ser bloqueada pelo Duque) |
| **Golpe de Estado** | Obrigatória com 10+ moedas, pague 7 para eliminar uma influência de outro (sempre bem-sucedida) |

---

## Ações de Personagem (padrões)
- **Duque**: Taxar — +3 moedas  
- **Assassino**: Assassinar — custa 3 moedas, elimina influência (pode ser bloqueado pela Condessa)  
- **Capitão**: Extorquir — pegar até 2 moedas de outro (pode ser bloqueado por Embaixador, Inquisidor ou Capitão)  
- **Embaixador**: Trocar — pegue 2 cartas do baralho, escolha as que deseja manter e embaralhe as outras de volta

---

## Ações Contrárias (Para bloquear)
- **Duque** bloqueia Ajuda Externa  
- **Condessa** bloqueia Assassinato  
- **Embaixador / Inquisidor / Capitão** bloqueiam Extorsão

---

## Contestações
- Qualquer ação ou bloqueio pode ser contestado por outro jogador.  
- Se contestado, o jogador deve mostrar a carta correspondente; se falhar, perde uma influência.  
- Se tiver a carta, devolve ao baralho, embaralha, compra nova e o contestante perde influência.

🚨 *Perigo do "Assassinato Duplo"*:  
Contestar um assassinato e falhar pode levar à perda imediata de duas influências!

---

## Fim do Jogo
- O último jogador com influência vence.

---

**Boa diversão com Coup!**
""")
        
        ui.button(
            "Fechar",
            on_click=lambda: (sound.play("botao.mp3"), help_dialog.close())
        ).classes('mt-4')

    original_open = help_dialog.open

    def open_with_sound():
        sound.play("fab.mp3")
        original_open()

    return help_dialog, open_with_sound
