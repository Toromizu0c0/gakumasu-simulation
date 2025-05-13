class EffectHandler:
    def __init__(self, game_state):
        self.game_state = game_state

    def apply(self, effects: dict):#追加効果適用
        for key, value in effects.items():
            if key == "hp":#HP回復
                self._heal_hp(value)
            elif key in self.game_state:#その他バフ増加
                self._increase_buff(key, value)

    def _heal_hp(self, amount):
        before = self.game_state["hp"]
        self.game_state["hp"] = min(self.game_state["max_hp"], self.game_state["hp"] + amount)

    def _increase_buff(self, buff_name, value):
        before = self.game_state[buff_name]
        self.game_state[buff_name] += value
        
        if before==0 and self.game_state[buff_name] > 0:
            if buff_name == "condition":
                self.game_state["condition_just_gained"] = True
            if buff_name == "great_condition":
                self.game_state["great_condition_just_gained"] = True