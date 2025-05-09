class Card:
    """
    Represent a single card: scissors, rock, paper
    Joker card can be played as any type based on the user choice
    """
    def __init__(self, type: str, is_joker: bool = False):
        self.type = type
        self.is_joker = is_joker
        self.joker_role = None #lucky/dead/mysterious

    def choose_type_for_joker(self):
        if self.is_joker and self.joker_role == 'mysterious':
            while True:
                choice = input("JOKER CARD: Choose a type to play as (scissors/rock/paper):  ").strip().lower()
                if choice in ['scissors', 'rock', 'paper']:
                    self.type = choice
                    self.joker_role = None
                    break
                else:
                    print('Invalid input. Please enter scissors, rock, or paper')

    def __str__(self):
        """
        display the card information
        """
        if self.is_joker:
            if self.joker_role == 'deadly':
                return "JOKER(DEADLY)"
            elif self.joker_role == 'lucky':
                return "JOKER(LUCKY)"
            elif self.joker_role == 'mysterious':
                return f"JOKER({self.type}) [MYSTERIOUS]"
            else:
                return f"JOKER({self.type})"
        else:
            return self.type.upper()


    def __repr__(self):
        return  self.__str__()

