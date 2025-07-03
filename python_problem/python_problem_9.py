import random

def brGame(num, player):
    if player == "computer":
        count = random.randint(1, 3)
    else: 
        while True:
            try:
                count_str = input("부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : ")
                count = int(count_str)
                if count in [1, 2, 3]:
                    break
                else:
                    print("1, 2, 3 중 하나를 입력하세요.")
            except ValueError:
                print("정수를 입력하세요.")

    for _ in range(count):
        num += 1
        print(f"{player} : {num}")
        if num >= 31:
            break
            
    return num

num = 0
current_player = "player" 

while num < 31:
    num = brGame(num, current_player)
    
    if num >= 31:
        winner = "computer" if current_player == "player" else "player"
        print(f"\n{winner} win!")
        break
    
    current_player = "computer" if current_player == "player" else "player"