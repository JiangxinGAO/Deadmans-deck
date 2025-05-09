# 🃏 Deadman's Deck: Joker Trap Edition

A command-line card game that combines Rock-Paper-Scissors with Russian Roulette, enhanced by Joker card mechanics.  
Developed for the COMP9001 Final Project.

---

## 🎮 Game Description

Three players take turns drawing cards and playing Rock, Paper, or Scissors.  
However, the deck contains Jokers—cards with special roles that can grant immunity, cause instant death, or trigger combo attacks.

---

## ✂️ Normal Cards: Rock-Paper-Scissors Mechanics

In each round, all surviving players must choose one of the two cards in their hand to play.

- Rock beats Scissors  
- Scissors beats Paper  
- Paper beats Rock  
- If all three types appear → **Draw**
- If only one type appears → **Draw**
- Players with the **losing card type** (and not immune) must spin and pull the trigger

---

## 🃏 Joker Types

| Joker Type     | Effect |
|----------------|--------|
| **Deadly**     | Immediately triggers spin-and-fire → player may die |
| **Lucky**      | Grants immunity for the current round |
| **Mysterious** | Player chooses a type (rock/paper/scissors) when played |

---

## 💥 Combo Mechanic: Lucky + Deadly

If a player **holds both a Deadly and a Lucky Joker**, they **trigger a combo**:

- Instead of spinning, they **choose another player to shoot**
- Both Joker cards are discarded after combo
- Combo triggers:
  - **In the same round** (e.g., draw Deadly then Lucky)
  - **Across rounds** (e.g., save Lucky in round 1, draw Deadly in round 2)

---

## Game Rules Summary

1. Each round:
   - All players play a card from their hand
   - RPS logic determines the loser(s)
   - Losers (not immune) spin the revolver
2. After the round, each surviving player draws back to 2 cards
3. Game ends when only 1 player remains

---

## 🚀 How to Run

```bash
python main.py
