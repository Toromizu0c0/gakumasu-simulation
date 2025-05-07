class Card:
    def __init__(self, name: str, score_up: int, cost: int,
                 effect_description: str = "", effects=None):
        
        self.name = name
        self.score_up = score_up
        self.cost = cost
        self.effect_description = effect_description  # ← 表示用説明文
        self.effects = effects or {}

    def __repr__(self):
        extra = f", Extra: {self.effect_description}" if self.effect_description else ""
        return f"{self.name} (Cost: {self.cost}, Score+{self.score_up}{extra})"

    def apply_effect(self, game_state):
        #追加効果処理の実装
        
        for key, value in self.effects.items():
            if key == "hp":
                before = game_state["hp"]
                game_state["hp"] = min(game_state["max_hp"], game_state["hp"] + value)
                print(f"💖 HP: {before} → {game_state['hp']}")               
            elif key in game_state:
                before = game_state[key]
                game_state[key] += value


