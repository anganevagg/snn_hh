# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:28:51 2022

@authors: Sergio Valadez-Godínez, Marco Antonio González Meza and Juan Adrián Vázquez Pérez
"""
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk

global T
global dt
global to
global Vo
global I

global LIF_Vrest
global LIF_Vth
global LIF_a
global LIF_b

global IZH_Vpeak
global IZH_a
global IZH_b
global IZH_c
global IZH_d

global HH_gBarNa
global HH_gBarK
global HH_gBarL
global HH_VNa
global HH_VK
global HH_VL
global HH_Cm

def Main_View():
    Main_View=tk.Tk()
    Main_View.title("Spiking Neuron Simulator")
    Main_View.resizable(0,0)

    Main_Frame=tk.Frame(Main_View,width=512,height=256)
    Main_Frame.pack()
   
    #Etiquetas ventana SN_View
    labelTop=tk.Label(Main_View,font='Helvetica 8 bold',text="Spiking neuron model:")
    labelTop.place(x=10,y=10)
  
    #Botones interfaz SN_View
    tk.Button(Main_View,text="Leaky Integrate-and-Fire",command=LIF_Configuration_View).place(x=10,y=50)
    tk.Button(Main_View,text="Izhikevich",command=IZH_Configuration_View).place(x=10,y=90)
    tk.Button(Main_View,text="Hodgkin-Huxley",command=HH_Configuration_View).place(x=10,y=130)

    Main_View.mainloop()
    

def LIF_Configuration_View():
    def Get_SN_Parameters():
        global T
        global dt
        global to
        global Vo
        global I

        global LIF_Vrest
        global LIF_Vth
        global LIF_a
        global LIF_b
        
        method=float(Solver_Combo.current())
        
        T=float(TEntry.get())
        dt=float(dtEntry.get())
        to=float(toEntry.get())
        Vo=float(VoEntry.get())
        
        I=float(IEntry.get())

        LIF_Vrest=float(VrestEntry.get())
        LIF_Vth=float(VthEntry.get())
        LIF_a=float(aEntry.get())
        LIF_b=float(bEntry.get())

        t,V=LIF(dt,method)
        Plotting_View(t,V,"Leaky Integrate-and-Fire model")
        
    model_name="Leaky Integrate-and-Fire model"
    
    Solver_List = ["Forward Euler",
             "Backward Euler",
             "Implicit midpoint",
             "Midpoint",
             "Heun",
             "Crank-Nicolson",
             "Ralston",
             "Hammer-Hollingsworth",
             "Heun 3rd order",
             "Runge-Kutta 3rd order",
             "Runge-Kutta 4th order",
             "Runge-Kutta 4rd order 3/8",
             "Runge-Kutta 5th order"]
          
    SN_View=tk.Tk()
    SN_View.title(model_name)
    SN_View.resizable(0,0)

    SN_Frame=tk.Frame(SN_View,width=800,height=1000)
    SN_Frame.pack()
     
    SN_Parameters_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',text="Spiking neuron parameters:")
    SN_Parameters_Label.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky="sw")

    VoLabel=tk.Label(SN_Frame,text="Initial membrane potential (Vo):")
    VoLabel.grid(row=1,column=0,padx=10,pady=10,sticky="sw")
    VoEntry=tk.Entry(SN_Frame)
    VoEntry.grid(row=1,column=1,padx=10,pady=10)
    VoEntry.insert(0, "0.0")
    

    ILabel = tk.Label(SN_Frame,text="Input current (I):")
    ILabel.grid(row=2,column=0,padx=10,pady=10,sticky="sw")    
    IEntry=tk.Entry(SN_Frame)
    IEntry.grid(row=2,column=1,padx=10,pady=10)
    IEntry.insert(0, "0.135")

    VrestLabel=tk.Label(SN_Frame,text="Resting potential (Vrest):")
    VrestLabel.grid(row=3,column=0,padx=10,pady=10,sticky="sw")
    VrestEntry=tk.Entry(SN_Frame)
    VrestEntry.grid(row=3,column=1,padx=10,pady=10)
    VrestEntry.insert(0, "0.0")

    VthLabel=tk.Label(SN_Frame,text="Voltage threshold (Vth):")
    VthLabel.grid(row=4,column=0,padx=10,pady=10,sticky="sw")
    VthEntry=tk.Entry(SN_Frame)
    VthEntry.grid(row=4,column=1,padx=10,pady=10)
    VthEntry.insert(0, "1.0")

    aLabel = tk.Label(SN_Frame,text="a:")
    aLabel.grid(row=5,column=0, padx=10,pady=10, sticky="sw")
    aEntry = tk.Entry(SN_Frame)
    aEntry.grid(row=5,column=1,padx=10,pady=10)
    aEntry.insert(0, "0.0")

    bLabel = tk.Label(SN_Frame,text="b:")
    bLabel.grid(row=6,column=0,padx=10,pady=10,sticky="sw")
    bEntry = tk.Entry(SN_Frame)
    bEntry.grid(row=6,column=1,padx=10,pady=10)
    bEntry.insert(0, "0.1")

    Solver_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',text="Numerical solver:")
    Solver_Label.grid(row=0,column=2,padx=10,pady=10,sticky="sw")
    Solver_Combo=ttk.Combobox(SN_Frame)
    Solver_Combo.grid(row=1,column=2,padx=10,pady=10,sticky="sw")
    Solver_Combo['values']=Solver_List
    Solver_Combo.current(0)
    
    Solver_Parameters_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',anchor="center",text="Numerical solver parameters:")
    Solver_Parameters_Label.grid(row=2,column=2,columnspan=2,padx=10,pady=10,sticky="sw")
    
    dtLabel=tk.Label(SN_Frame,text="Time step (dt):")
    dtLabel.grid(row=3,column=2,padx=10,pady=10,sticky="sw")
    dtEntry=tk.Entry(SN_Frame)
    dtEntry.grid(row=3,column=3,padx=10,pady=10)
    dtEntry.insert(0, "0.01")
    
    TLabel=tk.Label(SN_Frame,text="Time span (T):")
    TLabel.grid(row=4,column=2,padx=10,pady=10,sticky="sw")
    TEntry=tk.Entry(SN_Frame)
    TEntry.grid(row=4,column=3,padx=10,pady=10)
    TEntry.insert(0, "100")

    toLabel=tk.Label(SN_Frame,text="Initial time (to):")
    toLabel.grid(row=5,column=2, padx=10,pady=10,sticky="sw")
    toEntry=tk.Entry(SN_Frame)
    toEntry.grid(row=5,column=3,padx=10,pady=10)
    toEntry.insert(0, "0.0")
    
    SN_Simulation_Button=tk.Button(SN_Frame,text="Simulate",command=Get_SN_Parameters)
    SN_Simulation_Button.grid(row=12,column=0,columnspan=4,padx=10, pady=10)
    

def IZH_Configuration_View():
    def Get_SN_Parameters():
        global T
        global dt
        global to
        global Vo
        global I

        global IZH_Vpeak
        global IZH_a
        global IZH_b
        global IZH_c
        global IZH_d
        
        method=float(Solver_Combo.current())
        
        T=float(TEntry.get())
        dt=float(dtEntry.get())
        to=float(toEntry.get())
        Vo=float(VoEntry.get())
        
        I=float(IEntry.get())

        IZH_Vpeak=float(VpeakEntry.get())
        IZH_a=float(aEntry.get())
        IZH_b=float(bEntry.get())
        IZH_c=float(cEntry.get())
        IZH_d=float(dEntry.get())

        t,V=IZH(dt,method)
        Plotting_View(t,V,"Izhikevich model")

    Solver_List = ["Forward Euler",
             "Backward Euler",
             "Implicit midpoint",
             "Midpoint",
             "Heun",
             "Crank-Nicolson",
             "Ralston",
             "Hammer-Hollingsworth",
             "Heun 3rd order",
             "Runge-Kutta 3rd order",
             "Runge-Kutta 4th order",
             "Runge-Kutta 4rd order 3/8",
             "Runge-Kutta 5th order"]
    
    model_name="Izhikevich model"
          
    SN_View=tk.Tk()
    SN_View.title(model_name)
    SN_View.resizable(0,0)

    SN_Frame=tk.Frame(SN_View,width=800,height=1000)
    SN_Frame.pack()
     
    SN_Parameters_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',text="Spiking neuron parameters:")
    SN_Parameters_Label.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky="sw")

    VoLabel=tk.Label(SN_Frame,text="Initial membrane potential (Vo):")
    VoLabel.grid(row=1,column=0,padx=10,pady=10,sticky="sw")
    VoEntry=tk.Entry(SN_Frame)
    VoEntry.grid(row=1,column=1,padx=10,pady=10)
    VoEntry.insert(0, "0.0")
    
    ILabel = tk.Label(SN_Frame,text="Input current (I):")
    ILabel.grid(row=2,column=0,padx=10,pady=10,sticky="sw")    
    IEntry=tk.Entry(SN_Frame)
    IEntry.grid(row=2,column=1,padx=10,pady=10)
    IEntry.insert(0, "27.0")

    VpeakLabel=tk.Label(SN_Frame,text="Voltage peak (Vpeak):")
    VpeakLabel.grid(row=3,column=0,padx=10,pady=10,sticky="sw")
    VpeakEntry=tk.Entry(SN_Frame)
    VpeakEntry.grid(row=3,column=1,padx=10,pady=10)
    VpeakEntry.insert(0, "30.0")

    aLabel = tk.Label(SN_Frame,text="a:")
    aLabel.grid(row=4,column=0, padx=10,pady=10, sticky="sw")
    aEntry = tk.Entry(SN_Frame)
    aEntry.grid(row=4,column=1,padx=10,pady=10)
    aEntry.insert(0, "0.02")

    bLabel = tk.Label(SN_Frame,text="b:")
    bLabel.grid(row=5,column=0,padx=10,pady=10,sticky="sw")
    bEntry = tk.Entry(SN_Frame)
    bEntry.grid(row=5,column=1,padx=10,pady=10)
    bEntry.insert(0, "0.2")
    
    cLabel = tk.Label(SN_Frame,text="c:")
    cLabel.grid(row=6,column=0,padx=10,pady=10,sticky="sw")
    cEntry = tk.Entry(SN_Frame)
    cEntry.grid(row=6,column=1,padx=10,pady=10)
    cEntry.insert(0, "-65.0")
    
    dLabel = tk.Label(SN_Frame,text="d:")
    dLabel.grid(row=7,column=0,padx=10,pady=10,sticky="sw")
    dEntry = tk.Entry(SN_Frame)
    dEntry.grid(row=7,column=1,padx=10,pady=10)
    dEntry.insert(0, "8")
 
    Solver_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',text="Numerical solver:")
    Solver_Label.grid(row=0,column=2,padx=10,pady=10,sticky="sw")
    Solver_Combo=ttk.Combobox(SN_Frame)
    Solver_Combo.grid(row=1,column=2,padx=10,pady=10,sticky="sw")
    Solver_Combo['values']=Solver_List
    Solver_Combo.current(0)
    
    Solver_Parameters_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',anchor="center",text="Numerical solver parameters:")
    Solver_Parameters_Label.grid(row=2,column=2,columnspan=2,padx=10,pady=10,sticky="sw")
    
    dtLabel=tk.Label(SN_Frame,text="Time step (dt):")
    dtLabel.grid(row=3,column=2,padx=10,pady=10,sticky="sw")
    dtEntry=tk.Entry(SN_Frame)
    dtEntry.grid(row=3,column=3,padx=10,pady=10)
    dtEntry.insert(0, "0.01")
    
    TLabel=tk.Label(SN_Frame,text="Time span (T):")
    TLabel.grid(row=4,column=2,padx=10,pady=10,sticky="sw")
    TEntry=tk.Entry(SN_Frame)
    TEntry.grid(row=4,column=3,padx=10,pady=10)
    TEntry.insert(0, "100")

    toLabel=tk.Label(SN_Frame,text="Initial time (to):")
    toLabel.grid(row=5,column=2, padx=10,pady=10,sticky="sw")
    toEntry=tk.Entry(SN_Frame)
    toEntry.grid(row=5,column=3,padx=10,pady=10)
    toEntry.insert(0, "0.0")
    
    SN_Simulation_Button=tk.Button(SN_Frame,text="Simulate",command=Get_SN_Parameters)
    SN_Simulation_Button.grid(row=12,column=0,columnspan=4,padx=10, pady=10)


def HH_Configuration_View():
    def Get_SN_Parameters():
        global T
        global dt
        global to
        global Vo
        global I

        global HH_gBarNa
        global HH_gBarK
        global HH_gBarL
        global HH_VNa
        global HH_VK
        global HH_VL
        global HH_Cm
        
        method=float(Solver_Combo.current())
        
        T=float(TEntry.get())
        dt=float(dtEntry.get())
        to=float(toEntry.get())
        Vo=float(VoEntry.get())
        
        I=float(IEntry.get())

        HH_gBarNa=float(gBarNaEntry.get())
        HH_gBarK=float(gBarKEntry.get())
        HH_gBarL=float(gBarLEntry.get())
        HH_VNa=float(VNaEntry.get())
        HH_VK=float(VKEntry.get())
        HH_VL=float(VLEntry.get())
        HH_Cm=float(CmEntry.get())

        t,V=HH(dt,method)
        Plotting_View(t,V,"Hodgkin-Huxley model")

    Solver_List = ["Forward Euler",
             "Backward Euler",
             "Implicit midpoint",
             "Midpoint",
             "Heun",
             "Crank-Nicolson",
             "Ralston",
             "Hammer-Hollingsworth",
             "Heun 3rd order",
             "Runge-Kutta 3rd order",
             "Runge-Kutta 4th order",
             "Runge-Kutta 4rd order 3/8",
             "Runge-Kutta 5th order"]
    
    model_name="Hodgkin-Huxley model"
          
    SN_View=tk.Tk()
    SN_View.title(model_name)
    SN_View.resizable(0,0)

    SN_Frame=tk.Frame(SN_View,width=800,height=1000)
    SN_Frame.pack()
     
    SN_Parameters_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',text="Spiking neuron parameters:")
    SN_Parameters_Label.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky="sw")
    
    VoLabel=tk.Label(SN_Frame,text="Initial membrane potential (Vo):")
    VoLabel.grid(row=1,column=0,padx=10,pady=10,sticky="sw")
    VoEntry=tk.Entry(SN_Frame)
    VoEntry.grid(row=1,column=1,padx=10,pady=10)
    VoEntry.insert(0, "0.0")
    
    ILabel = tk.Label(SN_Frame,text="Input current (I):")
    ILabel.grid(row=2,column=0,padx=10,pady=10,sticky="sw")    
    IEntry=tk.Entry(SN_Frame)
    IEntry.grid(row=2,column=1,padx=10,pady=10)
    IEntry.insert(0, "9.5")
    
    gBarKLabel=tk.Label(SN_Frame,text="Potassium conductance (gK):")
    gBarKLabel.grid(row=3,column=0,padx=10,pady=10,sticky="sw")
    gBarKEntry=tk.Entry(SN_Frame)
    gBarKEntry.grid(row=3,column=1,padx=10,pady=10)
    gBarKEntry.insert(0, "36.0")

    gBarNaLabel=tk.Label(SN_Frame,text="Sodium conductance (gNA):")
    gBarNaLabel.grid(row=4,column=0,padx=10,pady=10,sticky="sw")
    gBarNaEntry=tk.Entry(SN_Frame)
    gBarNaEntry.grid(row=4,column=1,padx=10,pady=10)
    gBarNaEntry.insert(0, "120.0")
        
    gBarLLabel=tk.Label(SN_Frame,text="Leak conductance (gL):")
    gBarLLabel.grid(row=5,column=0,padx=10,pady=10,sticky="sw")
    gBarLEntry=tk.Entry(SN_Frame)
    gBarLEntry.grid(row=5,column=1,padx=10,pady=10)
    gBarLEntry.insert(0, "0.3")
    
    VKLabel=tk.Label(SN_Frame,text="Potassium reversal potential (VK):")
    VKLabel.grid(row=6,column=0,padx=10,pady=10,sticky="sw")
    VKEntry=tk.Entry(SN_Frame)
    VKEntry.grid(row=6,column=1,padx=10,pady=10)
    VKEntry.insert(0, "-12.0")
    
    VNaLabel=tk.Label(SN_Frame,text="Sodium reversal potential (VNa):")
    VNaLabel.grid(row=7,column=0,padx=10,pady=10,sticky="sw")
    VNaEntry=tk.Entry(SN_Frame)
    VNaEntry.grid(row=7,column=1,padx=10,pady=10)
    VNaEntry.insert(0, "115.0")
        
    VLLabel=tk.Label(SN_Frame,text="Leak reversal potential (VL):")
    VLLabel.grid(row=8,column=0,padx=10,pady=10,sticky="sw")
    VLEntry=tk.Entry(SN_Frame)
    VLEntry.grid(row=8,column=1,padx=10,pady=10)
    VLEntry.insert(0, "10.613")
    
    CmLabel=tk.Label(SN_Frame,text="Membrane capacitance (Cm):")
    CmLabel.grid(row=9,column=0,padx=10,pady=10,sticky="sw")
    CmEntry=tk.Entry(SN_Frame)
    CmEntry.grid(row=9,column=1,padx=10,pady=10)
    CmEntry.insert(0, "1.0")

    Solver_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',text="Numerical solver:")
    Solver_Label.grid(row=0,column=2,padx=10,pady=10,sticky="sw")
    Solver_Combo=ttk.Combobox(SN_Frame)
    Solver_Combo.grid(row=1,column=2,padx=10,pady=10,sticky="sw")
    Solver_Combo['values']=Solver_List
    Solver_Combo.current(0)
    
    Solver_Parameters_Label=tk.Label(SN_Frame,font='Helvetica 10 bold',anchor="center",text="Numerical solver parameters:")
    Solver_Parameters_Label.grid(row=2,column=2,columnspan=2,padx=10,pady=10,sticky="sw")
    
    dtLabel=tk.Label(SN_Frame,text="Time step (dt):")
    dtLabel.grid(row=3,column=2,padx=10,pady=10,sticky="sw")
    dtEntry=tk.Entry(SN_Frame)
    dtEntry.grid(row=3,column=3,padx=10,pady=10)
    dtEntry.insert(0, "0.01")
    
    TLabel=tk.Label(SN_Frame,text="Time span (T):")
    TLabel.grid(row=4,column=2,padx=10,pady=10,sticky="sw")
    TEntry=tk.Entry(SN_Frame)
    TEntry.grid(row=4,column=3,padx=10,pady=10)
    TEntry.insert(0, "100")

    toLabel=tk.Label(SN_Frame,text="Initial time (to):")
    toLabel.grid(row=5,column=2, padx=10,pady=10,sticky="sw")
    toEntry=tk.Entry(SN_Frame)
    toEntry.grid(row=5,column=3,padx=10,pady=10)
    toEntry.insert(0, "0.0")
    
    SN_Simulation_Button=tk.Button(SN_Frame,text="Simulate",command=Get_SN_Parameters)
    SN_Simulation_Button.grid(row=12,column=0,columnspan=4,padx=10, pady=10)


def Plotting_View(t,V,model_name):
    LIF_Plotting_View = tk.Tk()
    LIF_Plotting_View.title(model_name)
    LIF_Plotting_View.resizable(height = None, width = None)
        
    fig = plt.figure(dpi=100)
    fig.tight_layout()
    
    SN_Frame=tk.Frame(LIF_Plotting_View,width=800,height=800)
    SN_Frame.pack()
    
    canvas=FigureCanvasTkAgg(fig,master = SN_Frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both',expand=True)
    
    toolbar = NavigationToolbar2Tk(canvas, SN_Frame)
    toolbar.update()

    plt.plot(t,V)
    plt.title(model_name)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    

def LIF(dt,method):
    global T
    global to
    global Vo
    global I
    
    global LIF_Vrest
    global LIF_Vth
    global LIF_a
    global LIF_b
    
    t=[]
    V=[]
    t.append(to)
    V.append(Vo)
    
    i=0

    if method==4:
        k=LIF_fV(V[0])
        V.append(V[0]+k*dt)
        t.append(t[0]+dt)
        i=1  
        
    while t[i]<=T:
        
        if method==0:
            V.append(LIF_fFE(dt,V[i],LIF_fV))
        elif method==1:
            V.append(LIF_fBE(dt,V[i],LIF_fA,LIF_fB))            
        elif method==2:
            V.append(LIF_fIMP(dt,V[i],LIF_fV,LIF_fA))
        elif method==3:
            V.append(LIF_fMP(dt,V[i],LIF_fV))
        elif method==4:
            V.append(LIF_fHE(dt,V[i],LIF_fV))
        elif method==5:
            V.append(LIF_fCN(dt,V[i],LIF_fV,LIF_fA,LIF_fB))
        elif method==6:
            V.append(LIF_fRA(dt,V[i],LIF_fV))
        elif method==7:
            V.append(LIF_fHAH(dt,V[i],LIF_fV,LIF_fA))            
        elif method==8:
            V.append(LIF_fHE3(dt,V[i],LIF_fV))            
        elif method==9:
            V.append(LIF_fRK3(dt,V[i],LIF_fV))
        elif method==10:
            V.append(LIF_fRK4(dt,V[i],LIF_fV))            
        elif method==11:
            V.append(LIF_fRK438(dt,V[i],LIF_fV))            
        elif method==12:
            V.append(LIF_fRK5(dt,V[i],LIF_fV))

        if(V[i+1]>=LIF_Vth):
            V[i+1]=LIF_Vrest
        t.append(t[i]+dt)
        i=i+1
    return(np.asarray(t),np.asarray(V))

#0 Explicit
def LIF_fFE(dt,x,f):#Forward Euler
    k1=f(x)
    return x+k1*dt

#1 Implicit
def LIF_fBE(dt,x,fA,fB):#Backward Euler
    return (x+dt*fB())/(1.0+fA()*dt)
    
#2 Implicit
def LIF_fIMP(dt,x,f,fA):#Implicit Mid Point
    k1=f(x)/(1.0+0.5*fA()*dt)
    return x+k1*dt
    
#3 Explicit  
def LIF_fMP(dt,x,f):#Mid Point
    k1=f(x)
    k2=f(x+0.5*k1*dt)
    return x+k2*dt

#4 Explicit   
def LIF_fHE(dt,x,f):#Heun or Modified Euler
    k1=f(x)
    k2=f(x+k1*dt)
    return x+(0.5*(k1+k2))*dt
    
#5 Implicit
def LIF_fCN(dt,x,f,fA,fB):#Crank-Nicolson trapezoidal rule
    return (x+0.5*(f(x)+fB())*dt)/(1.0+0.5*fA()*dt)

#6 Explicit
def LIF_fRA(dt,x,f):#Ralston
    k1=f(x)
    k2=f(x+0.75*k1*dt)
    return x+((k1+2.0*k2)/3.0)*dt
    
#7 Implicit
def LIF_fHAH(dt,x,f,fA):#Hammer-Hollingsworth
    k1=f(x)
    k2=(k1-fA()*(1.0/3.0)*k1*dt)/(1.0+(1.0/3.0)*fA()*dt)
    return x+0.25*(k1+3.0*k2)*dt
    
#8 Explicit
def LIF_fHE3(dt,x,f):#Heun 3rd order
    k1=f(x)
    k2=f(x+k1*dt/3.0)
    k3=f(x+2.0*k2*dt/3.0)
    return x+((k1+3.0*k3)/4.0)*dt

#9 Explicit
def LIF_fRK3(dt,x,f):#Runge-Kutta 3rd order
    k1=f(x)
    k2=f(x+0.5*k1*dt)
    k3=f(x+(2.0*k2-k1)*dt)
    return x+((k1+4.0*k2+k3)/6.0)*dt

#10 Explicit
def LIF_fRK4(dt,x,f):#Runge-Kutta 4th order
    k1=f(x)
    k2=f(x+k1*0.5*dt)
    k3=f(x+k2*0.5*dt)
    k4=f(x+k3*dt)
    return x+((k1+2.0*(k2+k3)+k4)/6.0)*dt

#11 Explicit
def LIF_fRK438(dt,x,f):#Runge-Kutta 4rd order 3/8
    k1=f(x)
    k2=f(x+(k1/3.0)*dt)
    k3=f(x+(k2-k1/3.0)*dt)
    k4=f(x+(k1-k2+k3)*dt)
    return x+((k1+3.0*(k2+k3)+k4)/8.0)*dt

#12 Explicit
def LIF_fRK5(dt,x,f):#Runge-Kutta 5th order
    k1=f(x)
    k2=f(x+0.25*k1*dt)
    k3=f(x+(0.125*(k1+k2))*dt)
    k4=f(x+(k3-0.5*k2)*dt)
    k5=f(x+(0.1875*k1+0.5625*k4)*dt)
    k6=f(x+((2.0*k2+12.0*(k3-k4)+8.0*k5-3.0*k1)/7.0)*dt)
    return x+((7.0*k1+32.0*k3+12.0*k4+32.0*k5+7.0*k6)/90.0)*dt

def LIF_fV(V):
    return LIF_a+I-LIF_b*V
    
def LIF_fA():
    return LIF_b
    
def LIF_fB():
    return LIF_a+I

def IZH(dt,method):
    global T
    global to
    global Vo
    global I
    
    global IZH_Vpeak
    global IZH_a
    global IZH_b
    global IZH_c
    global IZH_d
    
    t=[]
    V=[]
    u=[]
    t.append(to)
    V.append(Vo)
    u.append(IZH_b*Vo)
    
    i=0

    if method==4:
        k=IZH_fV(V[0],u[0])
        V.append(V[0]+k*dt)
        k=IZH_fu(u[0],V[0])
        u.append(u[0]+k*dt)
        t.append(t[0]+dt)
        i=1  
        
    while t[i]<=T:
        
        if method==0:
            V.append(IZH_fFE(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fFE(dt,u[i],V[i],IZH_fu))
        elif method==1:
            V.append(IZH_fBE(dt,V[i],u[i],IZH_fAV,IZH_fBV))
            u.append(IZH_fBE(dt,u[i],V[i],IZH_fAu,IZH_fBu))
        elif method==2:
            V.append(IZH_fIMP(dt,V[i],u[i],IZH_fV,IZH_fAV))
            u.append(IZH_fIMP(dt,u[i],V[i],IZH_fu,IZH_fAu))
        elif method==3:
            V.append(IZH_fMP(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fMP(dt,u[i],V[i],IZH_fu))
        elif method==4:
            V.append(IZH_fH(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fH(dt,u[i],V[i],IZH_fu))
        elif method==5:
            V.append(IZH_fCN(dt,V[i],u[i],IZH_fV,IZH_fAV,IZH_fBV))
            u.append(IZH_fCN(dt,u[i],V[i],IZH_fu,IZH_fAu,IZH_fBu))
        elif method==6:
            V.append(IZH_fR(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fR(dt,u[i],V[i],IZH_fu))
        elif method==7:
            V.append(IZH_fHAMH(dt,V[i],u[i],IZH_fV,IZH_fAV))
            u.append(IZH_fHAMH(dt,u[i],V[i],IZH_fu,IZH_fAu))
        elif method==8:
            V.append(IZH_fH3(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fH3(dt,u[i],V[i],IZH_fu))            
        elif method==9:
            V.append(IZH_fRK3(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fRK3(dt,u[i],V[i],IZH_fu))
        elif method==10:
            V.append(IZH_fRK4(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fRK4(dt,u[i],V[i],IZH_fu))
        elif method==11:
            V.append(IZH_fRK438(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fRK438(dt,u[i],V[i],IZH_fu))
        elif method==12:
            V.append(IZH_fRK5(dt,V[i],u[i],IZH_fV))
            u.append(IZH_fRK5(dt,u[i],V[i],IZH_fu))
        
        if(V[i+1]>=IZH_Vpeak):
            V[i]=IZH_Vpeak
            V[i+1]=IZH_c
            u[i+1]=u[i+1]+IZH_d
        t.append(t[i]+dt)
        i=i+1
    return(np.asarray(t),np.asarray(V))

#0 Explicit
def IZH_fFE(dt,x,y,f):#Forward Euler
    k1=f(x,y)
    return x+k1*dt

#1 Implicit
def IZH_fBE(dt,x,y,fA,fB):#Backward Euler
    return (x+dt*fB(y))/(1.0+fA(x)*dt)

#2 Implicit
def IZH_fIMP(dt,x,y,f,fA):#Implicit Mid Point
    k1=f(x,y)/(1.0+0.5*fA(x)*dt)
    return x+k1*dt
    
#3 Explicit  
def IZH_fMP(dt,x,y,f):#Mid Point
    k1=f(x,y)
    k2=f(x+0.5*k1*dt,y)
    return x+k2*dt

#4 Explicit 
def IZH_fH(dt,x,y,f):#Heun or Modified Euler
    k1=f(x,y)
    k2=f(x+k1*dt,y)
    return x+(0.5*(k1+k2))*dt

#5 Implicit
def IZH_fCN(dt,x,y,f,fA,fB):#Crank-Nicolson trapezoidal rule
    return (x+0.5*(f(x,y)+fB(y))*dt)/(1.0+0.5*fA(x)*dt)    

#6 Explicit
def IZH_fR(dt,x,y,f):#Ralston
    k1=f(x,y)
    k2=f(x+0.75*k1*dt,y)
    return x+((k1+2.0*k2)/3.0)*dt
    
#7 Implicit
def IZH_fHAMH(dt,x,y,f,fA):#Hammer-Hollingsworth
    k1=f(x,y)
    k2=(k1-fA(x)*(1.0/3.0)*k1*dt)/(1.0+(1.0/3.0)*fA(x)*dt)
    return x+0.25*(k1+3.0*k2)*dt
    
#8 Explicit
def IZH_fH3(dt,x,y,f):#Heun 3rd order
    k1=f(x,y)
    k2=f(x+k1*dt/3.0,y)
    k3=f(x+2.0*k2*dt/3.0,y)
    return x+((k1+3.0*k3)/4.0)*dt

#9 Explicit
def IZH_fRK3(dt,x,y,f):#Runge-Kutta 3rd order
    k1=f(x,y)
    k2=f(x+0.5*k1*dt,y)
    k3=f(x+(2.0*k2-k1)*dt,y)
    return x+((k1+4.0*k2+k3)/6.0)*dt

#10 Explicit
def IZH_fRK4(dt,x,y,f):#Runge-Kutta 4th order
    k1=f(x,y)
    k2=f(x+k1*0.5*dt,y)
    k3=f(x+k2*0.5*dt,y)
    k4=f(x+k3*dt,y)
    return x+((k1+2.0*(k2+k3)+k4)/6.0)*dt

#11 Explicit
def IZH_fRK438(dt,x,y,f):#Runge-Kutta 4rd order 3/8
    k1=f(x,y)
    k2=f(x+(k1/3.0)*dt,y)
    k3=f(x+(k2-k1/3.0)*dt,y)
    k4=f(x+(k1-k2+k3)*dt,y)
    return x+((k1+3.0*(k2+k3)+k4)/8.0)*dt

#12 Explicit
def IZH_fRK5(dt,x,y,f):#Runge-Kutta 5th order
    k1=f(x,y)
    k2=f(x+0.25*k1*dt,y)
    k3=f(x+(0.125*(k1+k2))*dt,y)
    k4=f(x+(k3-0.5*k2)*dt,y)
    k5=f(x+(0.1875*k1+0.5625*k4)*dt,y)
    k6=f(x+((2.0*k2+12.0*(k3-k4)+8.0*k5-3.0*k1)/7.0)*dt,y)
    return x+((7.0*k1+32.0*k3+12.0*k4+32.0*k5+7.0*k6)/90.0)*dt

def IZH_fV(V,n):
    return 0.04*math.pow(V,2.0)+5.0*V+140.0-n+I
    
def IZH_fu(u,V):
    return IZH_a*(IZH_b*V-u)
    
def IZH_fAV(V):
    return -0.04*V-5.0
    
def IZH_fBV(u):
    return 140.0-u+I
    
def IZH_fAu(u):
    return IZH_a
    
def IZH_fBu(V):
    return IZH_a*IZH_b*V

def HH(dt,method):
    global T
    global to
    global Vo
    global I

    global HH_gBarNa
    global HH_gBarK
    global HH_gBarL
    global HH_VNa
    global HH_VK
    global HH_VL
    global HH_Cm
    
    t=[]
    V=[]
    n=[]
    m=[]
    h=[]
    t.append(to)
    V.append(Vo)
    n.append(HH_alphan(V[0])/(HH_alphan(V[0])+HH_bethan(V[0])))
    m.append(HH_alpham(V[0])/(HH_alpham(V[0])+HH_betham(V[0])))
    h.append(HH_alphah(V[0])/(HH_alphah(V[0])+HH_bethah(V[0])))
    i=0

    if method==4:
        k=HH_fV(V[0],n[0],m[0],h[0])
        V.append(V[0]+k*dt)
        k=HH_fn(n[0],V[0])
        n.append(n[0]+k*dt)
        k=HH_fm(m[0],V[0])
        m.append(m[0]+k*dt)
        k=HH_fh(h[0],V[0])
        h.append(h[0]+k*dt)
        t.append(t[0]+dt)
        i=1  
        
    while t[i]<=T:
        if method==0:
            V.append(HH_fFEV(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fFEx(dt,n[i],V[i],HH_fn))
            m.append(HH_fFEx(dt,m[i],V[i],HH_fm))
            h.append(HH_fFEx(dt,h[i],V[i],HH_fh))
        elif method==1:
            V.append(HH_fBEV(dt,V[i],n[i],m[i],h[i],HH_fAV,HH_fBV))
            n.append(HH_fBEx(dt,n[i],V[i],HH_fAn,HH_fBn))
            m.append(HH_fBEx(dt,m[i],V[i],HH_fAm,HH_fBm))
            h.append(HH_fBEx(dt,h[i],V[i],HH_fAh,HH_fBh))
        elif method==2:
            V.append(HH_fIMPV(dt,V[i],n[i],m[i],h[i],HH_fV,HH_fAV))
            n.append(HH_fIMPx(dt,n[i],V[i],HH_fn,HH_fAn))
            m.append(HH_fIMPx(dt,m[i],V[i],HH_fm,HH_fAm))
            h.append(HH_fIMPx(dt,h[i],V[i],HH_fh,HH_fAh))
        elif method==3:
            V.append(HH_fMPV(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fMPx(dt,n[i],V[i],HH_fn))
            m.append(HH_fMPx(dt,m[i],V[i],HH_fm))
            h.append(HH_fMPx(dt,h[i],V[i],HH_fh))
        elif method==4:
            V.append(HH_fHV(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fHx(dt,n[i],V[i],HH_fn))
            m.append(HH_fHx(dt,m[i],V[i],HH_fm))
            h.append(HH_fHx(dt,h[i],V[i],HH_fh))
        elif method==5:
            V.append(HH_fCNV(dt,V[i],n[i],m[i],h[i],HH_fV,HH_fAV,HH_fBV))
            n.append(HH_fCNx(dt,n[i],V[i],HH_fn,HH_fAn,HH_fBn))
            m.append(HH_fCNx(dt,m[i],V[i],HH_fm,HH_fAm,HH_fBm))
            h.append(HH_fCNx(dt,h[i],V[i],HH_fh,HH_fAh,HH_fBh))
        elif method==6:
            V.append(HH_fRV(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fRx(dt,n[i],V[i],HH_fn))
            m.append(HH_fRx(dt,m[i],V[i],HH_fm))
            h.append(HH_fRx(dt,h[i],V[i],HH_fh))
        elif method==7:
            V.append(HH_fHAMHV(dt,V[i],n[i],m[i],h[i],HH_fV,HH_fAV))
            n.append(HH_fHAMHx(dt,n[i],V[i],HH_fn,HH_fAn))
            m.append(HH_fHAMHx(dt,m[i],V[i],HH_fm,HH_fAm))
            h.append(HH_fHAMHx(dt,h[i],V[i],HH_fh,HH_fAh))
        elif method==8:
            V.append(HH_fH3V(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fH3x(dt,n[i],V[i],HH_fn))      
            m.append(HH_fH3x(dt,m[i],V[i],HH_fm))
            h.append(HH_fH3x(dt,h[i],V[i],HH_fh))
        elif method==9:
            V.append(HH_fRK3V(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fRK3x(dt,n[i],V[i],HH_fn))
            m.append(HH_fRK3x(dt,m[i],V[i],HH_fm))
            h.append(HH_fRK3x(dt,h[i],V[i],HH_fh))
        elif method==10:
            V.append(HH_fRK4V(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fRK4x(dt,n[i],V[i],HH_fn))
            m.append(HH_fRK4x(dt,m[i],V[i],HH_fm))
            h.append(HH_fRK4x(dt,h[i],V[i],HH_fh))
        elif method==11:
            V.append(HH_fRK438V(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fRK438x(dt,n[i],V[i],HH_fn))
            m.append(HH_fRK438x(dt,m[i],V[i],HH_fm))
            h.append(HH_fRK438x(dt,h[i],V[i],HH_fh))
        elif method==12:
            V.append(HH_fRK5V(dt,V[i],n[i],m[i],h[i],HH_fV))
            n.append(HH_fRK5x(dt,n[i],V[i],HH_fn))
            m.append(HH_fRK5x(dt,m[i],V[i],HH_fm))
            h.append(HH_fRK5x(dt,h[i],V[i],HH_fh))
        t.append(t[i]+dt)
        i=i+1
    return(np.asarray(t),np.asarray(V))

#0 Explicit
def HH_fFEV(dt,x,y,z,w,f):#Forward Euler
    k1=f(x,y,z,w)
    return x+k1*dt

#1 Implicit
def HH_fBEV(dt,x,y,z,w,fA,fB):#Backward Euler
    return (x+dt*fB(y,z,w))/(1.0+fA(y,z,w,)*dt)

#2 Implicit
def HH_fIMPV(dt,x,y,z,w,f,fA):#Implicit Mid Point
    k1=f(x,y,z,w)/(1.0+0.5*fA(y,z,w)*dt)
    return x+k1*dt
    
#3 Explicit  
def HH_fMPV(dt,x,y,z,w,f):#Mid Point
    k1=f(x,y,z,w)
    k2=f(x+0.5*k1*dt,y,z,w)
    return x+k2*dt

#4 Explicit 
def HH_fHV(dt,x,y,z,w,f):#Heun or Modified Euler
    k1=f(x,y,z,w)
    k2=f(x+k1*dt,y,z,w)
    return x+(0.5*(k1+k2))*dt

#5 Implicit
def HH_fCNV(dt,x,y,z,w,f,fA,fB):#Crank-Nicolson trapezoidal rule
    return (x+0.5*(f(x,y,z,w)+fB(y,z,w))*dt)/(1.0+0.5*fA(y,z,w)*dt)    

#6 Explicit
def HH_fRV(dt,x,y,z,w,f):#Ralston
    k1=f(x,y,z,w)
    k2=f(x+0.75*k1*dt,y,z,w)
    return x+((k1+2.0*k2)/3.0)*dt
    
#7 Implicit
def HH_fHAMHV(dt,x,y,z,w,f,fA):#Hammer-Hollingsworth
    k1=f(x,y,z,w)
    k2=(k1-fA(y,z,w)*(1.0/3.0)*k1*dt)/(1.0+(1.0/3.0)*fA(y,z,w)*dt)
    return x+0.25*(k1+3.0*k2)*dt
    
#8 Explicit
def HH_fH3V(dt,x,y,z,w,f):#Heun 3rd order
    k1=f(x,y,z,w)
    k2=f(x+k1*dt/3.0,y,z,w)
    k3=f(x+2.0*k2*dt/3.0,y,z,w)
    return x+((k1+3.0*k3)/4.0)*dt

#9 Explicit
def HH_fRK3V(dt,x,y,z,w,f):#Runge-Kutta 3rd order
    k1=f(x,y,z,w)
    k2=f(x+0.5*k1*dt,y,z,w)
    k3=f(x+(2.0*k2-k1)*dt,y,z,w)
    return x+((k1+4.0*k2+k3)/6.0)*dt

#10 Explicit
def HH_fRK4V(dt,x,y,z,w,f):#Runge-Kutta 4th order
    k1=f(x,y,z,w)
    k2=f(x+k1*0.5*dt,y,z,w)
    k3=f(x+k2*0.5*dt,y,z,w)
    k4=f(x+k3*dt,y,z,w)
    return x+((k1+2.0*(k2+k3)+k4)/6.0)*dt

#11 Explicit
def HH_fRK438V(dt,x,y,z,w,f):#Runge-Kutta 4rd order 3/8
    k1=f(x,y,z,w)
    k2=f(x+(k1/3.0)*dt,y,z,w)
    k3=f(x+(k2-k1/3.0)*dt,y,z,w)
    k4=f(x+(k1-k2+k3)*dt,y,z,w)
    return x+((k1+3.0*(k2+k3)+k4)/8.0)*dt

#12 Explicit
def HH_fRK5V(dt,x,y,z,w,f):#Runge-Kutta 5th order
    k1=f(x,y,z,w)
    k2=f(x+0.25*k1*dt,y,z,w)
    k3=f(x+(0.125*(k1+k2))*dt,y,z,w)
    k4=f(x+(k3-0.5*k2)*dt,y,z,w)
    k5=f(x+(0.1875*k1+0.5625*k4)*dt,y,z,w)
    k6=f(x+((2.0*k2+12.0*(k3-k4)+8.0*k5-3.0*k1)/7.0)*dt,y,z,w)
    return x+((7.0*k1+32.0*k3+12.0*k4+32.0*k5+7.0*k6)/90.0)*dt
    
#0 Explicit
def HH_fFEx(dt,x,y,f):#Forward Euler
    k1=f(x,y)
    return x+k1*dt

#1 Implicit
def HH_fBEx(dt,x,y,fA,fB):#Backward Euler
    return (x+dt*fB(y))/(1.0+fA(y)*dt)

#2 Implicit
def HH_fIMPx(dt,x,y,f,fA):#Implicit Mid Point
    k1=f(x,y)/(1.0+0.5*fA(y)*dt)
    return x+k1*dt
    
#3 Explicit  
def HH_fMPx(dt,x,y,f):#Mid Point
    k1=f(x,y)
    k2=f(x+0.5*k1*dt,y)
    return x+k2*dt

#4 Explicit 
def HH_fHx(dt,x,y,f):#Heun or Modified Euler
    k1=f(x,y)
    k2=f(x+k1*dt,y)
    return x+(0.5*(k1+k2))*dt

#5 Implicit
def HH_fCNx(dt,x,y,f,fA,fB):#Crank-Nicolson trapezoidal rule
    return (x+0.5*(f(x,y)+fB(y))*dt)/(1.0+0.5*fA(y)*dt)    

#6 Explicit
def HH_fRx(dt,x,y,f):#Ralston
    k1=f(x,y)
    k2=f(x+0.75*k1*dt,y)
    return x+((k1+2.0*k2)/3.0)*dt

#7 Implicit
def HH_fHAMHx(dt,x,y,f,fA):#Hammer-Hollingsworth
    k1=f(x,y)
    k2=(k1-fA(y)*(1.0/3.0)*k1*dt)/(1.0+(1.0/3.0)*fA(y)*dt)
    return x+0.25*(k1+3.0*k2)*dt
    
#8 Explicit
def HH_fH3x(dt,x,y,f):#Heun 3rd order
    k1=f(x,y)
    k2=f(x+k1*dt/3.0,y)
    k3=f(x+2.0*k2*dt/3.0,y)
    return x+((k1+3.0*k3)/4.0)*dt

#9 Explicit
def HH_fRK3x(dt,x,y,f):#Runge-Kutta 3rd order
    k1=f(x,y)
    k2=f(x+0.5*k1*dt,y)
    k3=f(x+(2.0*k2-k1)*dt,y)
    return x+((k1+4.0*k2+k3)/6.0)*dt

#10 Explicit
def HH_fRK4x(dt,x,y,f):#Runge-Kutta 4th order
    k1=f(x,y)
    k2=f(x+k1*0.5*dt,y)
    k3=f(x+k2*0.5*dt,y)
    k4=f(x+k3*dt,y)
    return x+((k1+2.0*(k2+k3)+k4)/6.0)*dt

#11 Explicit
def HH_fRK438x(dt,x,y,f):#Runge-Kutta 4rd order 3/8
    k1=f(x,y)
    k2=f(x+(k1/3.0)*dt,y)
    k3=f(x+(k2-k1/3.0)*dt,y)
    k4=f(x+(k1-k2+k3)*dt,y)
    return x+((k1+3.0*(k2+k3)+k4)/8.0)*dt

#12 Explicit
def HH_fRK5x(dt,x,y,f):#Runge-Kutta 5th order
    k1=f(x,y)
    k2=f(x+0.25*k1*dt,y)
    k3=f(x+(0.125*(k1+k2))*dt,y)
    k4=f(x+(k3-0.5*k2)*dt,y)
    k5=f(x+(0.1875*k1+0.5625*k4)*dt,y)
    k6=f(x+((2.0*k2+12.0*(k3-k4)+8.0*k5-3.0*k1)/7.0)*dt,y)
    return x+((7.0*k1+32.0*k3+12.0*k4+32.0*k5+7.0*k6)/90.0)*dt

def HH_fV(V,n,m,h):
    gK=HH_gBarK*n*n*n*n
    gNa=HH_gBarNa*m*m*m*h
    return (-gK*(V-HH_VK)-gNa*(V-HH_VNa)-HH_gBarL*(V-HH_VL)+I)/HH_Cm
    
def HH_fn(n,V):
    return HH_alphan(V)*(1.0-n)-HH_bethan(V)*n
    
def HH_fm(m,V):
    return HH_alpham(V)*(1.0-m)-HH_betham(V)*m
    
def HH_fh(h,V):
    return HH_alphah(V)*(1.0-h)-HH_bethah(V)*h
    
def HH_fAV(n,m,h):
    gK=HH_gBarK*n*n*n*n
    gNa=HH_gBarNa*m*m*m*h
    return (gK+gNa+HH_gBarL)/HH_Cm
    
def HH_fBV(n,m,h):
    gK=HH_gBarK*n*n*n*n
    gNa=HH_gBarNa*m*m*m*h
    return (gK*HH_VK+gNa*HH_VNa+HH_gBarL*HH_VL+I)/HH_Cm
    
def HH_fAn(V):
    return HH_alphan(V)+HH_bethan(V)
    
def HH_fBn(V):
    return HH_alphan(V)
    
def HH_fAm(V):
    return HH_alpham(V)+HH_betham(V)
    
def HH_fBm(V):
    return HH_alpham(V)
    
def HH_fAh(V):
    return HH_alphah(V)+HH_bethah(V)
    
def HH_fBh(V):
    return HH_alphah(V)

def HH_alphan(v):
    if v==10.0:
        return 0.1
    else:
        return (0.01*(10.0-v))/(math.exp((10.0-v)/10.0)-1.0)

def HH_bethan(v):
    return 0.125*math.exp(-v/80.0)
    
def HH_alpham(v):
    if v==25.0:
        return 0.1
    else:
        return 0.1*(25.0-v)/(math.exp((25.0-v)/10.0)-1.0)
        
def HH_betham(v):
    return 4.0*math.exp(-v/18.0)

def HH_alphah(v):
    return 0.07*math.exp(-v/20.0)

def HH_bethah(v):
    return 1.0/(math.exp((30.0-v)/10.0)+1.0)

Main_View()