from player import Player
from card import Card
import random

class Game:
    def __init__(self):
        self.players = []
        for i in range(3):
            while True:
                name = input(f"Enter name for Player {i + 1}: ").strip()
                if not name:
                    print("Name cannot be empty. Try again.")
                    continue
                if any(p.name == name for p in self.players):
                    print("This name is already taken. Please choose a different name.")
                    continue
                break
            self.players.append(Player(name))

        self.deck = self._create_deck()
        self._assign_joker_roles()
        self.round_number =1

    # Creates and shuffles the full deck of 14 cards 随机生成牌
    def _create_deck(self):
        deck = [Card('scissors') for _ in range(4)] + \
               [Card('rock') for _ in range(4)] + \
               [Card('paper') for _ in range(4)] + \
               [Card('unknown', is_joker = True) for _ in range(3)]
        random.shuffle(deck)
        return deck

    def _assign_joker_roles(self):
        joker_cards = []
        for card in self.deck:
            if card.is_joker:
                joker_cards.append(card)
        random.shuffle(joker_cards)
        if len(joker_cards) >= 1:
            joker_cards[0].joker_role = 'deadly'
        if len(joker_cards) >= 2:
            joker_cards[1].joker_role = 'lucky'
        if len(joker_cards) >= 3:
            joker_cards[2].joker_role = 'mysterious'

    def _get_alive_players(self):
        alive = []
        for p in self.players:
            if p.alive:
                alive.append(p)
        return alive

    def _deal_cards(self, alive_players):
        MAX_HAND = 2
        random.shuffle(self.deck)

        for player in alive_players:
            card_index = 1

            while len(player.hand) < MAX_HAND and self.deck:
                card = self.deck.pop()

                # 显示抽牌信息
                if card.is_joker:
                    if card.joker_role == 'deadly':
                        print(f"🃏 {player.name} drew a Joker... and it's CURSED!")
                    elif card.joker_role == 'lucky':
                        print(f"🃏 {player.name} drew a Joker... and it's a BLESSING!")
                    elif card.joker_role == 'mysterious':
                        print(f"🃏 {player.name} drew a MYSTERIOUS Joker...It can be anything!")

                print(f"🃏 {player.name} drew card {card_index}: {card}")
                player.hand.append(card)
                card_index += 1

                # 插入 combo + deadly-only 判断（在 append 后立即判断）
                has_deadly = any(c.is_joker and c.joker_role == 'deadly' for c in player.hand)
                has_lucky = any(c.is_joker and c.joker_role == 'lucky' for c in player.hand)

                if has_deadly and has_lucky:
                    print(f"\n💀🛡️ {player.name} holds BOTH a DEADLY and a LUCKY Joker!")
                    print(f"{player.name}, choose a player to shoot:")

                    target_players = [p for p in self.players if p != player and p.alive]
                    for idx, tp in enumerate(target_players):
                        print(f"{idx + 1}. {tp.name}")

                    while True:
                        try:
                            choice = int(input("Enter number of the player to shoot: "))
                            if 1 <= choice <= len(target_players):
                                target = target_players[choice - 1]
                                print(f"🎯 {player.name} targets {target.name}!")
                                target.spin_and_fire()
                                break
                            else:
                                print("Invalid input.")
                        except ValueError:
                            print("Invalid input.")

                    # 丢弃 deadly 和 lucky Joker
                    player.hand = [c for c in player.hand if not (c.is_joker and c.joker_role in ['deadly', 'lucky'])]
                    continue  # 继续抽牌

                elif has_deadly and not has_lucky:
                    print(f"\n☠️ {player.name} holds only a DEADLY Joker... Time to pull the trigger.")
                    player.spin_and_fire()
                    player.hand = [c for c in player.hand if not (c.is_joker and c.joker_role == 'deadly')]
                    if not player.alive:
                        break
                    continue  # 生还继续抽

            print()

        print("🎴 Hands have been refreshed.")

    # def _deal_cards(self, alive_players):
    #     MAX_HAND = 2
    #     random.shuffle(self.deck)
    #
    #     for player in alive_players:
    #         card_index = 1
    #
    #         while len(player.hand) < MAX_HAND and self.deck:
    #             card = self.deck.pop()
    #
    #             # 显示抽牌信息
    #             if card.is_joker:
    #                 if card.joker_role == 'deadly':
    #                     print(f"🃏 {player.name} drew a Joker... and it's CURSED!")
    #                 elif card.joker_role == 'lucky':
    #                     print(f"🃏 {player.name} drew a Joker... and it's a BLESSING!")
    #                 elif card.joker_role == 'mysterious':
    #                     print(f"🃏 {player.name} drew a MYSTERIOUS Joker...It can be anything!")
    #
    #             print(f"🃏 {player.name} drew card {card_index}: {card}")
    #             player.hand.append(card)
    #             card_index += 1
    #
    #             # 玩家立即触发 deadly 效果
    #             if card.is_joker and card.joker_role == 'deadly':
    #                 player.spin_and_fire()
    #                 print()
    #                 if not player.alive:
    #                     player.hand = []
    #                     break  # 死亡则退出
    #                 # 生还 → 移除 deadly joker，避免末尾重复触发
    #                 player.hand = [c for c in player.hand if not (c.is_joker and c.joker_role == 'deadly')]
    #                 continue
    #
    #             # 玩家立即使用 lucky joker 时不 spin，但我们之后判断 combo
    #
    #             # 每次抽完牌后，立刻检查 combo / deadly-only
    #             has_deadly = any(c.is_joker and c.joker_role == 'deadly' for c in player.hand)
    #             has_lucky = any(c.is_joker and c.joker_role == 'lucky' for c in player.hand)
    #
    #             if has_deadly and has_lucky:
    #                 print(f"\n💀🛡️ {player.name} holds BOTH a DEADLY and a LUCKY Joker!")
    #                 print(f"{player.name}, choose a player to shoot:")
    #
    #                 target_players = [p for p in self.players if p != player and p.alive]
    #                 for idx, tp in enumerate(target_players):
    #                     print(f"{idx + 1}. {tp.name}")
    #
    #                 while True:
    #                     try:
    #                         choice = int(input("Enter number of the player to shoot: "))
    #                         if 1 <= choice <= len(target_players):
    #                             target = target_players[choice - 1]
    #                             print(f"🎯 {player.name} targets {target.name}!")
    #                             target.spin_and_fire()
    #                             break
    #                         else:
    #                             print("Invalid input.")
    #                     except ValueError:
    #                         print("Invalid input.")
    #
    #                 # 丢弃 deadly 和 lucky Joker
    #                 player.hand = [c for c in player.hand if not (c.is_joker and c.joker_role in ['deadly', 'lucky'])]
    #                 continue
    #
    #             elif has_deadly and not has_lucky:
    #                 print(f"\n☠️ {player.name} holds only a DEADLY Joker... Time to pull the trigger.")
    #                 player.spin_and_fire()
    #                 player.hand = [c for c in player.hand if not (c.is_joker and c.joker_role == 'deadly')]
    #                 if not player.alive:
    #                     break
    #                 continue
    #
    #         print()
    #
    #     print("🎴 Hands have been refreshed.")

    # def _deal_cards(self, alive_players):
    #     MAX_HAND = 2
    #     random.shuffle(self.deck)
    #
    #     for player in alive_players:
    #         drew_deadly = False
    #         drew_lucky = False
    #         card_index = 1
    #
    #         while len(player.hand) < MAX_HAND and self.deck:
    #             # deadly + lucky combo 条件成立
    #             if drew_deadly and any(card.is_joker and card.joker_role == 'lucky' for card in player.hand):
    #                 print(f"\n💀🛡️ {player.name} drew BOTH a DEADLY and a LUCKY Joker!")
    #                 print(f"{player.name}, choose a player to shoot:")
    #
    #                 target_players = [p for p in self.players if p != player and p.alive]
    #                 for idx, tp in enumerate(target_players):
    #                     print(f"{idx + 1}. {tp.name}")
    #
    #                 while True:
    #                     try:
    #                         choice = int(input("Enter number of the player to shoot: "))
    #                         if 1 <= choice <= len(target_players):
    #                             target = target_players[choice - 1]
    #                             print(f"🎯 {player.name} targets {target.name}!")
    #                             target.spin_and_fire()
    #
    #                             # Combo成功 → 丢弃两张 Joker
    #                             original_size = len(player.hand)
    #                             player.hand = [
    #                                 c for c in player.hand
    #                                 if not (c.is_joker and c.joker_role in ['deadly', 'lucky'])
    #                             ]
    #                             removed = original_size - len(player.hand)
    #                             print(f"🗑️ {player.name} discarded 2 Joker(s) used for combo.")
    #                             break
    #                         else:
    #                             print("Invalid input.")
    #                     except ValueError:
    #                         print("Invalid input.")
    #
    #                 # combo后继续抽牌
    #                 drew_deadly = False
    #                 drew_lucky = False
    #                 continue
    #
    #             card = self.deck.pop()
    #
    #             if card.is_joker:
    #                 if card.joker_role == 'deadly':
    #                     drew_deadly = True
    #                     print(f"🃏 {player.name} drew a Joker... and it's CURSED!")
    #                     print(f"🃏 {player.name} drew card {card_index}: {card}")
    #                     player.hand.append(card)
    #                     card_index += 1
    #
    #                     player.spin_and_fire()
    #                     print()
    #
    #                     if not player.alive:
    #                         player.hand = []
    #                         break  # 死了直接退出
    #                     # 生还者移除 deadly joker，防止末尾误判触发重复死亡
    #                     player.hand = [c for c in player.hand if not (c.is_joker and c.joker_role == 'deadly')]
    #                     continue
    #
    #                 elif card.joker_role == 'lucky':
    #                     drew_lucky = True
    #                     print(f"🃏 {player.name} drew a Joker... and it's a BLESSING!")
    #                     card_obj = Card("unknown", is_joker=True)
    #                     card_obj.joker_role = "lucky"
    #                     if len(player.hand) < MAX_HAND:
    #                         print(f"🃏 {player.name} drew card {card_index}: {card_obj}")
    #                         player.hand.append(card_obj)
    #                         card_index += 1
    #                     continue
    #
    #                 elif card.joker_role == 'mysterious':
    #                     print(f"🃏 {player.name} drew a MYSTERIOUS Joker...It can be anything!")
    #                     print(f"🃏 {player.name} drew card {card_index}: {card}")
    #                     player.hand.append(card)
    #                     card_index += 1
    #                     continue
    #             else:
    #                 print(f"🃏 {player.name} drew card {card_index}: {card}")
    #                 player.hand.append(card)
    #                 card_index += 1
    #
    #             if drew_deadly:
    #                 player.spin_and_fire()
    #                 print()
    #                 if not player.alive:
    #                     player.hand = []
    #                     break  # 死了不再发牌
    #                 drew_deadly = False  # 重置标记
    #                 continue
    #
    #         # 检查是否只持有 DEADLY Joker，强制触发死亡并 continue 跳过该玩家
    #         if any(c.is_joker and c.joker_role == 'deadly' for c in player.hand) and \
    #                 not any(c.is_joker and c.joker_role == 'lucky' for c in player.hand):
    #             deadly_card = [c for c in player.hand if c.is_joker and c.joker_role == 'deadly'][0]
    #             print(f"\n☠️ {player.name} holds only a DEADLY Joker... Time to pull the trigger.")
    #             player.spin_and_fire()
    #             player.hand.remove(deadly_card)
    #             if not player.alive:
    #                 continue
    #
    #         # 额外检查 combo 是否留在手牌末尾未触发
    #         if any(c.is_joker and c.joker_role == 'deadly' for c in player.hand) and \
    #            any(c.is_joker and c.joker_role == 'lucky' for c in player.hand):
    #             print(f"\n💀🛡️ {player.name} holds BOTH a DEADLY and a LUCKY Joker!")
    #             print(f"{player.name}, choose a player to shoot:")
    #
    #             target_players = [p for p in self.players if p != player and p.alive]
    #             for idx, tp in enumerate(target_players):
    #                 print(f"{idx + 1}. {tp.name}")
    #
    #             while True:
    #                 try:
    #                     choice = int(input("Enter number of the player to shoot: "))
    #                     if 1 <= choice <= len(target_players):
    #                         target = target_players[choice - 1]
    #                         print(f"🎯 {player.name} targets {target.name}!")
    #                         target.spin_and_fire()
    #                         original_size = len(player.hand)
    #                         player.hand = [c for c in player.hand if
    #                                        not (c.is_joker and c.joker_role in ['deadly', 'lucky'])]
    #                         removed = original_size - len(player.hand)
    #                         print(f"🗑️ {player.name} discarded {removed} Joker(s) used for combo.")
    #
    #                         continue
    #                     else:
    #                         print("Invalid input.")
    #                 except ValueError:
    #                     print("Invalid input.")
    #
    #         print()
    #
    #     print("🎴 Hands have been refreshed.")



    # Determines the losers and triggers their revolver. 决定输家并开枪
    def _resolve_round(self, alive_players):
        cards_played = []
        for player in alive_players:
            if not player.alive or not player.hand:
                continue
            card = None
            while card is None:
                card = player.play_card()  # 会一直要求用户输入，直到选中一张有效卡牌

            print(f"{player.name} plays: {card}")
            cards_played.append((player, card))

        if len(cards_played) < 2:
            # 仅一人出牌（其余可能死亡或空手），不触发判定
            return

        # 获取非免死玩家
        active_cards = [
            (player, card) for player, card in cards_played
            if not getattr(player, 'immune', False)
        ]


        # 平局判断逻辑
        if len(active_cards) == 0:
            print("🤝 All active players are immune this round. It's a draw!")
            print()
            for p in self.players:
                p.immune = False
            return

        if len(active_cards) == 1:
            print("🤝 Only one player eligible for battle. No death this round.")
            print()
            for p in self.players:
                p.immune = False  # 防止提前 return 导致下轮免疫遗留
            return

        types = [card.type for _, card in active_cards]
        unique = set(types)

        if len(unique) == 3:
            print("🤝 All cards are different. It's a draw!")
            print()
            for p in self.players:
                p.immune = False  # 防止提前 return 导致下轮免疫遗留
            return

        # 胜者/失败者判断逻辑
        win_map = {
            'scissors': 'paper',
            'paper': 'rock',
            'rock': 'scissors'
        }

        # 判定赢家和失败者类型
        if len(unique) == 2:
            type1, type2 = list(unique)
            if win_map[type1] == type2:
                winning_type = type1
                losing_type = type2
            elif win_map[type2] == type1:
                winning_type = type2
                losing_type = type1
            else:
                print("🤝 No decisive winner this round.")
                print()
                return

            losers = []
            for player, card in active_cards:
                if card.type == losing_type:
                    losers.append(player)
        else:
                print("🤝 No clear winner this round.")
                print()
                return

        # 开枪处理
        if not losers:
            print("No clear loser this round.")
            print()
            return
        else:
            for loser in losers:
                if getattr(loser, 'immune', False):
                    print(f"{loser.name} is immune and avoids death this round.")
                    print()
                else:
                    loser.spin_and_fire()

                    if len(self._get_alive_players()) == 1:
                        break

            # 清除 lucky Joker 的免死状态
            for p in self.players:
                p.immune = False

            # 最后再次检测胜利（防止前面用了 break 而没结束）
            if len(self._get_alive_players()) == 1:
                return

    def start(self):
        print("\n♠Welcome to Deadman's Deck!♠")
        print("====================================")
        print("Prepare to draw, shoot, and survive.\n")

        self._deal_cards(self._get_alive_players())

        while True:
            alive_players = self._get_alive_players()

            if len(alive_players) <= 1:
                break

            print(f"\n===== ROUND {self.round_number} =====")

            self._resolve_round(alive_players)

            # 关键新增判断：防止多余步骤
            if len(self._get_alive_players()) <= 1:
                break

            if not self.deck:
                print("\n⛔ Game stopped: The deck is empty.")
                break  # 牌不够 → 游戏终止

            self._deal_cards(self._get_alive_players())

            self.round_number += 1

        self._announce_winner()




    def _announce_winner(self):
        alive = self._get_alive_players()
        if len(alive) == 1:
            print(f"\n🏆 {alive[0].name} is the last one standing! Winner!")
        else:
            print("\n🤔 Unexpected game state: no winner identified.")






