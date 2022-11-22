# -*- coding: utf-8 -*-
"""
@authors: Sergio Valadez Godínez, Juan Humberto Sossa Azuela, Raúl Santiago Montero
"""

import numpy as np
import csv
import math

def HHTFE(dt,to,T,Io,gBarK,gBarNa,gBarL,EK,ENa,EL,C):
		#an,bn,am,bm,ah,bh
		abcoeff=[]
		i=-100
		while i<=201:
				vector=[]
				for j in range(4):
						vector.append(alphan(i))
						vector.append(bethan(i))
						vector.append(alpham(i))
						vector.append(betham(i))
						vector.append(alphah(i))
						vector.append(bethah(i))
				abcoeff.append(vector)
				i=i+1
				
		t=[]
		n=[]
		m=[]
		h=[]
		V=[]
		t.append(to)
		V.append(0.0)
		iV=int(math.floor(V[0]+100.5))
		n.append(abcoeff[iV][0]/(abcoeff[iV][0]+abcoeff[iV][1]))
		m.append(abcoeff[iV][2]/(abcoeff[iV][2]+abcoeff[iV][3]))
		h.append(abcoeff[iV][4]/(abcoeff[iV][4]+abcoeff[iV][5]))
		i=0
		while t[i]<=T:
				iV=int(math.floor(V[i]+100.5))
				t.append(t[i]+dt)
				Vk1=fV(V[i],n[i],m[i],h[i],Io)
				a=abcoeff[iV][0]
				BA=a+abcoeff[iV][1]
				nk1=a-n[i]*BA
				
				a=abcoeff[iV][2]
				BA=a+abcoeff[iV][3]
				mk1=a-m[i]*BA
				
				a=abcoeff[iV][4]
				BA=a+abcoeff[iV][5]
				hk1=a-h[i]*BA
				
				V.append(V[i]+Vk1*dt)
				n.append(n[i]+nk1*dt)
				m.append(m[i]+mk1*dt)
				h.append(h[i]+hk1*dt)
				print(f">>>> {n[-1]} {m[-1]} {h[-1]}")
				
				i=i+1
		return np.asarray(t),np.asarray(V)
		
def HHTRK4(dt,to,T,Io,gBarK,gBarNa,gBarL,EK,ENa,EL,C):
		#an,bn,am,bm,ah,bh
		abcoeff=[]
		i=-100
		while i<=201:
				vector=[]
				for j in range(4):
						vector.append(alphan(i))
						vector.append(bethan(i))
						vector.append(alpham(i))
						vector.append(betham(i))
						vector.append(alphah(i))
						vector.append(bethah(i))
				abcoeff.append(vector)
				i=i+1
				
		t=[]
		n=[]
		m=[]
		h=[]
		V=[]
		t.append(to)
		V.append(0.0)
		iV=int(math.floor(V[0]+100.5))
		n.append(abcoeff[iV][0]/(abcoeff[iV][0]+abcoeff[iV][1]))
		m.append(abcoeff[iV][2]/(abcoeff[iV][2]+abcoeff[iV][3]))
		h.append(abcoeff[iV][4]/(abcoeff[iV][4]+abcoeff[iV][5]))
		dt2=0.5*dt
		i=0
		while t[i]<=T:
				iV=int(math.floor(V[i]+100.5))
				t.append(t[i]+dt)
				 
				Vk1=fV(V[i],n[i],m[i],h[i],Io)
				a=abcoeff[iV][0]
				BA=a+abcoeff[iV][1]
				nk1=a-n[i]*BA
				a=abcoeff[iV][2]
				BA=a+abcoeff[iV][3]
				mk1=a-m[i]*BA
				a=abcoeff[iV][4]
				BA=a+abcoeff[iV][5]
				hk1=a-h[i]*BA
				
				Vaux=V[i]+Vk1*dt2
				naux=n[i]+nk1*dt2
				maux=m[i]+mk1*dt2
				haux=h[i]+hk1*dt2
				Vk2=fV(Vaux,naux,maux,haux,Io)
				iV=int(math.floor(Vaux+100.5))
				a=abcoeff[iV][0]
				BA=a+abcoeff[iV][1]
				nk2=a-naux*BA
				a=abcoeff[iV][2]
				BA=a+abcoeff[iV][3]
				mk2=a-maux*BA
				a=abcoeff[iV][4]
				BA=a+abcoeff[iV][5]
				hk2=a-haux*BA
				
				Vaux=V[i]+Vk2*dt2
				naux=n[i]+nk2*dt2
				maux=m[i]+mk2*dt2
				haux=h[i]+hk2*dt2
				Vk3=fV(Vaux,naux,maux,haux,Io)
				iV=int(math.floor(Vaux+100.5))
				a=abcoeff[iV][0]
				BA=a+abcoeff[iV][1]
				nk3=a-naux*BA
				a=abcoeff[iV][2]
				BA=a+abcoeff[iV][3]
				mk3=a-maux*BA
				a=abcoeff[iV][4]
				BA=a+abcoeff[iV][5]
				hk3=a-haux*BA
				
				Vaux=V[i]+Vk3*dt
				naux=n[i]+nk3*dt
				maux=m[i]+mk3*dt
				haux=h[i]+hk3*dt
				Vk4=fV(Vaux,naux,maux,haux,Io)
				iV=int(math.floor(Vaux+100.5))
				a=abcoeff[iV][0]
				BA=a+abcoeff[iV][1]
				nk4=a-naux*BA
				a=abcoeff[iV][2]
				BA=a+abcoeff[iV][3]
				mk4=a-maux*BA
				a=abcoeff[iV][4]
				BA=a+abcoeff[iV][5]
				hk4=a-haux*BA
				
				V.append(V[i]+((Vk1+2.0*(Vk2+Vk3)+Vk4)/6.0)*dt)
				n.append(n[i]+((nk1+2.0*(nk2+nk3)+nk4)/6.0)*dt)
				m.append(m[i]+((mk1+2.0*(mk2+mk3)+mk4)/6.0)*dt)
				h.append(h[i]+((hk1+2.0*(hk2+hk3)+hk4)/6.0)*dt)
			 
				i=i+1
		return np.asarray(t),np.asarray(V)
		
