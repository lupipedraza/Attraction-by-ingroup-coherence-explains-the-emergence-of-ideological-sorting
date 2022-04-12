#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 15:17:08 2021

@author: lupa
"""




import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import json


class Agentes():
    
   def __init__(self,n,dim):
        #En estado se guardan las opiniones de los n agentes, y sobre esa variable se realizan todas las interacciones
        self.Estado=np.random.randint(-1,2,size=(n,dim))
        
        self.n=n
        self.dim=dim
        
   def CalcularIdeologia(self,alpha):
        #self.Ideologia=np.sum(self.Estado,axis=1)/self.dim
        self.Ideologia=np.sum(self.Estado,axis=1)/self.dim
        self.Ideologiaxy=[[np.dot([1,alpha],e)/2,np.dot([alpha,1],e)/2] for e in self.Estado]
        self.Ideologiay=[np.dot([alpha,1],e) for e in self.Estado]

   def Emparejar(self):
        self.Js=list(range(self.n))
        np.random.shuffle(self.Js)
        self.Is=range(self.n)
        
   def Calcular_Similaridades(self):
        self.S=np.sum(abs(self.Estado-self.Estado[self.Js]),axis=1)/float(2*self.dim) #Medida manhatan

   def IdentidadIdeologica(self):
       Identidad=self.Ideologia*self.Ideologia[self.Js]
       self.Identidad=[(int(I>0)) for I in Identidad]

   def ProbabilidadInteraccion(self,k1,alpha):
       #self.P=(k1)*(1-self.S)+np.array([(1-k1)*(abs(self.Ideologiaxy[self.Js[i]][int(self.cambio[i])]))*self.Identidad[i] for i in range(self.n)]) #distancia
       self.P=((k1)*(1-self.S)+np.array([(abs(self.Ideologiaxy[self.Js[i]][int(self.cambio[i])])) for i in range(self.n)]))/(k1+(1+alpha)/2) #distancia
       #self.P=((k1)*(1-self.S)+np.array([(1-k1)*(abs(self.Ideologia[self.Js[i]]))*self.Identidad[i]  for i in range(self.n)])) #distancia

       #self.P=(k1)*(1-self.S)+(1-k1)*np.array([((abs(self.Ideologiaxy[self.Js[i]][int(self.cambio[i])]))) for i in range(self.n)]) #distancia      
       '''
       if tipoP=='lineal':
           
           self.P=(k1)*(1-self.S)+(1-k1-k3)*(abs(self.Ideologia[self.Js]))*self.Identidad+(k3)*np.random.rand() #distancia
           
       else:
           #d=(k1)*(self.S)+(1-k1-k3)*(1-abs(self.Ideologia[self.Js]))*self.Identidad+(k3)*np.random.rand() #Probabilidad de interactuar 
           #self.P=(0.5)**(d/tipoP)
           self.S_f=1-self.S*2
           d=(k1)*(self.S_f)+(1-k1-k3)*(self.Ideologia[self.Js])*np.sign(self.Ideologia)+(k3)*np.random.rand() #Probabilidad de interactuar 
           self.P=np.exp(-tipoP*(1-d))
        '''
   def rechazoOatraccion(self,Condicion):
        self.EstadoMezclado=self.Estado[self.Js].copy()

        if Condicion=='3-4':
            self.Condicion_Tol=self.S<(3./4)
        elif Condicion=='2-4':
            self.Condicion_Tol=self.S<(2./4)
        elif Condicion=='Max2':
            self.Condicion_Tol=np.max(np.abs(self.Estado-self.EstadoMezclado),axis=1)<2

   def direccion(self):

       diferentes=np.array([self.Estado[:,s]-self.EstadoMezclado[:,s]!=0 for s in range(self.dim)])
       self.cambio=np.zeros(self.n, dtype=np.uint8)
       for i in range(self.n):
           if self.Condicion_Tol[i]: #Si se atraen
               #Elige uno de los diferentes
               verdaderos=np.where(diferentes[:,i])[0]
               if len(verdaderos)>0:
                   self.cambio[i]=int(np.random.choice(verdaderos))
           else:
                #Elige uno al azar
                self.cambio[i]=int(np.random.randint(self.dim))

   def Interaccion(self,Condicion,enElse):
        Condicion_proba=np.random.uniform(size=self.n )<self.P


        for i in np.where(Condicion_proba)[0]:
            #Buscamos los diferentes
            if sum(self.Estado[i]==self.EstadoMezclado[i])<2:
                if self.Condicion_Tol[i]:
                        if self.Estado[i][self.cambio[i]]<self.EstadoMezclado[i][self.cambio[i]]:
                            self.Estado[i][self.cambio[i]]+=1
                        else:
                            self.Estado[i][self.cambio[i]]-=1
                        
                else:
                   if enElse=='pass':
                       pass
                   elif enElse=='rechazo':
                                       
                       #Influencia negativa
                       if self.Estado[i][self.cambio[i]]==0:
                           #print('rechazo')
                           if self.EstadoMezclado[i][self.cambio[i]]>0:
                                self.Estado[i][self.cambio[i]]+=1
                           elif self.EstadoMezclado[i][self.cambio[i]]<0:
                                self.Estado[i][self.cambio[i]]-=1

def Ver_Estado(hist):
    #Funcion para identificar si hay consenso, polarizacion en las esquinas, o polarización en las esquinas y el centro
    if np.max(hist)>0.9: #En este caso es consenso
           consenso=np.argmax(hist)
           #print('Consenso en: ', consenso)
           Estado='Consenso'
    elif (hist[0,1]+hist[1,0]+hist[2,1]+hist[1,2])<0.1:#Hay segregación
        if hist[1,1]<0.1: #No hay indiferentes
               polarizacion= hist[0,0]+hist[2,2]
               #print('Polarizacion con:',polarizacion)
               Estado='Polarizacion'
        else:
               centro=hist[1,1]
               polarizacion= hist[0,0]+hist[2,2]
               #print('polarizacion con centro:' ,centro, ' y ',polarizacion)
               Estado='PolarizacionConCentro'
    else:
           plt.imshow(hist)
           #print('Ninguno')
           Estado='Ninguno'
    return(Estado)      

def corrida(n,dim,cantidad,k1,alpha,Condicion,enElse):
        #Función que ejecuta un paso en la corrida
        Ag=Agentes(1000,2)		
        Historia=[]
        for c in range(cantidad):
            Ag.CalcularIdeologia(alpha)
            Ag.Emparejar()
            Ag.Calcular_Similaridades()
            Ag.IdentidadIdeologica()
            Ag.rechazoOatraccion(Condicion)
            Ag.direccion()
            Ag.ProbabilidadInteraccion(k1,alpha)
            Ag.Interaccion(Condicion,enElse)
            #print(c)
            Historia.append(Ag.Estado.copy())
        return(Historia)
        
def dibujar_hist(Agentes,dim,n):
    #Función que plotea el histograma en un estado, y devuelve los valores de la matriz de 3x3 con la densidad de poblacion
    hist=plt.hist2d([x[0] for x in Agentes],[x[1] for x in Agentes],bins=3,range=[[-1.5,1.5],[-1.5,1.5]],cmap=plt.get_cmap('BuPu'),vmin=0,vmax=n/2)
    #plt.show()
    plt.clf()
    plt.close()
    return hist[0]
#%%

def Corrida_Total(Nombre,Condicion,enElse,alpha,cantidad_interacciones=700, Veces=40):
    #Función que corre cantidad_interacciones pasos y promedia Veces interacciones
    
    n=1000
    dim=2
    step=0.1
    K=np.arange(0,1+step,step)
    
    Coherentes=[]
    Incoherentes=[]
    Indiferentes=[]
    Tibios=[]
    
    
    # Para construir el grafico de estado final por veces
    Estado={'Consenso':{k:0 for k in K},
            'Polarizacion':{k:0 for k in K},
            'PolarizacionConCentro':{k:0 for k in K},
            'Ninguno':{k:0 for k in K}}
    
    Histograma={'Consenso':{k:np.zeros((3,3)) for k in K},
            'Polarizacion':{k:np.zeros((3,3)) for k in K},
            'PolarizacionConCentro':{k:np.zeros((3,3)) for k in K},
            'Ninguno':{k:np.zeros((3,3)) for k in K}}

    for k in K:
    
        Coherentes_temporal=np.zeros(int(cantidad_interacciones/10))
        Incoherentes_temporal=np.zeros(int(cantidad_interacciones/10))
        Indiferentes_temporal=np.zeros(int(cantidad_interacciones/10))
        Tibios_temporal=np.zeros(int(cantidad_interacciones/10))
        C_F=[]
        I_F=[]
        A_F=[]
        T_F=[]
                  
        
        for v in range(Veces):
 
            #Histograma=np.zeros((3,3))
            Historia=corrida(n,dim,cantidad_interacciones,k,alpha,Condicion,enElse)
            
            for i in range(0,int(cantidad_interacciones/10)):
                hist=dibujar_hist(Historia[i*10],dim,n)
                #Histograma+=hist/Veces
                Paso_coherentes=((hist[0,0]+hist[2,2])/n)
                Paso_incoherentes=((hist[0,2]+hist[2,0])/n)
                Paso_indiferentes=((hist[1,1])/n)
                Paso_tibios=((hist[1,0]+hist[1,2]+hist[0,1]+hist[2,1])/n)
    
                Coherentes_temporal[i]+=(Paso_coherentes/Veces)
                Incoherentes_temporal[i]+=(Paso_incoherentes/Veces)
                Indiferentes_temporal[i]+=(Paso_indiferentes/Veces)
                Tibios_temporal[i]+=Paso_tibios/Veces
                
            #Finales_Con_Error
            C_F.append(Paso_coherentes)
            I_F.append(Paso_incoherentes)
            A_F.append(Paso_indiferentes)
            T_F.append(Paso_tibios)

            
        print(k)

        #Guardar todos los finales para poder calcular el error
        df_F=pd.DataFrame([C_F,I_F,A_F,T_F],['Coherentes','Incoherentes','Indiferentes','Tibios'])
        df_F.to_csv(Nombre+'/Finales'+str(k)+'.csv')

            
        #Guardar los datos cada 10 tiempos
        df_temporal=pd.DataFrame([range(0,cantidad_interacciones,10),Coherentes_temporal,Incoherentes_temporal,Indiferentes_temporal,Tibios_temporal])    
        df_temporal.to_csv(Nombre+'_Temporal_k='+str(round(k,2))+'.csv')

#%%
plt.plot(range(0,cantidad_interacciones,10),Coherentes_temporal)
plt.plot(range(0,cantidad_interacciones,10),Incoherentes_temporal)    
plt.ylim((0,1))    
plt.show()
 
#%% FINALES Op 1
k3=0
step=0.1
K=np.arange(0,1+step,step)
Total=np.zeros((len(K),4))

i=0    
for k in K:
    df=pd.read_csv(Nombre+'/'+'_Temporal_k='+str(round(k,2))+'.csv')    
    Total[i]=(df.T.iloc[-1][1:]).T
    i+=1
df=pd.DataFrame([K,Total.T[0],Total.T[1],Total.T[2],Total.T[3]],['K','Coherentes','Incoherentes','Indiferentes','Tibios'])
df.to_csv(Nombre+'/Finales.csv')

#%% Finales Op 2 
step=0.2
K=np.arange(0.0,1-k3+step,step)
Mean=[]
Error=[]
i=0    
for k in K:
    df_F=pd.read_csv(Nombre+'/Finales'+str(k)+'.csv')
    Mean.append(df_F.T[1:].mean())  
    Error.append(df_F.T[1:].std()) 

Mean=np.array(Mean)
Error=np.array(Error)
    
#%%    
import os
current_directory = os.getcwd()

#%%

#SIMULAR TODO

Condiciones=['Max2','3-4']
enElses=['rechazo','pass']
tipoPs=['lineal']
k3s=[0.0]
for Condicion in Condiciones:
    for enElse in enElses:
        for tipoP in tipoPs:
            for k3 in k3s:
                Nombre='E='+str(tipoP)+'_BC='+Condicion+'_K3='+str(k3)+'_EnElse='+enElse
                print(Nombre)
                final_directory = os.path.join(current_directory, Nombre)
                if not os.path.exists(final_directory):
                    os.makedirs(final_directory)
                Corrida_Total(Nombre+'/',Condicion,enElse,tipoP,k3)
                


#%%

Condicion='2-4'
enElse='Mix'
tipoP=2
k3=0.0
Nombre='E='+str(tipoP)+'_BC='+Condicion+'_K3='+str(k3)+'_EnElse='+enElse+'FEDE'
print(Nombre)
final_directory = os.path.join(current_directory, Nombre)
if not os.path.exists(final_directory):
    os.makedirs(final_directory)
Corrida_Total(Nombre+'/',Condicion,enElse,tipoP,k3)

#%%
step=0.1
K=np.arange(0,1+step,step)
Total=np.zeros((len(K),4))
k3=0
Condicion='2-4'
enElse='rechazo'
tipoP='lineal'


for alpha in np.arange(0,1,0.1):
    Nombre='BC='+Condicion+'_EnElse='+enElse+'alpha='+str(alpha)+'SinBandos_normalizado'
    #Nombre='BC='+Condicion+'_EnElse='+enElse+'Clasico'
    final_directory = os.path.join(current_directory, Nombre)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
    Corrida_Total(Nombre+'/',Condicion,enElse,alpha,cantidad_interacciones=200, Veces=10)

    
    i=0    
    for k in K:
        df=pd.read_csv(Nombre+'/'+'_Temporal_k='+str(round(k,2))+'.csv')    
        Total[i]=(df.T.iloc[-1][1:]).T
        i+=1
    df=pd.DataFrame([K,Total.T[0],Total.T[1],Total.T[2],Total.T[3]],['K','Coherentes','Incoherentes','Indiferentes','Tibios'])
    df.to_csv(Nombre+'/Finales.csv')


#%%
'''
Condicion='3-4'
enElse='pass'
tipoP=0.2
Nombre='E='+str(tipoP)+'_'+Condicion+'_'+enElse
final_directory = os.path.join(current_directory, Nombre)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
Corrida_Total(Nombre+'/',Condicion,enElse,tipoP)

#%%
Condicion='3-4'
enElse='rechazo'
tipoP=0.2
Nombre='E='+str(tipoP)+'_'+Condicion+'_'+enElse
final_directory = os.path.join(current_directory, Nombre)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
Corrida_Total(Nombre+'/',Condicion,enElse,tipoP)


#%%
Condicion='2-4'
enElse='rechazo'
Nombre='NuevaP_'+Condicion+str('_')+enElse
final_directory = os.path.join(current_directory, Nombre)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
Corrida_Total(Nombre+'/',Condicion,enElse)

#%%
#%%
Condicion='Max2'
enElse='rechazo'
Nombre='NuevaP_'+Condicion+str('_')+enElse
final_directory = os.path.join(current_directory, Nombre)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
Corrida_Total(Nombre+'/',Condicion,enElse)
'''

#%%
#Grafico P
'''
E=0.2
f_ex=lambda x: (0.5)**(x/E)
f_lin=lambda x: 1-x

plt.plot(np.linspace(0,1,100),f_ex(np.linspace(0,1,100)),c='darkviolet',label='Exponencial')
plt.ylim((0,1))
plt.xlabel('Distancia', size=16)
plt.ylabel('Probabilidad', size=16)

plt.plot(np.linspace(0,1,100),f_lin(np.linspace(0,1,100)),c='g',label='Lineal')
plt.ylim((0,1))
plt.xlabel('Distancia', size=16)
plt.ylabel('Probabilidad', size=16)

plt.legend(fontsize=16)
'''
#%%

