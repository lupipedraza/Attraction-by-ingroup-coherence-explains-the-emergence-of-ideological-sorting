#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 11:39:00 2022

@author: lupa
"""
import numpy as np
def cargar_ecuaciones(Condicion,enElse,tipoP,k3,C,I,A,T,k1,alpha):
    k3=0.0
    #k2=1-k3-k1
    k2=1
    if Condicion=='2-4' and enElse=='rechazo' and tipoP=='lineal' and k3==0.0:
        '''
        dC=T*C*k1/16+T*C*k2/4+T**2/16*(k1)#+k2)-C*A*k1/2
        dI=T*I/16*k1+T**2/16*(k1)#-I*A/2*k1
        dA=-A*C*k1/2-A*I*k1/2
        dT=-C*T*k1/16+C*A*k1/2+A*I*k1/2-T*C*k2*1/4-T*I*k1/16-T**2/8*(k1)#-T**2/8*(k2/2)#-dC-dI-dA
        '''
        dC=T*C*k1/16+T*C*k2*(1+alpha)/8+T*C*k2/4+T**2/16*(k1)+T**2*k2/16#+k2)-C*A*k1/2
        dI=T*I*k1/16+T*I*k2*(1-alpha)/8+T*I/4*(1-2*alpha)+T**2/16*(k1)+T**2*k2/16#-I*A/2*k1
        dA=-A*C/2*(k1+k2*(1+alpha))-A*I/2*(k1+k2*(1-alpha))-T*A*k2/2
        dT=-dC-dI-dA#-C*T*k1/16+C*A*k1/2+A*I*k1/2-T*C*k2*1/4-T*I*k1/16-T**2/8*(k1)#-T**2/8*(k2/2)#-dC-dI-dA


    if Condicion=='2-4' and enElse=='pass' and tipoP=='lineal' and k3==0.0:
        dC=T*C*k2/4
        dI=0*T
        dA=0*T
        dT=-T*C*k2*1/4
    if Condicion=='Max2' and enElse=='pass' and tipoP=='lineal' and k3==0.0:
        dC=T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2
        dI=T**2/16*(k1)-I*A/2*k1
        dA=T**2/8*(k1+k2/2)-A*C*k1/2-A*I*k1/2
        dT=C*A*k1+A*I*k1-T*C*k2*1/4-T**2/4*(k1+k2/2)#-dC-dI-dA
    if Condicion=='3-4' and enElse=='pass' and tipoP=='lineal' and k3==0.0:
        dC=T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2-C*I*k1/2
        dI=T**2/16*(k1)-I*A/2*k1-C*I*k1/2
        dA=T**2/8*(2*k1+k2/2)-A*C*k1/2-A*I*k1/2
        dT=C*A*k1+A*I*k1-T*C*k2*1/4-T**2/4*(k1*3/2+k2/2)+C*I*k1#-dC-dI-dA
    if Condicion=='3-4' and enElse=='rechazo' and tipoP=='lineal' and k3==0.0:
        dC=T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2-C*I*k1/2+T*C*k1/16
        dI=T**2/16*(k1)-I*A/2*k1-C*I*k1/2+T*I*k1/16
        dA=T**2/8*(2*k1+k2/2)-A*C*k1/2-A*I*k1/2
        dT=C*A*k1+A*I*k1-T*C*k2*1/4-T**2/4*(k1*3/2+k2/2)+C*I*k1-T*C*k1/16-T*I*k1/16
    if Condicion=='Max2' and enElse=='rechazo' and tipoP=='lineal' and k3==0.0:
        dC=T*C*k1/16+T*C*k2/4+T**2/16*(k1+k2)-C*A*k1/2
        dI=T*I/16*k1+T**2/16*(k1)-I*A/2*k1
        dA=T**2/8*(k1+k2/2)-A*C*k1/2-A*I*k1/2
        dT=-C*T*k1/16+C*A*k1+A*I*k1-T*C*k2*1/4-T*I*k1/16-T**2/4*(k1+k2/2)#-dC-dI-dA
    if Condicion=='2-4' and enElse=='Mix' and tipoP==2 and k3==0.0:
        dC=T*C*(np.exp(-tipoP*(1-(k1*1/2+k2)))/2+np.exp(-tipoP*(1-(-k1/2-k2)))/4-np.exp(-tipoP*(1-k1*1/2-k2/2))/2)
        dI=T*I*np.exp(-tipoP*(1+k1*1/2))/4
        dA=0
        dT=-dC-dI-dA
    return(dC,dI,dA,dT)