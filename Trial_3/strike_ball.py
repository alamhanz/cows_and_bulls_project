import pandas as pd
from itertools import permutations as permut
import numpy as np
from main_machine import prior_prob, poster_prob
import random

print "save 4 different number between 0-9"

#All_Possible_Answer
A=list(permut([i+1 for i in range(9)],4))
gn=1
prior_score=prior_prob(pd.Series([-1.0]*len([i for i in range(10)]),index=[i for i in range(10)]))
score_board=poster_prob(pd.Series([-1.0]*len(A),index=A),prior=prior_score.all_prior)
ans=[0,-1]

while ans[0]!=4:
	print "---------------------"
	print "guess number ",gn
	print "---------------------"

	if sum(ans)==-1:
		guess=random.choice(A)
	else:
		#new_scoring
		prior_score.update(ans,guess)
		score_board.update(ans,guess,prior_score.all_prior)
		#another_guess
		guess=score_board.new_guess()


	print prior_score.all_prior,'\n'
	print score_board.bayes_matrix,'\n'
	print guess

	A=score_board.element
	ans=input("is it true? [strike,ball] :")
	gn+=1


