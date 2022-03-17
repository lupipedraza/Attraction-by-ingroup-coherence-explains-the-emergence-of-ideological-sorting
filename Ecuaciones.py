#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 13:09:45 2021

@author: lupa
"""

#Ecuacion:
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np
from Cargar_Ecuacion import cargar_ecuaciones

'''
Condicion='max2'
enElse='SinRepulsion'
#Nombre='E='+str(tipoP)+'_'+Condicion+'_'+enElse
#tipoP=0.2

Nombre='Manhattan_'+enElse+'_'+Condicion

f, Axs = plt.subplots(3, 2, sharey=True,figsize=(9,10))

plt.subplots_adjust(left=None, bottom=None, right=0.77, top=None, wspace=0.1, hspace=0.3)
i=0
for k in [0.0,0.2,0.4,0.6,0.8,1]:
    
    def ecuacion(t,x):
        C,I,In,T=x
        #k=0.2
        dC=T*C*k/2
        dI=-T*I*k/2
        dIn=-T*In*k/2
        dT=T*k/2*(In+I-C)
        return([dC,dI,dIn,dT])
    #t_eval=np.linspace(0, 100)  
    res = solve_ivp(ecuacion, (0, 400), [2./9, 1./9, 4./9,2./9])
    #plt.gca().set_color_cycle(['darkviolet','y','r','g'])
    lineObjects=Axs[(i/2,i%2)].plot(res.t,res.y.T,linewidth=2)
    Axs[(i/2,i%2)].set_title('k='+str(round(k,2)),size=16)

    i+=1
#f.set_title('Ecuaciones',size=16)
f.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(0.75, 0.7))
#plt.savefig(Nombre+'/Ecuacion.jpg')#,bbox_inches='tight')
'''
#%%
#Ecuacion:

Condicion='2-4'
enElse='rechazo'
tipoP='lineal'
k3=0.0
K=np.arange(0.0,1-k3+0.01,0.01) #Valores k1

Finales=np.zeros((len(K),4))
i=0
h=4
for k1 in K:
    k2=1-k3-k1

    def ecuacion(t,x): #s<2/4
        C,I,A,T=x
        dC=T*C*k1*(1/16)**h+T*C*k2*(1/4)**h+T**2*k1*(1/16)**h#+k2)-C*A*k1/2
        dI=T*I*(1/16)**h*(k1)+T**2*(k1+k2)*(1/16)**h#-I*A/2*k1
        dA=-A*C*k1*(1/2)**h-A*I*k1*(1/2)**h
        dT=-C*T*k1*(1/16)**h+C*A*k1*(1/2)**h+A*I*k1*(1/2)**h-T*C*k2*(1/4)**h-T*I*k1*(1/16)**h-T**2*k2*(1/16)**h-T**2*(1/8)**h*(k1)#-dC-dI-dA
        return([dC,dI,dA,dT])
    res = solve_ivp(ecuacion, (0, 10000), [2./9, 2./9, 1./9,4./9])
    Finales[i]=res.y.T[-1]#Tomar los valores finales
    i+=1  

plt.plot(1-K-k3,Finales,linewidth=3,linestyle='--',alpha=0.7)
plt.xlabel('k',size=16)
plt.ylabel('Poblaciones Finales',size=16)
plt.title('h = '+str(h),size=16)
plt.ylim((-0.03,1.03))   
#%%


Nombre='E='+str(tipoP)+'_BC='+Condicion+'_K3='+str(k3)+'_EnElse='+enElse

f, Axs = plt.subplots(3, 2, sharey=True,figsize=(9,10))
print(Axs.shape)

plt.subplots_adjust(left=None, bottom=None, right=0.77, top=None, wspace=0.1, hspace=0.3)
i=0
k3=0
K1s=np.arange(0,1-k3+0.1,0.1)#+[0.95,1]

#K1s=[0.0,0.2,0.4,0.6,0.8,1]
Finales=np.zeros((len(K1s),4))
for k1 in K1s:
    k2=1-k1-k3
    # def ecuacion(t,x): #Max2
    #     C,I,A,T=x
    #     #k=0.2
    #     dC=T*C*k1/16+T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2
    #     dI=T*I/16*k1+T**2/16*(k1)-I*A/2*k1
    #     dA=T**2/8*(k1+k2/2)-A*C*k1/2-A*I*k1/2
    #     dT=-C*T*k1/16+C*A*k1+A*I*k1-T*C*k2*1/4-T*I*k1/16-T**2/4*(k1+k2/2)#-dC-dI-dA
    #     #if dC+dI+dA+dT>0.000001:
    #         #print(t,dC+dI+dA+dT,k1)
    #     return([dC,dI,dA,dT])
    def ecuacion(t,x): #s<2/4
        C,I,A,T=x
        #k=0.2
        dC=T*C*k1/16+T*C*k2/4+T**2/16*(k1)#+k2)-C*A*k1/2
        dI=T*I/16*k1+T**2/16*(k1+k2)#-I*A/2*k1
        dA=-A*C*k1/2-A*I*k1/2
        dT=-C*T*k1/16+C*A*k1/2+A*I*k1/2-T*C*k2*1/4-T*I*k1/16-T**2/8*(k1+k2/2)#-dC-dI-dA
        #if dC+dI+dA+dT>0.000001:
            #print(t,dC+dI+dA+dT,k1)
        return([dC,dI,dA,dT])


    #t_eval=np.linspace(0, 100)  
    res = solve_ivp(ecuacion, (0, 200), [2./9, 2./9, 1./9,4./9])
    #plt.gca().set_color_cycle(['darkviolet','y','r','g'])
    Finales[i]=res.y.T[-1]

    if i%2==0:
        print(i)
        lineObjects=Axs[int(i/4),int(i/2)%2].plot(res.t,res.y.T,linewidth=2)
        Axs[int(i/4),int(i/2)%2].set_title('k='+str(round(k1,2)),size=16)
        Axs[int(i/4),int(i/2)%2].set_ylim((-0.03,1.03))
        #print(np.sum(res.y.T[10]))
    i+=1

#f.set_title('Ecuaciones',size=16)
f.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(0.75, 0.7))
plt.savefig(Nombre+'/Ecuacion.jpg')#,bbox_inches='tight')
plt.close()

#Finales Ecuacion
#plt.gca().set_color_cycle(['darkviolet','y','r','g'])
lineObjects=plt.plot(1-K1s,Finales,marker='o',linewidth=2)
plt.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('k',size=16)
plt.ylabel('Poblaciones Finales',size=16)
plt.title('Ecuacion '+Nombre)
plt.ylim((-0.03,1.03))

plt.savefig(Nombre+'/Finales_Ecuacion.jpg',bbox_inches='tight')
plt.show()
plt.close()   

#%%


Condicion='Max2'
enElse='pass'
tipoP='lineal'
k3=0.0

Nombre='E='+str(tipoP)+'_BC='+Condicion+'_K3='+str(k3)+'_EnElse='+enElse

f, Axs = plt.subplots(3, 2, sharey=True,figsize=(9,10))
print(Axs.shape)

plt.subplots_adjust(left=None, bottom=None, right=0.77, top=None, wspace=0.1, hspace=0.3)
i=0
k3=0
K1s=np.arange(0,1-k3+0.1,0.1)#+[0.95,1]

#K1s=[0.0,0.2,0.4,0.6,0.8,1]
Finales=np.zeros((len(K1s),4))
for k1 in K1s:
    k2=1-k1-k3
    def ecuacion(t,x): #Max2
        C,I,A,T=x
        #k=0.2
        dC=T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2
        dI=T**2/16*(k1)-I*A/2*k1
        dA=T**2/8*(k1+k2/2)-A*C*k1/2-A*I*k1/2
        dT=C*A*k1+A*I*k1-T*C*k2*1/4-T**2/4*(k1+k2/2)#-dC-dI-dA
        #if dC+dI+dA+dT>0.000001:
            #print(t,dC+dI+dA+dT,k1)
        return([dC,dI,dA,dT])


    #t_eval=np.linspace(0, 100)  
    res = solve_ivp(ecuacion, (0, 200), [2./9, 2./9, 1./9,4./9])
    #plt.gca().set_color_cycle(['darkviolet','y','r','g'])
    Finales[i]=res.y.T[-1]

    if i%2==0:
        print(i)
        lineObjects=Axs[int(i/4),int(i/2)%2].plot(res.t,res.y.T,linewidth=2)
        Axs[int(i/4),int(i/2)%2].set_title('k='+str(round(k1,2)),size=16)
        Axs[int(i/4),int(i/2)%2].set_ylim((-0.03,1.03))
        #print(np.sum(res.y.T[10]))
    i+=1

#f.set_title('Ecuaciones',size=16)
f.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(0.75, 0.7))
plt.savefig(Nombre+'/Ecuacion.jpg')#,bbox_inches='tight')
plt.close()

#Finales Ecuacion
#plt.gca().set_color_cycle(['darkviolet','y','r','g'])
lineObjects=plt.plot(1-K1s,Finales,marker='o',linewidth=2)
plt.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('k',size=16)
plt.ylabel('Poblaciones Finales',size=16)
plt.title('Ecuacion '+Nombre)
plt.ylim((-0.03,1.03))

plt.savefig(Nombre+'/Finales_Ecuacion.jpg',bbox_inches='tight')
plt.show()
plt.close()   

#%%


Condicion='3-4'
enElse='pass'
tipoP='lineal'
k3=0.0

Nombre='E='+str(tipoP)+'_BC='+Condicion+'_K3='+str(k3)+'_EnElse='+enElse

f, Axs = plt.subplots(3, 2, sharey=True,figsize=(9,10))
print(Axs.shape)

plt.subplots_adjust(left=None, bottom=None, right=0.77, top=None, wspace=0.1, hspace=0.3)
i=0
k3=0
K1s=np.arange(0,1-k3+0.1,0.1)#+[0.95,1]

#K1s=[0.0,0.2,0.4,0.6,0.8,1]
Finales=np.zeros((len(K1s),4))
for k1 in K1s:
    k2=1-k1-k3
    def ecuacion(t,x): #Max2
        C,I,A,T=x
        #k=0.2
        dC=T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2-C*I*k1/2
        dI=T**2/16*(k1)-I*A/2*k1-C*I*k1/2
        dA=T**2/8*(2*k1+k2/2)-A*C*k1/2-A*I*k1/2
        dT=C*A*k1+A*I*k1-T*C*k2*1/4-T**2/4*(k1*3/2+k2/2)+C*I*k1#-dC-dI-dA
        #if dC+dI+dA+dT>0.000001:
            #print(t,dC+dI+dA+dT,k1)
        return([dC,dI,dA,dT])


    #t_eval=np.linspace(0, 100)  
    res = solve_ivp(ecuacion, (0, 200), [2./9, 2./9, 1./9,4./9])
    #plt.gca().set_color_cycle(['darkviolet','y','r','g'])
    Finales[i]=res.y.T[-1]

    if i%2==0:
        print(i)
        lineObjects=Axs[int(i/4),int(i/2)%2].plot(res.t,res.y.T,linewidth=2)
        Axs[int(i/4),int(i/2)%2].set_title('k='+str(round(k1,2)),size=16)
        Axs[int(i/4),int(i/2)%2].set_ylim((-0.03,1.03))
        #print(np.sum(res.y.T[10]))
    i+=1

#f.set_title('Ecuaciones',size=16)
f.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(0.75, 0.7))
plt.savefig(Nombre+'/Ecuacion.jpg')#,bbox_inches='tight')
plt.close()

#Finales Ecuacion
#plt.gca().set_color_cycle(['darkviolet','y','r','g'])
lineObjects=plt.plot(1-K1s,Finales,marker='o',linewidth=2)
plt.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('k',size=16)
plt.ylabel('Poblaciones Finales',size=16)
plt.title('Ecuacion '+Nombre)
plt.ylim((-0.03,1.03))

plt.savefig(Nombre+'/Finales_Ecuacion.jpg',bbox_inches='tight')
plt.show()
plt.close()   

#%%


Condicion='2-4'
enElse='Mix'
tipoP=2
k3=0.0
Nombre='E='+str(tipoP)+'_BC='+Condicion+'_K3='+str(k3)+'_EnElse='+enElse+'FEDE'
beta=tipoP

f, Axs = plt.subplots(3, 2, sharey=True,figsize=(9,10))
print(Axs.shape)

plt.subplots_adjust(left=None, bottom=None, right=0.77, top=None, wspace=0.1, hspace=0.3)
i=0
k3=0
K1s=np.arange(0,1-k3+0.1,0.1)#+[0.95,1]
#K1s=[0.0,0.2,0.4,0.6,0.8,1]
Finales=np.zeros((len(K1s),4))
for k1 in K1s:
    k2=1-k1-k3
    def ecuacion(t,x): #Max2
        C,I,A,T=x
        #k=0.2
        dC=T*C*(np.exp(-beta*(1-(k1*1/2+k2)))/2+np.exp(-beta*(1-(-k1/2-k2)))/4-np.exp(-beta*(1-k1*1/2-k2/2))/2)
        dI=T*I*np.exp(-beta*(1+k1*1/2))/4
        dA=0
        dT=-dC-dI-dA
        #if dC+dI+dA+dT>0.000001:
            #print(t,dC+dI+dA+dT,k1)
        return([dC,dI,dA,dT])


    #t_eval=np.linspace(0, 100)  
    res = solve_ivp(ecuacion, (0, 200), [2./9, 2./9, 1./9,4./9])
    #plt.gca().set_color_cycle(['darkviolet','y','r','g'])
    Finales[i]=res.y.T[-1]

    if i%2==0:
        print(i)
        lineObjects=Axs[int(i/4),int(i/2)%2].plot(res.t,res.y.T,linewidth=2)
        Axs[int(i/4),int(i/2)%2].set_title('k='+str(round(k1,2)),size=16)
        Axs[int(i/4),int(i/2)%2].set_ylim((-0.03,1.03))
        #print(np.sum(res.y.T[10]))
    i+=1

#f.set_title('Ecuaciones',size=16)
f.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(0.75, 0.7))
plt.savefig(Nombre+'/Ecuacion.jpg')#,bbox_inches='tight')
plt.close()

#Finales Ecuacion
#plt.gca().set_color_cycle(['darkviolet','y','r','g'])
lineObjects=plt.plot(1-K1s,Finales,marker='o',linewidth=2)
plt.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('k',size=16)
plt.ylabel('Poblaciones Finales',size=16)
plt.title('Ecuacion '+Nombre)
plt.ylim((-0.03,1.03))

plt.savefig(Nombre+'/Finales_Ecuacion.jpg',bbox_inches='tight')
plt.show()
plt.close()   