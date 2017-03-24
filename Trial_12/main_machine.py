import pandas as pd
import math
import numpy as np
from itertools import permutations as permut
import random

def data_val(pri,pos,co):
	dv=pd.DataFrame({'element':pos.index,'pos_prob':pos.values})
	dv['pri_prob']=dv.element.apply(lambda x : np.product(pri[list(x)].values))	
	# dv.to_csv('data_value_'+str(co)+'.csv')
	dv=dv[(dv.pri_prob>0.0) & (dv.pos_prob>0.0)]
	mp=dv.pri_prob.mean()
	st=dv.pri_prob.std()
	mp2=dv.pos_prob.mean()
	st2=dv.pos_prob.std()
	dv2=dv[(dv.pri_prob>0.0) & (dv.pos_prob>0.0)].element.values
	if len(dv)>50 and st>0.0:
		dv2=dv[dv.pri_prob<=mp].element.values

	elif st2>0.0:
		dv2=dv[dv.pos_prob>=mp2].element.values
		# print co
		# print dv
		# print mp2
		# print dv.pos_prob>=mp2

	if len(dv2)==0:
		dv2=dv[(dv.pri_prob>0.0) & (dv.pos_prob>0.0)].element.values
	print 'data_val :', len(dv2)

	return list(dv2)

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def iid_tes(X,x2):
	hasil=0
	if len(X)==1:
		hasil=0
	else:
		for x1 in X:
			if (len(set(x1[0]) & set(x2[0]))==0) and (x1[1]+x2[1]==4):
				hasil=x1[0]
				break
	return hasil

class prior_prob():

	def __init__(self, A):
		self.all_prior = A
		self.element = A.index.tolist()
		self.count=1
		self.former_guess=[]

	def update(self,answer,old_guess):
		self.strike=answer[0]
 		self.ball=answer[1]
		# respro=list(permut(old_guess,4))
		# alpro=0.0
		# for r in respro:
		# 	if r in self.former_guess:
		# 		alpro+=1
		# number_of_combination=len(respro)-alpro
		# prob_take=number_of_combination/(float(nCr(10,4))-self.count)
		self.former_guess.append((old_guess,sum(answer)))

		tes_guess=iid_tes(self.former_guess,self.former_guess[-1])
		if tes_guess!=0:
			guess_1=list(tes_guess)
			guess_2=list(self.former_guess[-1][0])
			gg=guess_1+guess_2
			for n in self.element:
				if n not in gg:
					self.all_prior[n]=0.0

		# print len(self.all_prior[(self.all_prior>0) | (self.all_prior<0) ])
		rest=len(self.all_prior[(self.all_prior>0) | (self.all_prior<0) ])

		for ans in self.element:
			if ans not in old_guess:
				if self.all_prior[ans]==-1:
					self.all_prior[ans]=((4-sum(answer))/4.0)#*(0.6)*(0.5))/(1.0/len(self.all_prior[(self.all_prior>0) | (self.all_prior<0) ]))
				else:
					pr_p2=((4-sum(answer))/4.0)*(1-((nCr(rest-1,3)/float(nCr(rest,4)))))*(self.all_prior[ans])
					pr_p1=pr_p2+((1-(pr_p2/self.all_prior[ans]))*(1-self.all_prior[ans]))
					self.all_prior[ans]=pr_p2/pr_p1#/(1.0/len(self.all_prior[(self.all_prior>0) | (self.all_prior<0) ]))
			else:
				if self.all_prior[ans]==-1:
					self.all_prior[ans]=(sum(answer)/4.0)#*(0.4)*(0.5))/(1.0/len(self.all_prior[(self.all_prior>0) | (self.all_prior<0) ]))
				else:
					pr_p2=(sum(answer)/4.0)*(nCr(rest-1,3)/float(nCr(rest,4)))*(self.all_prior[ans])
					pr_p1=pr_p2+((1-(pr_p2/self.all_prior[ans]))*(1-self.all_prior[ans]))
					self.all_prior[ans]=pr_p2/pr_p1#/(1.0/len(self.all_prior[(self.all_prior>0) | (self.all_prior<0) ]))

		print len(self.all_prior[self.all_prior>0])
		self.count+=1

