import random
from src.bconj import distpar

print('start the game.')

n_digits = 2
all_digits = [str(i) for i in range(10)]
y = random.sample(all_digits , k = n_digits)
y = ''.join(y)

dp = distpar()
while True:
    dp.bshows()
    x = input('guess ?')
    if x == '-1':
        x = dp.make_guess()

    if x == y:
        print('nice')
        break
    else:
        dp.update_slots(guess = x)
        print('nope')
        # print(dp.stats)
        print(dp.possible_bulls)


