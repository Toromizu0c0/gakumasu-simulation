def create_game_state():
    return {
        "score": 0,
        "hp": 10,
        "max_hp": 10,
        "cost_modifier": 0,
        "hand_size": 3,
        "focus": 0,#集中を実装
        "condition":0,#好調を実装
        "great_condition":0,#絶好調を実装
        
        #バフ減衰を制御
        "condition_gained":False,
        "great_condition_gained":False,
    }