class poster_prob():

	def __init__(self, A,prior=[-1.0]):
		self.all_poster=A
		self.prior_prob=prior
		self.element = A.index.tolist()
		self.bayes_matrix=np.ones([10,4])*-1.0
		self.count=1
		self.former_guess=[]
		self.massive=0

	def update(self,answer,old_guess,prior):
		self.former_guess.append((old_guess,sum(answer)))
		self.prior_prob=prior
		if sum(answer)==0:
			#MassiveElimination
			g=set(old_guess)
			A=list(permut(list(set([i+1 for i in range(9)])-g),4))
			self.all_poster=self.all_poster[A].fillna(0.0)
			self.element=self.all_poster.index.tolist()

		elif sum(answer)==4:
			if len(self.all_poster)<=24:
				#Elimination
				self.all_poster[old_guess]=0.0
			else:
				#Massive_Elimination
				A=list(permut(old_guess,4))
				self.all_poster=self.all_poster[A].fillna(0.0)
				self.all_poster[old_guess]=0.0
				self.element=self.all_poster.index.tolist()
				self.massive=1
		else:
			#MassiveElimination
			guess_variation=list(permut(old_guess,4))
			A=list(set(self.element)-set(guess_variation))
			self.all_poster=self.all_poster[A].fillna(0.0)
			self.element=self.all_poster.index.tolist()


		#update_matrix
		for el in old_guess:
			if self.bayes_matrix[el,old_guess.index(el)]==-1.0:
				self.bayes_matrix[el,old_guess.index(el)]=(self.prior_prob[el]*(answer[0]/4.0))
				for place in set([0,1,2,3])-set([old_guess.index(el)]):
					self.bayes_matrix[el,place]=(1-self.bayes_matrix[el,old_guess.index(el)])/3.0
			else:
				if self.bayes_matrix[el,old_guess.index(el)]==0.0:
					self.bayes_matrix[el,old_guess.index(el)]=0.0
				else:
					prob_place=((self.prior_prob[el])*(self.bayes_matrix[el,old_guess.index(el)]))+((1-self.prior_prob[el])*(1-self.bayes_matrix[el,old_guess.index(el)]))
					self.bayes_matrix[el,old_guess.index(el)]=((self.prior_prob[el]*(answer[0]/4.0))/prob_place)

				for place in set([0,1,2,3])-set([old_guess.index(el)]):
					if self.bayes_matrix[el,place]==0.0:
						self.bayes_matrix[el,place]=0.0
					else:	
						prob_place=(self.prior_prob[el]*self.bayes_matrix[el,place])+((1-self.prior_prob[el])*(1-self.bayes_matrix[el,place]))
						self.bayes_matrix[el,place]=((self.prior_prob[el]*((4-answer[0])/4.0))/prob_place)

		#update_score
		for comb in self.element:
			if self.all_poster[comb]==0.0:
				self.all_poster=self.all_poster.drop([comb])
			else:
				prob_comb=1
				for el in comb:
					prob_comb=prob_comb*self.bayes_matrix[el,comb.index(el)]

				if prob_comb<0:
					self.all_poster[comb]=-1.0
				else:
					self.all_poster[comb]=prob_comb

		self.element=self.all_poster.index.tolist()
		self.count+=1

	def new_guess(self):
		# print len(self.element)
		tes_guess=iid_tes(self.former_guess,self.former_guess[-1])
		se_sum_bayes=pd.Series([])
		if tes_guess!=0 and self.massive==0:
			guess_1=list(tes_guess)
			guess_2=list(self.former_guess[-1][0])
			g=set(guess_1+guess_2)
			A=list(permut(list(g),4))
			self.all_poster=self.all_poster[A].fillna(0.0)
			self.all_poster=self.all_poster[self.all_poster>0]
			self.element=self.all_poster.index.tolist()
			self.massive=1
		else:
			sum_bayes=sum(np.array(self.bayes_matrix).transpose())
			se_sum_bayes=pd.Series(sum_bayes)


		if (-4.0 in se_sum_bayes.values) and (self.massive==0):
			print 'MASUUUUK'
			
			never_been_guess=list(set(se_sum_bayes[se_sum_bayes<0].index.tolist()) & 
				set(self.prior_prob[self.prior_prob>0].index.tolist()))

			if len(never_been_guess)>=4:
				nguess_list1=list(permut(never_been_guess,4))
				nguess_list=list(set(nguess_list1) & set(self.element))

				nguess=random.choice(nguess_list)
			else:
				have_been_guess=se_sum_bayes[se_sum_bayes>=0].index.tolist()
				nguess=list(random.choice(list(permut(never_been_guess,len(never_been_guess)))))+list(random.choice(list(permut(have_been_guess,4-len(never_been_guess)))))

		else:
			# self.acc=max(self.all_poster.values)
			# nguess_list=self.all_poster[self.all_poster>=self.acc].index.tolist()
			# nguess=random.choice(nguess_list)
			nguess_list=data_val(self.prior_prob,self.all_poster,self.count)
			nguess=random.choice(nguess_list)
			print nguess
			
		# print len(self.all_poster.values)
		return nguess