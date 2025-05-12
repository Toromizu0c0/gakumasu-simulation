from CardClass import Card
from deck import Deck
from enums import ExtraEffectType
from game_state import create_game_state

def printBuff(gameState):
    if gameState['focus'] != 0:
        print(f"🔥集中： {game_state['focus']}")
    if gameState['condition'] != 0:
        print(f"💪好調： {game_state['condition']}")
    if gameState['great_condition'] != 0:
        print(f"絶好調： {game_state['great_condition']}")

deck = Deck()
cards = [
    #名前，コスト，スコア，追加効果，説明文
    
    Card("筋トレ", 3, 2,
         effect_description="スコア+2",
         effects = {}),
    
    Card("読書", 2, 1,
         effect_description="次のターン，手札+1",
         effects = {"next_hand":1}),
    
    Card("瞑想", 4, 1, 
         effect_description="体力回復+3",
         effects = {"hp":3}),
    
    Card("ランニング", 2, 2,
         effect_description="スコア+2",
         effects={}),
    
    # Card("休憩", 0, 0, ExtraEffectType.HEAL_HP_3, 
    #      effect_description="次のカードの消費体力-1"),
    
    Card("ゲーム", 4, 3,
         effect_description="スコア+3",
         effects={}),
    
    Card("精神統一", 3, 1, 
         effect_description="集中を+1獲得",
         effects={"focus":1}),
    
    Card("軽い",2, 3,
         effect_description="好調が3増加",
         effects={"condition":3}),
    
    Card("計画", 2, 0, 
         effect_description="絶好調が+3増加",
         effects={"greatcondition":3})
]

for c in cards:
    deck.add_card(c)
deck.shuffle_pile(deck.draw_pile)

game_state = create_game_state()

turn=1
while turn<=20 :#ターン回し
# for turn in range(1, 20):
    print(f"\n🎲 --- ターン {turn} ---")
    print(f"❤️ 体力: {game_state['hp']} | 🏆 スコア: {game_state['score']}")
    printBuff(game_state)
    
    deck.start_turn(game_state)
    deck.show_piles()
    deck.show_hand()
    
    
    choice = input("使いたいカードの番号を入力（スキップはEnter，現在の山札一覧表示はa）: ").strip()
    if choice != "": 
        if choice >= "0" and choice < str(game_state['hand_size']):
            index = int(choice)
            result = deck.play_card( index, game_state)
            
        elif choice == "a":
            #山札一覧表示
            deck.show_deck()
        
        if result == None:
            #体力が足りない or 想定外の入力
            print(f"result -> None")
            deck.end_turn()
            deck.show_piles()
            continue
        
    else:
        #何も入力されなかった場合（スキップ）
        deck.skip_turn(game_state)
        
        
    deck.end_turn()
    deck.show_piles()
    turn += 1
    
print(f"\n🎯 最終スコア: {game_state['score']}（残り体力: {game_state['hp']}）")
