import random
from src.bconj import distpar

print('start.')

y = random.randint(0,9)
dp = distpar(10)

while True:
    dp.bshows()
    x = input('guess ?')
    if x == -1:
        x = dp.make_guess()
    else:
        x = int(x)
    if x == y:
        print('nice')
        break
    else:
        dp.update_slots(guess = x)
        print('nope')
        print(dp.stats)





