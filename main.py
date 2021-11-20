import random
from src.bconj import distpar

print('start.')

y = random.randint(1,9)

# while True:
#     x = input('guess ?')
#     x = int(x)
#     if x == y:
#         print('nice')
#         break
#     else:
#         print('nope')

dp = distpar(9)
print(dp.slots[1])
dp.bshows(2)

