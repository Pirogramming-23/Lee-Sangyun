num = 0

while True:
    try:
        count = int(input("부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : "))
        if count in [1, 2, 3]:
            break  
        else:
            print("1, 2, 3 중 하나를 입력하세요.")
    except ValueError:
        print("정수를 입력하세요.")

for _ in range(count):
    num += 1
    print(f"playerA : {num}")

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
    print(f"playerB : {num}")