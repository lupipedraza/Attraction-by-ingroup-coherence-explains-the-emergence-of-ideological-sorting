#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 11:39:00 2022

@author: lupa
"""
import numpy as np

def load_equations(enElse, C, I, A, T, k1):
    k2 = 1 - k1
    if enElse == 'rejection':
        dC = T * C * k2 / 16 + T * C * k1 / 4 + T ** 2 / 16 * (k2)  # + k2) - C * A * k1 / 2
        dI = T * I / 16 * k2 + T ** 2 / 16 * (k2)  # - I * A / 2 * k1
        dA = -A * C * k2 / 2 - A * I * k2 / 2
        dT = -C * T * k2 / 16 + C * A * k2 / 2 + A * I * k2 / 2 - T * C * k1 * 1 / 4 - T * I * k2 / 16 - T ** 2 / 8 * (k2)
    if enElse == 'pass':
        dC = T * C * k1 / 4
        dI = 0 * T
        dA = 0 * T
        dT = -T * C * k1 * 1 / 4
    return (dC, dI, dA, dT)