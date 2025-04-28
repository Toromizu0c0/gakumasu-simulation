from enum import Enum, auto

class ExtraEffectType(Enum):
    DRAW_1 = auto()
    COST_DOWN_NEXT = auto()
    HEAL_HP_3 = auto()
    FOCUS_UP = auto()#集中バフ
    CONDITION_UP = auto()#好調バフ