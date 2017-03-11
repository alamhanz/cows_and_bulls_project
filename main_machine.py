import pandas as pd
import math
import numpy as np
from itertools import permutations as permut
import random

def data_val(pri,pos):

	return 

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def iid_tes(X,x2):
	if len(X)==1:
		return 0
	else:
		b=0
		for x1 in X:
			if (len(set(x1[0]) & set(x2[0]))==0) and (x1[1]+x2[1]==4):
				b=x1
				break
			else:
				b=0
		return b

class prior_prob():

	def __init__(self, A):
		self.all_prior = A
		self.element = A.index.tolist()
		self.count=1

	def update(self,answer,old_guess):
		self.strike=answer[0]
		self.ball=answer[1]
		for ans in old_guess:
			if self.all_prior[ans]==-1:
				self.all_prior[ans]=float((sum(answer)/4.0)*(((nCr(4,sum(answer)))*(nCr(6,4-sum(answer))))/(float(nCr(10,4))-self.count)))
			else:
				self.all_prior[ans]=(self.all_prior[ans]*(sum(answer)/4.0)*
					((nCr(4,sum(answer))*nCr(6,4-sum(answer)))/(float(nCr(10,4))-self.count)))

		if sum(answer)==4:
			for el in self.element:
				if el not in old_guess:
					self.all_prior[el]=0.0

		for ans in self.element:
			if ans not in old_guess:
				if self.all_prior[ans]==-1:
					self.all_prior[ans]=(1-(sum(answer)/4.0))*(1-(((nCr(4,sum(answer)))*(nCr(6,4-sum(answer))))/(float(nCr(10,4))-self.count)))
				else:
					self.all_prior[ans]=self.all_prior[ans]*(1-(sum(answer)/4.0))*(1-((nCr(4,sum(answer))*nCr(6,4-sum(answer)))/(float(nCr(10,4))-self.count)))


		self.count+=1

class poster_prob():

	def __init__(self, A,prior=[-1.0]):
		self.all_poster=A
		self.prior_prob=prior
		self.element = A.index.tolist()
		self.bayes_matrix=np.ones([10,4])*-1.0
		self.count=1
		self.former_guess=[]

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
		else:
			#MassiveElimination
			guess_variation=list(permut(old_guess,4))
			A=list(set(self.element)-set(guess_variation))
			self.all_poster=self.all_poster[A].fillna(0.0)
			self.element=self.all_poster.index.tolist()


		#update_matrix
		for el in old_guess:
			if self.bayes_matrix[el,old_guess.index(el)]==-1.0:
				self.bayes_matrix[el,old_guess.index(el)]=((self.prior_prob[el]*(answer[0]/4.0))/0.25)
				for place in set([0,1,2,3])-set([old_guess.index(el)]):
					self.bayes_matrix[el,place]=(1-self.bayes_matrix[el,old_guess.index(el)])*(1/3.0)
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
		massive=0
		if iid_tes(self.former_guess,self.former_guess[-1])!=0:
			guess_1=iid_tes(self.former_guess,self.former_guess[-1])[0]
			guess_2=self.former_guess[-1][0]
			g=set(guess_1+guess_2)
			A=list(permut(list(g),4))
			self.all_poster=self.all_poster[A].fillna(0.0)
			self.element=self.all_poster.index.tolist()
			massive=1

		if (-1.0 in self.prior_prob.values) and (massive==0):
			never_been_guess=self.prior_prob[self.prior_prob==-1.0].index.tolist()
			if len(never_been_guess)>=4:
				nguess_list=list(permut(never_been_guess,4))
				nguess=random.choice(nguess_list)
			else:
				have_been_guess=self.prior_prob[self.prior_prob!=-1.0].index.tolist()
				nguess=list(random.choice(list(permut(never_been_guess,len(never_been_guess)))))+list(random.choice(list(permut(have_been_guess,4-len(never_been_guess)))))
		else:
			# self.acc=max(self.all_poster.values)
			# nguess_list=self.all_poster[self.all_poster>=self.acc].index.tolist()
			# nguess=random.choice(nguess_list)
			dtp=data_val(self.prior_prob,self.all_poster)
		# print len(self.all_poster.values)
		return nguess