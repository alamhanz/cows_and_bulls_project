import random
from src.bconj import distpar

print('start.')

y = random.randint(1,9)
dp = distpar(9)

while True:
    dp.bshows()
    x = input('guess ?')
    x = int(x)
    if x == y:
        print('nice')
        break
    else:
        dp.update_slots(guess = x)
        print('nope')