def HHTEE(dt,to,T,Io,gBarK,gBarNa,gBarL,EK,ENa,EL,C):
		#an,bn,am,bm,ah,bh
		abcoeff=[]
		i=-100
		while i<=201:
				vector=[]
				for j in range(4):
						vector.append(alphan(i))
						vector.append(bethan(i))
						vector.append(alpham(i))
						vector.append(betham(i))
						vector.append(alphah(i))
						vector.append(bethah(i))
				abcoeff.append(vector)
				i=i+1
				
		t=[]
		n=[]
		m=[]
		h=[]
		V=[]
		t.append(to)
		V.append(0.0)
		iV=int(math.floor(V[0]+100.5))
		n.append(abcoeff[iV][0]/(abcoeff[iV][0]+abcoeff[iV][1]))
		m.append(abcoeff[iV][2]/(abcoeff[iV][2]+abcoeff[iV][3]))
		h.append(abcoeff[iV][4]/(abcoeff[iV][4]+abcoeff[iV][5]))
		i=0
		gl=gBarL*EL
		while t[i]<=T:
				iV=int(math.floor(V[i]+100.5))
				t.append(t[i]+dt)
				
				A=abcoeff[iV][0]
				B=A+abcoeff[iV][1]
				BA=A/B
				n.append((n[i]-BA)*math.exp(-B*dt)+BA)
				
				A=abcoeff[iV][2]
				B=A+abcoeff[iV][3]
				BA=A/B
				m.append((m[i]-BA)*math.exp(-B*dt)+BA)
				
				A=abcoeff[iV][4]
				B=A+abcoeff[iV][5]
				BA=A/B
				h.append((h[i]-BA)*math.exp(-B*dt)+BA)
				
				gK=gBarK*n[i]*n[i]*n[i]*n[i]
				gNa=gBarNa*m[i]*m[i]*m[i]*h[i]
				
				B=gK+gNa+gBarL
				BA=(gK*EK+gNa*ENa+gl+Io)/B
				V.append((V[i]-BA)*math.exp(-B*dt)+BA)
				i=i+1
		return np.asarray(t),np.asarray(V)
		
def fV(V,n,m,dt,Io):
		gK=gBarK*n*n*n*n
		gNa=gBarNa*m*m*m*dt
		return Io-gK*(V-EK)-gNa*(V-ENa)-gBarL*(V-EL)
		
def alpham(V):
		if V==25.0:
				return 1.0
		else:
				a=2.5-0.1*V
				return a/(math.exp(a)-1.0)

def alphan(V):
		if V==10.0:
				return 0.1
		else:
				return (0.1-0.01*V)/(math.exp(1.0-0.1*V)-1.0)

def alphah(V):
		return 0.07*math.exp(-V/20.0)
		
def betham(V):
		return 4.0*math.exp(-V/18.0)

def bethan(V):
		return 0.125*math.exp(-V/80.0)

def bethah(V):
		return 1.0/(math.exp(3.0-0.1*V)+1.0)
		
T=1000.0
to=0.0
Io=10.5 #10.5-->70Hz, 22.5-->90Hz, 54.3-->120Hz
gBarK=36.0
gBarNa=120.0
gBarL=0.3
EK=-12.0
ENa=115.0
EL=10.6
C=1.0
Vth=32.0

dt=1

t,V=HHTFE(dt=dt,to=to,T=T,Io=Io,gBarK=gBarK,gBarNa=gBarNa,gBarL=gBarL,EK=EK,ENa=ENa,EL=EL,C=C)

csvfile = csv.writer(open("Voltage-HHT-FE-"+str(dt)+".csv", "w"))
csvfile.writerow(['Time', 'Voltage'])
for i in range(len(t)):
		csvfile.writerow([t[i],V[i]])

SpikeTimes=[]
crossVth=np.logical_and(V[:-1]>=Vth,V[1:]<Vth)
SpikeTimes = t[crossVth]

csvfile = csv.writer(open("Spike-Timing-HHT-FE-"+str(dt)+".csv", "w"))
csvfile.writerow(["Time"])
for i in range(len(SpikeTimes)):
		csvfile.writerow([SpikeTimes[i]])