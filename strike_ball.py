import pandas as pd
from itertools import permutations as permut
import numpy as np

print "save 4 different number between 0-9"

#All_Possible_Answer
A=list(permut([i+1 for i in range(9)],4))
gn=1
score_board=pd.Series([-1]*len(A),index=A)
ans=[0,-1]

while ans[0]!=4:
	print "---------------------"
	print "guess number ",gn
	print "---------------------"

	if sum(ans)==-1:
		choose_a=np.random.randint(len(A))
		guess=A[choose_a]

	elif sum(ans)==0:
		#MassiveElimination
		g=set(guess)
		A=list(permut(list(set([i+1 for i in range(9)])-g),4))
		#another_guess
		choose_a=np.random.randint(len(A))
		guess=A[choose_a]
		#another_guess
		
	elif sum(ans)==4:
		if len(A)<=24:
			#Elimination
			#new_scoring
			#another_guess
		else:
			#Massive_Elimination
			A=list(permut(guess,4))
			#new_scoring
			#another_guess
	else:
		#Elimination
		A.remove(guess)
		#new_scoring
		#another_guess

	print guess

	ans=input("is it true? [strike,ball] :")
	gn+=1
