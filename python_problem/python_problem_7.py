num = 0
current_player = "playerA"

while num < 31:
    while True:
        try:
            count_str = input(f"{current_player}님, 부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : ")
            count = int(count_str)
            if count in [1, 2, 3]:
                break
            else:
                print("1, 2, 3 중 하나를 입력하세요.")
        except ValueError:
            print("정수를 입력하세요.")

    for _ in range(count):
        num += 1
        print(f"{current_player} : {num}")
        if num >= 31:
            if current_player == "playerA":
                print("\nplayerB win!")
            else:
                print("\nplayerA win!")
            break
    if current_player == "playerA":
            current_player = "playerB"
    else:
        current_player = "playerA"