import random
import math
from CardClass import Card

class Deck:
    def __init__(self):
        self.draw_pile = []
        self.discard_pile = []
        self.banished_pile = []
        self.hand = []

    def add_card(self, card: Card):
        self.draw_pile.append(card)

    def shuffle_draw_pile(self):
        random.shuffle(self.draw_pile)

    def draw_cards(self, num: int):
        for _ in range(num):
            if not self.draw_pile:
                self.reshuffle_discard_into_draw()
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop(0))

    def reshuffle_discard_into_draw(self):
        if self.discard_pile:
            self.draw_pile = self.discard_pile
            self.discard_pile = []
            self.shuffle_draw_pile()
            print("🔄 捨て札を山札に戻してシャッフル。")

    def start_turn(self, game_state):
        self.hand = []
        if game_state['condition'] >= 1:
            game_state['condition'] -= 1
        self.draw_cards(game_state.get("hand_size", 3))
        

    def play_card(self, index: int, game_state):
        if 0 <= index < len(self.hand):
            card = self.hand[index]
            effective_cost = max(0, card.cost - game_state.get("cost_modifier", 0))
            if effective_cost > game_state["hp"]:
                print(f"❌ {card.name} を使用するには体力が足りません！（必要: {effective_cost}, 現在: {game_state['hp']}）")
                return None
            self.hand.pop(index)
            self.banished_pile.append(card)
            
            #スコアの計算
            focus_bonus = game_state.get("focus", 0)
            condition_bonus = game_state.get("condition", 0)
            great_condition_bonus = game_state.get("great_condition", 0)
            total_score = focus_bonus + card.score_up#集中の計算
            if condition_bonus != 0:#好調の計算
                total_score *= 1.5
                math.floor(total_score)
            if great_condition_bonus != 0:#絶好調の計算
                total_score *= (1+(0.1*great_condition_bonus))
                math.floor(total_score)
                
            print(f"✅ {card.name} を使用しました（スコア +({total_score}), 体力 -{effective_cost}）")
            game_state["score"] += total_score
            game_state["hp"] -= effective_cost
            game_state["cost_modifier"] = 0  # 効果のリセット
            card.apply_effect(game_state)
            return card
        else:
            print("その番号のカードは存在しません")
            return None

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand = []
        
    def skip_turn(self, game_state):
        heal_amount = 2
        old_hp = game_state["hp"]
        game_state["hp"] = min(game_state["max_hp"], game_state["hp"] + heal_amount)
        healed = game_state["hp"] - old_hp
        print(f"🛌 ターンをスキップしたため、体力を{healed}回復（現在の体力: {game_state['hp']}）")    

    def show_hand(self):
        print("🖐 手札:")
        for i, card in enumerate(self.hand):
            print(f"  [{i}] {card}")

    def show_piles(self):
        print(f"📦 山札: {len(self.draw_pile)}枚 | 捨て札: {len(self.discard_pile)}枚 | 除外: {len(self.banished_pile)}枚")
        
    def show_deck(self):
        print(self.draw_pile)
