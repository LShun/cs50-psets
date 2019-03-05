from cs50 import get_float

# get amount owed
while True:
    # get non-negative value
    change = get_float("Change owed: ")
    if change >= 0:
        break

# convert amount into cents (round due to imprecision)
change = round(change * 100)

# calculate coins to be returned (always use largest coin possible)

coins = 0

if change != 0:
    # quarters
    coins += change // 25
    change %= 25
    if change != 0:
        # dimes
        coins += change // 10
        change %= 10
        if change != 0:
            # nickles
            coins += change // 5
            change %= 5
            if change != 0:
                # pennies
                coins += change // 1
                change %= 1
print(coins)