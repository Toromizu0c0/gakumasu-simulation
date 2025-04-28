from CardClass import Card
from deck import Deck
from enums import ExtraEffectType
from game_state import create_game_state

def printBuff(gameState):
    if gameState['focus'] != 0:
        print(f"🔥集中： {game_state['focus']}")
    if gameState['condition'] != 0:
        print(f"💪好調： {game_state['condition']}")

deck = Deck()
cards = [
    #名前，コスト，スコア，追加効果，説明文
    
    Card("筋トレ", 3, 2),
    Card("読書", 2, 1, ExtraEffectType.DRAW_1,
         effect_description="次のターン，手札+1"),
    
    Card("瞑想", 1, 1, ExtraEffectType.COST_DOWN_NEXT, 
         effect_description="体力回復+3"),
    
    Card("ランニング", 2, 2),
    
    Card("休憩", 0, 0, ExtraEffectType.HEAL_HP_3, 
         effect_description="次のカードの消費体力-1"),
    
    Card("ゲーム", 4, 3),
    
    Card("精神統一", 0, 1, 
         extra_effect=ExtraEffectType.FOCUS_UP, 
         effect_description="集中を+1獲得"),
    
    Card("軽い",2, 3,
         extra_effect= ExtraEffectType.CONDITION_UP,
         effect_description="好調が3上昇")
]

for c in cards:
    deck.add_card(c)
deck.shuffle_draw_pile()

game_state = create_game_state()

for turn in range(1, 10):
    print(f"\n🎲 --- ターン {turn} ---")
    print(f"❤️ 体力: {game_state['hp']} | 🏆 スコア: {game_state['score']}")
    printBuff(game_state)
    
    deck.start_turn(game_state)
    deck.show_hand()
    deck.show_piles()
    if deck.hand and game_state["hp"] > 0:
        choice = input("使いたいカードの番号を入力（スキップはEnter，現在の山札一覧表示はa）: ").strip()
        if choice != "":
            try:
                index = int(choice)
                deck.play_card(index, game_state)
            except ValueError:
                print("⚠️ 無効な入力です。カードは使用されませんでした。")
        elif choice == "":
            deck.skip_turn(game_state)
        elif choice == "a":
            deck.show_deck()
            continue
            
    else:
        print("カードが使えないか、体力がありません。")
    deck.end_turn()
    deck.show_piles()
    if game_state["hp"] <= 0:
        print("💀 体力が尽きました！ゲーム終了！")
        break
print(f"\n🎯 最終スコア: {game_state['score']}（残り体力: {game_state['hp']}）")

