def brGame(num, player):
    while True:
        try:
            count_str = input(f"{player}님, 부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : ")
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
player = "playerA"

while num < 31:
    num = brGame(num, player)
    
    if num >= 31:
        break
    else:
        player = "playerB" if player == "playerA" else "playerA"