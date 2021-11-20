import pandas as pd
from itertools import permutations as permut
import numpy as np
from main_machine import prior_prob, poster_prob
import random
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def answer_guess(pred,truen):
	strike=0
	ball=0
	for i in pred:
		if i in truen:
			if pred.index(i)==truen.index(i):
				strike+=1
			else:
				ball+=1

	return [strike,ball]

print "save 4 different number between 0-9"

file_r = open('result_trial_3.txt','w')
guess_numb=[]
str_file=''
for trials in range(1500):
	Bt=list(permut([i+1 for i in range(9)],4))
	true_one=random.choice(Bt)

	#All_Possible_Answer
	A=list(permut([i+1 for i in range(9)],4))
	gn=1 
	prior_score=prior_prob(pd.Series([-1.0]*len([i for i in range(10)]),index=[i for i in range(10)]))
	score_board=poster_prob(pd.Series([-1.0]*len(A),index=A),prior=prior_score.all_prior)
	ans=[0,-1]

	print trials
	str_file_2=''
	while ans[0]!=4:
		# print "---------------------"
		# print "guess number ",gn
		# print "---------------------"

		
		if sum(ans)==-1:
			guess=random.choice(A)
		else:
			#new_scoring
			prior_score.update(ans,guess)
			score_board.update(ans,guess,prior_score.all_prior)

			#another_guess
			# try:
			guess=score_board.new_guess()
			# 	str_file_2=str_file_2+'   \nguess_'+str(gn)+' '+str(guess)
			# except:
			# 	str_file_2=str_file_2+'   \nguess_'+str(gn)+' FAILED'
			# 	print 'FAILED'
			# 	break


		# print prior_score.all_prior,'\n'
		# print score_board.bayes_matrix,'\n'
		# print guess

		A=score_board.element
		# ans=input("is it true? [strike,ball] :")
		ans=answer_guess(guess,true_one)

		gn+=1

	guess_numb.append(gn)
	if ans[0]==4:
	 	str_file=str_file+'\nTrial '+str(trials)+' the problem is '+str(true_one)+' success with '+str(gn)
	else:
		str_file=str_file+'\nTrial Error :\n'
		str_file=str_file+str_file_2

	

	print '-'*10
file_r.write(str_file) 
file_r.close() 
print np.average(guess_numb)

df=pd.DataFrame({'Avg_GN':guess_numb})

fig, ax = plt.subplots()
df.hist('Avg_GN', ax=ax,bins=50)
plt.title('average trial 3 :'+str(np.average(guess_numb))+'\nwith std :'+str(np.std(guess_numb)))
fig.savefig('number_distribution_3.png')