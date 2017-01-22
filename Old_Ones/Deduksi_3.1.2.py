# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 05:56:42 2015

@author: Aska
"""

from random import *
import numpy as np
import sys

def cek(S,T):
    strike=sum([int(S[i]==T[i]) for i in range(len(S))])
    bub=0
    for i in S:
        if i in T:
            bub=bub+1
    bub=bub-strike
    return [bub,strike]

def PrBu(X,s,h,A):
    for i in range(len(s)):
        if A[X.index(s[i])]>=1.5:
            A[X.index(s[i])]=(float(h[0]+h[1])/4)
        else:
            A[X.index(s[i])]=float(A[X.index(s[i])])*(float(h[0]+h[1])/4)
    return A

def PrSt(X,s,h,A):
    for i in range(len(s)):
        for j in range(3):
            if A[X.index(s[i])][s.index(s[i])]>=1.5:
                A[X.index(s[i])][s.index(s[i])]=(float(h[1])/4)
            else:
                A[X.index(s[i])][s.index(s[i])]=float(A[X.index(s[i])][s.index(s[i])])*(float(h[1])/4)
    return A

def Datain(X,s,h,A,B,c,l):
    if h==[0,4]:
        return 1
    elif h[0]+h[1]==4:
        A=list(np.array(list(np.zeros(len(X))))+5)
        B=PrSt(X,s,h,B)
        X2=[]
        A2=[]
        B2=[]
        c2=[]
        s.sort()
        for i in range(len(s)):
            X2.append(s[i])
            A2.append(A[X.index(s[i])])
            B2.append(B[X.index(s[i])])
            c2.append(c[X.index(s[i])])   
        l=6
        return [X2,A2,B2,c2,l]
        
    elif h[0]+h[1]==0:
        for i in range(len(s)):
            A.pop(int(X.index(s[i])))
            B.pop(int(X.index(s[i])))
            c.pop(int(X.index(s[i]))) 
            X.pop(int(X.index(s[i])))
            l=l+1
        return [X,A,B,c,l]
    
    else:
        A=PrBu(X,s,h,A)
        B=PrSt(X,s,h,B)
        return [X,A,B,c,l]

def Product(P):
    P1=[]
    for i in range(len(P)):
        if np.mod(sum(P[i]),2)==0:
            P1.append(0.0)
        else:
            j=0
            k=1
            while j<=3:
                if P[i][j]<=0.9999:
                    k=float(k)*P[i][j]
                j=j+1
            P1.append(k)
    return P1
        
def my_guess(X,P):

    n=len(P[0])
    P1=np.array(P)
    P1=list(np.transpose(P))
    for i in range(4):
        P1[i]=list(P1[i])
        for j in range(n):
            if P1[i][j]==2.0:
                P1[i][j]=0.0
    maxi1=[]
    for i in range(4):
        maxi1.append(max(P1[i]))
    
    maxi=list(np.copy(maxi1))
    s=['k','k','k','k']
    while 'k' in s:
        ind=maxi.index(max(maxi1))
        inde=P1[ind].index(max(P1[ind]))
        s[ind]=X[inde]
        for i in range(4):
            P1[i].pop(inde)
        X.pop(inde)
        maxi1.remove(max(maxi1))
        maxi[ind]='k'
    
    return s
        
    

My_num=input("angka : ")
lw=input("Trying : ")
test=[]
tess=0
while tess<=lw:
    loop=0
    done=0
    X=[0,1,2,3,4,5,6,7,8,9]
    prB=list(np.array(list(np.zeros(len(X))))+2.0)
    prS=[list(x) for x in np.array(list(np.zeros([len(X),4])))+2.0]
    count=list(np.zeros(len(X)))
    lose=0
    var_list=[]


    while done==0:
        #print loop
        if loop>=20:
            break
            
        #print "---------------------------------------------"
        
        if 2 in prB:
            X1=list(np.copy(X))
            count1=list(np.copy(count))
            prB1=list(np.copy(prB))
            prS1=list(np.copy(prS))
            #print
            #print "Your number is .."
            s=[0,0,0,0]
            lose1=0
            prr=1
            LnX1=len(X1)-1
            while prr<=2:
                try :
                    if loop>=1 and LnX1+1>=4:
                        ind=randint(0,LnX1)
                        if prB1[ind]!=2:
                            X1.pop(ind)
                            prB1.pop(ind)
                            prS1.pop(ind)
                            count1.pop(ind)
                            prr=prr+1
                            lose1=lose1+1
                        else:
                            if np.mod(sum(prB1),2)==0:
                                X1.pop(ind)
                                prB1.pop(ind)
                                prS1.pop(ind)
                                count1.pop(ind)
                                prr=prr+1
                                lose1=lose1+1
                            else:
                                ind=randint(0,LnX1)
                    else:
                        ind=randint(0,LnX1)
                        if LnX1+1>=4:
                            X1.pop(ind)
                            prB1.pop(ind)
                            prS1.pop(ind)
                            count1.pop(ind)
                            prr=prr+1
                            lose1=lose1+1
                except:
                    ind=0
    
            
            s=sample(X1,4)            
            #print s
            #print
            for i in s:
                count[X.index(i)]=count[X.index(i)]+1
            has=cek(s,My_num)
            #has=[0,0]
            #print has
            #print
            Pr=Datain(X,s,has,prB,prS,count,lose)
            if Pr==1:
                done=1
                break
            else:
                X=Pr[0]
                prB=Pr[1]
                prS=Pr[2]
                count=Pr[3]
                lose=Pr[4]
                            
        else:
            #print "----------MASUK-----------"
            X1=list(np.copy(X))
            count1=list(np.copy(count))
            prB1=list(np.copy(prB))
            prS1=list(np.copy(prS))
            #print
            #print "Your number is .."
            s=[0,0,0,0]
            prr=0
            #Variansi dari banyaknya count
            var_list.append(np.var(count1))
            if np.var(count1)>=0.15 and len(X1)>=5:
                lose1=0
                for i in range(randint(max(4-lose,0),max(0,6-lose))):
                    if len(X1)>=5:
                        iv=count1.index(max(count1))
                        X1.pop(iv)
                        prB1.pop(iv)
                        prS1.pop(iv)
                        count1.pop(iv)
            elif np.var(count1)>=0.1 and len(X1)>=5:
                lose1=0
                for i in range(randint(max(3-lose,0),max(5-lose,0))):
                    if len(X1)>=5:
                        iv=count1.index(max(count1))
                        X1.pop(iv)
                        prB1.pop(iv)
                        prS1.pop(iv)
                        count1.pop(iv)
            elif len(X1)>=5:
                lose1=0
                for i in range(randint(max(2-lose,0),max(4-lose,0))):
                    if len(X1)>=5:
                        iv=count1.index(max(count1))
                        X1.pop(iv)
                        prB1.pop(iv)
                        prS1.pop(iv)
                        count1.pop(iv)
            
            #Vanish number who has the biggest opportunity
            prS2=Product(prS1)
        
            if len(X1)>=5:
                ran=randint(0,max(0,len(X1)-4))
                if randint(0,1)==1:
                    for i in range(ran):
                        if len(X1)>=5:
                            iv=prS2.index(min(prS2))
                            X1.pop(iv)
                            prB1.pop(iv)
                            prS1.pop(iv)
                            count1.pop(iv)
                            prS2.pop(iv)
                else:
                    for i in range(ran):
                        if len(X1)>=5:
                            iv=prS2.index(max(prS2))
                            X1.pop(iv)
                            prB1.pop(iv)
                            prS1.pop(iv)
                            count1.pop(iv)
                            prS2.pop(iv)
                    
            
            #Pilih samplenya
            s=my_guess(X1,prS1)
            #print s
            
            #print
            for i in s:
                count[X.index(i)]=count[X.index(i)]+1
            has=cek(s,My_num)
            #has=[0,0]
            #print has
            #print
            Pr=Datain(X,s,has,prB,prS,count,lose)
            if Pr==1:
                done=1
                break
            else:
                X=Pr[0]
                prB=Pr[1]
                prS=Pr[2]
                count=Pr[3]
            
            
        loop=loop+1
    
    if done==1:
        print "done"
        print loop
        test.append(loop)
    else:
        print "not yet"
        
    tess=tess+1

print "\n----------------Fin-----------------"
if len(test)>=1:
    print "mean :", float(sum(test))/len(test)
    print "var :", np.var(test)
    print "Tertebak :", (len(test)/float(lw))*100,"%"
else:
    print "mean : nope"
    print "var : nope"