#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 20:20:16 2022

@author: lupa
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp
from Cargar_Ecuacion import cargar_ecuaciones

#Dibujar las ecuaciones en conjunto con las simulaciones

k3=0
Condicion='2-4'
enElse='rechazo'
tipoP='lineal'
alpha=0.2
Nombre='BC='+Condicion+'_EnElse='+enElse+'Clasico'
def interpolar(lim_inf,lim_sup,Finales,K):
        borde_inf=np.searchsorted(Finales[:,0][::-1],lim_inf)
        borde_sup=np.searchsorted(Finales[:,0][::-1],lim_sup,side='rigth')
        return(borde_inf,borde_sup)

def dibujar(Condicion,enElse,tipoP,k3,Nombre,alpha):
        
        K=np.arange(0.0,1-k3+0.01,0.01) #Valores k1
        
        #Armar datos ecuaciones
        i=0
        Finales=np.zeros((len(K),4))
        for k1 in K:
            def ecuacion(t,x): #s<2/4
                C,I,A,T=x
                #Cargar la ecuacion correcta
                dC,dI,dA,dT=cargar_ecuaciones(Condicion,enElse,tipoP,k3,C,I,A,T,k1,alpha)
                return([dC,dI,dA,dT])
            res = solve_ivp(ecuacion, (0, 200), [2./9, 2./9, 1./9,4./9])
            Finales[i]=res.y.T[-1]#Tomar los valores finales
            i+=1            
        
        #Figuras
        fig,ax=plt.subplots(figsize=(8,5))
        df=pd.read_csv(Nombre+'/Finales.csv')#Datos simulacion
        
        # for i in range(4):
        #     plt.errorbar(1-K,Mean[:,i],yerr=Error[:,i])
        # plt.show()
        
        #Plotear simulacion
        lineObjects=ax
        plt.plot((df.T[0][1:]),df.T[range(1,5)][1:],marker='o',linewidth=1,alpha=0.7,markersize=4)

        
        #Plotear ecuaciones
        lineObjects=ax.plot(K,Finales,linewidth=3,linestyle='--',c='gray',alpha=0.7)

        #Formato plot
        ax.legend(iter(lineObjects), ('Coherentes','Incoherentes','Indiferentes','Tibios'),fontsize=13,loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlabel('k',size=16)
        ax.set_ylabel('Poblaciones Finales',size=16)
        ax.set_title(Nombre,size=16)
        ax.set_ylim((-0.03,1.03))     
        #Graficar las interpolaciones 
        lim_inf,lim_sup=0.55, 0.57
        borde_inf,borde_sup=interpolar(lim_inf,lim_sup,Finales,K)      
        #ax.errorbar((K[borde_inf]+K[borde_sup])/2, (lim_inf+lim_sup)/2, xerr=(K[borde_sup]-K[borde_inf])/2, yerr=(lim_sup-lim_inf)/2,marker='X',markersize=10,linewidth=1,c='k')
        #ax.ylim((0,1))
        #Inset (mismo plot)
        #axins = ax.inset_axes([0.02, 0.77, 0.2, 0.2])
        #axins.plot((1-df.T[0][1:]),df.T[range(1,5)][1:],marker='o',linewidth=1,alpha=0.7,markersize=4)
        #axins.plot(1-K-k3,Finales,linewidth=3,linestyle='--',c='gray',alpha=0.7)
        #axins.errorbar((K[borde_inf]+K[borde_sup])/2, (lim_inf+lim_sup)/2, xerr=(K[borde_sup]-K[borde_inf])/2, yerr=(lim_sup-lim_inf)/2,marker='X',markersize=10,linewidth=1,c='k')
        #x1, x2, y1, y2 = 0.15, 0.25, 0.54,  0.58
        #axins.set_xlim(x1, x2)
        #axins.set_ylim(y1, y2)
        #axins.set_xticklabels([])
        #axins.set_yticklabels([])
        #ax.indicate_inset_zoom(axins, edgecolor="black")

        #Guardar figura
        plt.savefig(Nombre+'/Finales_Ecuacion_J.jpg',bbox_inches='tight')
        plt.show()
        plt.close() 



        return()
#%%
alpha=0.9
Nombre='BC='+Condicion+'_EnElse='+enElse+'Clasico'
dibujar(Condicion,enElse,tipoP,k3,Nombre,alpha)
#%%
df_coherentes=np.zeros((10,11))
#Mapa en 2 variables
for i,alpha in enumerate(np.arange(0,1,0.1)):
    Nombre='BC='+Condicion+'_EnElse='+enElse+'alpha='+str(alpha)+'SinBandos_k2'
    #Nombre='E='+str(tipoP)+'_BC='+Condicion+'_EnElse='+enElse+'SinBandos'

    df=pd.read_csv(Nombre+'/Finales.csv')#Datos simulacion
    df_coherentes[i]=(df.T[1][1:])
    
plt.imshow(np.array(df_coherentes),extent=(0,1.1,0,1),cmap='coolwarm', vmax=0.6, vmin=0.4)
plt.colorbar()
plt.title('Simulación Coherentes',size=16)
plt.xlabel('k',size=16)
#plt.yticks(np.arange(0,1.1,0.1))
#plt.yticks(np.arange(0,1.1,0.1))

plt.ylabel(u'$cos(\delta)$',size=16)
