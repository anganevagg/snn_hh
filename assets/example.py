import math

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

dt=0.0001

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

def fV(V,n,m,dt,Io):
    gK=gBarK*n*n*n*n
    print(f">>>> {n} {m}")
    gNa=gBarNa*m*m*m*dt
    return Io-gK*(V-EK)-gNa*(V-ENa)-gBarL*(V-EL)

n = alphan(0)/(alphan(0) + bethan(0))
m = alpham(0)/(alpham(0) + betham(0))
h = alphah(0)/(alphah(0) + bethah(0))

print(f"{n}")
print(f"{m}")
print(f"{h}")

i = 0
V_val = 0
while i<10:
    V_val = fV(V_val, n, m, 0.0001, Io)
    n = alphan(n) * (1 - n) - bethan(n)*n
    m = alpham(m) * (1 - m) - betham(m)*m
    h = alphah(h) * (1 - h) - bethah(h)*h