import random
from enum import Enum, auto

class ExtraEffectType(Enum):
    DRAW_1 = auto()
    COST_DOWN_NEXT = auto()
    HEAL_HP_3 = auto()


class Card:
    def __init__(self, name: str, score_up: int, cost: int, 
                 extra_effect: ExtraEffectType = None, 
                 effect_description: str = ""):
        self.name = name
        self.score_up = score_up
        self.cost = cost
        self.extra_effect = extra_effect
        self.effect_description = effect_description  # ← 表示用説明文

    def __repr__(self):
        extra = f", Extra: {self.effect_description}" if self.effect_description else ""
        return f"{self.name} (Cost: {self.cost}, Score+{self.score_up}{extra})"

    def apply_effect(self, deck, game_state):
        """追加効果を処理"""
        effect = self.extra_effect
        if effect == ExtraEffectType.DRAW_1:
            print("🃏 追加効果：次のターン，カードを1枚ドロー！")
            game_state["hand_size"] += 1
        elif effect == ExtraEffectType.COST_DOWN_NEXT:
            print("💸 追加効果：次のカードのコストが1軽減！")
            game_state["cost_modifier"] = 1
        elif effect == ExtraEffectType.HEAL_HP_3:
            print("💖 追加効果：体力を3回復！")
            game_state["hp"] += 3


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
            print("🔄 捨て札を山札に戻してシャッフルしました。")

    def start_turn(self):
        self.hand = []
        self.draw_cards(game_state.get("hand_size", 3))

    def play_card(self, index: int, game_state: dict):
        if 0 <= index < len(self.hand):
            card = self.hand[index]
            effective_cost = max(0, card.cost - game_state.get("cost_modifier", 0))
            if effective_cost > game_state["hp"]:
                print(f"❌ {card.name} を使用するには体力が足りません！（必要: {effective_cost}, 現在: {game_state['hp']}）")
                return None
            self.hand.pop(index)
            self.banished_pile.append(card)
            print(f"✅ {card.name} を使用しました（スコア +{card.score_up}, 体力 -{effective_cost}）")
            game_state["score"] += card.score_up
            game_state["hp"] -= effective_cost
            game_state["cost_modifier"] = 0  # 効果のリセット
            card.apply_effect(self, game_state)
            return card
        else:
            print("その番号のカードは存在しません")
            return None

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand = []

    def show_hand(self):
        print("🖐 手札:")
        for i, card in enumerate(self.hand):
            print(f"  [{i}] {card}")

    def show_piles(self):
        print(f"📦 山札: {len(self.draw_pile)}枚 | 捨て札: {len(self.discard_pile)}枚 | 除外: {len(self.banished_pile)}枚")


# 実行部
if __name__ == "__main__":
    deck = Deck()
    cards = [
        Card("筋トレ", 3, 2),
        Card("読書", 2, 1, ExtraEffectType.DRAW_1,
             effect_description="次のターン，手札+1"),
        
        Card("瞑想", 1, 1, ExtraEffectType.COST_DOWN_NEXT, 
             effect_description="体力回復+3"),
        
        Card("ランニング", 2, 2),
        
        Card("休憩", 0, 0, ExtraEffectType.HEAL_HP_3, 
             effect_description="次のカードの消費体力-1"),
        
        Card("ゲーム", 4, 3),
    ]
    for c in cards:
        deck.add_card(c)
    deck.shuffle_draw_pile()

    game_state = {
        "score": 0,
        "hp": 10,
        "cost_modifier": 0,
        "hand_size": 3
    }

    for turn in range(1, 10):
        print(f"\n🎲 --- ターン {turn} ---")
        print(f"❤️ 体力: {game_state['hp']} | 🏆 スコア: {game_state['score']}")
        deck.start_turn()
        deck.show_hand()
        deck.show_piles()

        if deck.hand and game_state["hp"] > 0:
            choice = input("使いたいカードの番号を入力（スキップはEnter）: ").strip()
            if choice != "":
                try:
                    index = int(choice)
                    deck.play_card(index, game_state)
                except ValueError:
                    print("⚠️ 無効な入力です。カードは使用されませんでした。")
        else:
            print("カードが使えないか、体力がありません。")

        deck.end_turn()
        deck.show_piles()

        if game_state["hp"] <= 0:
            print("💀 体力が尽きました！ゲーム終了！")
            break

    print(f"\n🎯 最終スコア: {game_state['score']}（残り体力: {game_state['hp']}）")
