from card import Card
import  random

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.alive = True
        self.immune = False
        self.roulette = self._init_roulette()
        self.chamber_index = 0

    def _init_roulette(self):
        chambers = [False] * 2
        chambers.insert(random.randint(0, 2), True)
        return chambers

    def play_card(self):
        if not self.alive:
            print(f'{self.name} is dead and cannot play!')
            return None

        print(f"\n{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"{i + 1}: {card}")

        while True:
            try:
                choice = int(input(f"{self.name}, choose a card to play (1-{len(self.hand)}): "))
                if 1 <= choice <= len(self.hand):
                    selected = self.hand.pop(choice - 1)

                    if selected.is_joker:
                       if selected.joker_role == 'mysterious':
                          selected.choose_type_for_joker()
                       elif selected.joker_role == 'lucky':
                           print(f"🛡️ {self.name} used LUCKY Joker for immunity this round!")
                           self.immune = True

                    return selected
            except ValueError:
                pass
            print("Invalid input. Try again.")




    def spin_and_fire(self):
        if not self.alive:
            return

        print(f"\n{self.name} pulls the trigger...")

        if self.roulette[self.chamber_index]:
            print(f"☠️Boom! {self.name} is shot! It is eliminated.")
            self.alive = False
        else:
            print(f"😇 Oops! {self.name} survives this round!")

        self.chamber_index += 1



