from enums import ExtraEffectType


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
        #追加効果処理の実装
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
        elif effect == ExtraEffectType.FOCUS_UP:
            print("🔥追加効果：集中を1上昇！")
            game_state["focus"] += 1
        elif effect == ExtraEffectType.CONDITION_UP:
            print("💪追加効果：好調を1上昇！")
            game_state["condition"] += 1


