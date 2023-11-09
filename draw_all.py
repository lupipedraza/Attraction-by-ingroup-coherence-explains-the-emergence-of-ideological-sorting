#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp
from load_equations import load_equations
from cycler import cycler

#%% Functions
def interpolate(lower_limit, upper_limit, Finals, K):
    
    """
    Calculate a confidence interval for a possible value of K based on given data.

    Args:
    lower_limit (float): The lower limit of the confidence interval.
    upper_limit (float): The upper limit of the confidence interval.
    Finals (numpy.ndarray): An array of final values for each population for each value of K.
    K (list): A list of parameter values.

    Returns:
    tuple: A tuple containing the lower and upper bounds of the confidence interval.

    This function takes final values and their associated parameter values to calculate a confidence interval
    for a possible value of K based on a given lower and upper limit.
    """
    lower_boundary = np.searchsorted(Finals[:, 0], lower_limit)
    upper_boundary = np.searchsorted(Finals[:, 0], upper_limit, side='right')
    return (len(Finals) - lower_boundary, len(Finals) - upper_boundary)

def solve_single_equation(k, elseClause, final):
    """
    Solve a differential equation with an initial condition [2./9, 2./9, 1./9, 4./9].

    Args:
        k (float): The parameter for the equation.
        elseClause (str): A parameter that distinguishes between two proposed models: "rejection" and "pass".
        final (float): The final time for solving the differential equation.

    Returns:
        scipy.integrate._ivp.ivp.OdeResult: The result of the differential equation solver.

    This function solves a differential equation with a specified initial condition and parameter. The 'elseClause' parameter
    is used to distinguish between two proposed models: "rejection" and "pass".
    """
    def equation(t, x): # s < 2/4
        C, I, A, T = x
        # Load the correct equation
        dC, dI, dA, dT = load_equations(elseClause, C, I, A, T, k)
        return [dC, dI, dA, dT]
    return solve_ivp(equation, (0, final), [2./9, 2./9, 1./9, 4./9])

def solve_equation(K, elseClause, final=600):
    """
    Solve the equation for all possible values from k to 0 to K.
    Save only the final values.

    Args:
        K (list): A list of parameter values to be tested.
        elseClause (str): A parameter that distinguishes between two proposed models: "rejection" and "pass".
        final (float, optional): The final time for solving the differential equation (default is 600).

    Returns:
        numpy.ndarray: An array containing the final values for each population for each value of K.

    This function iterates over a range of parameter values in K, solving the differential equation for each value
    and saving only the final values. The 'elseClause' parameter is used to distinguish between two proposed models.
    """
    Finals = np.zeros((len(K), 4))
    for i, k in enumerate(K):
        res = solve_single_equation(k, elseClause, final)
        Finals[i] = res.y.T[-1]  # Take the final values
    return Finals

def draw_interpolation(K, elseClause, Name, interpolators):

    """
    Create Figure 3: Plot simulations and equations with interpolations.

    Args:
        K (list): A list of parameter values to be tested.
        elseClause (str): A parameter that distinguishes between two proposed models: "rejection" and "pass".
        Name (str): The name of the directory where the results will be saved.
        interpolators (list): List of interpolators for generating confidence intervals.

    This function generates Figure 3, which includes simulations, equations, and interpolations based on the provided parameters.
    """
    
    # Figures
    fig, ax = plt.subplots(figsize=(8, 5))

    # Load equation data
    Finals = solve_equation(K, elseClause)

    # Load simulation data
    df = pd.read_csv(Name + '/Finals_mean.csv') # Simulation data

    # Colors
    ax.set_prop_cycle(cycler('color', ['purple', 'orangered', 'silver', 'orchid']))

    # Plot simulations
    # C, I = ax.plot(1 - (df.T[0][1:]).values[::3], df.T[range(1, 3)][1:].values[::3], marker='o', linewidth=0, alpha=0.7, markersize=10)
    
    # Plot equations
    EC = ax.plot(K, Finals[:, 0:1], linewidth=3, linestyle='--', alpha=0.7, label='Equations')

    # Plot format
    # ax.legend([C, I, A, T, EC], ['Coherent', 'Incoherent', 'Apathetic', 'Weak', 'equations'], fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
    # ax.legend([C, I, A, T, EC], ['Coherent', 'Incoherent', 'Apathetic', 'Weak'], fontsize=14, loc='upper left')
    # ax.legend([EC, EI, EA, ET], ['Coherent', 'Incoherent', 'Apathetic', 'Weak'], fontsize=13, loc='lower left')

    # ax.legend([C, I, EC], ['Coherent', 'Incoherent', "equations"], fontsize=14, loc='upper left')

    ax.set_xlabel('k', size=16)
    ax.set_ylabel('sorting', size=16)
    ax.tick_params(labelsize=16)
    plt.xticks(np.arange(0, 1.2, step=0.25))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.set_ylim([0.475,0.825])
    
    plt.yticks(np.arange(0.5, 0.9, 0.1))

    # Plot the interpolations
    for inte in interpolators:
        lower_limit, upper_limit = inte[:2]
        try:
            print(inte)
            if inte[2] == 0:
                lower_boundary, upper_boundary = interpolate(lower_limit, upper_limit, Finals, K)
                nopol = ax.errorbar(1 - (K[lower_boundary] + K[upper_boundary]) / 2, (lower_limit + upper_limit) / 2,
                                   xerr=(K[upper_boundary] - K[lower_boundary]) / 2, yerr=(upper_limit - lower_limit) / 2,
                                   marker='o', markersize=7, linewidth=1, c='gray')
            else:
                lower_boundary, upper_boundary = interpolate(lower_limit, upper_limit, Finals, K)
                pol = ax.errorbar(1 - (K[lower_boundary] + K[upper_boundary]) / 2, (lower_limit + upper_limit) / 2,
                                 xerr=(K[upper_boundary] - K[lower_boundary]) / 2, yerr=(upper_limit - lower_limit) / 2,
                                 marker='D', markersize=7, linewidth=1, c='k')
        except:
            pass

    ax.legend([EC, nopol, pol], ['equation', 'non-political', 'political'], fontsize=14, loc='upper left')

    plt.savefig('Figures/'+Name+'_Interpolated_Equations.pdf', bbox_inches='tight')
    plt.savefig('Figures/'+Name+'_Interpolated_Equations.jpg', bbox_inches='tight')
    plt.show()
    plt.close()
    
def draw_error(K, elseClause, Name, interpolators, simulate=True, equation=True):

    """
    Create Figure 2: Plot simulations and equations with error bars.
    
    Args:
        K (list): A list of parameter values to be tested.
        elseClause (str): A parameter that distinguishes between two proposed models: "rejection" and "pass".
        Name (str): The name of the directory where the results will be saved.
        interpolators (list): List of interpolators for generating confidence intervals.
        simulate (bool, optional): Whether to include simulation results (default is True).
        equation (bool, optional): Whether to include equation results (default is True).
    
    This function generates Figure 2, which includes simulations and equations with error bars based on the provided parameters.
    """
    
    # Figures
    fig, ax = plt.subplots(figsize=(8, 5))

    # Colors
    ax.set_prop_cycle(cycler('color', ['purple', 'orangered', 'silver', 'orchid']))

    if simulate:
        df_m = pd.read_csv( Name + '/Finals_mean.csv')
        df_e = pd.read_csv(Name + '/Finals_error.csv')

        # Plot simulations
        C = ax.errorbar( (df_m.T[0][1:]).values, df_m.T[1][1:].values, yerr=df_e.T[1][1:].values, fmt="o")
        I = ax.errorbar( (df_m.T[0][1:]).values, df_m.T[2][1:].values, yerr=df_e.T[2][1:].values, fmt="o")
        A = ax.errorbar( (df_m.T[0][1:]).values, df_m.T[3][1:].values, yerr=df_e.T[3][1:].values, fmt="o")
        T = ax.errorbar( (df_m.T[0][1:]).values, df_m.T[4][1:].values, yerr=df_e.T[4][1:].values, fmt="o")

        ax.legend([C, I, A, T], ['Coherent', 'Incoherent', 'Apathetic', 'Weak'], fontsize=16, loc='upper left')
        Nom = 'Simu'

    if equation:
        Finals = solve_equation(K, elseClause)
        EC, EI, EA, ET = ax.plot(K, Finals, linewidth=2, linestyle='--', label='Equations', color='gray')
        ax.legend([EC, EI, EA, ET], ['Coherent', 'Incoherent', 'Apathetic', 'Weak'], fontsize=16, loc='upper left')
        Nom = 'Eq'

        if simulate:
            ax.legend([C, I, A, T, EC], ['Coherent', 'Incoherent', 'Apathetic', 'Weak', 'Equation'], fontsize=16, loc='upper left', bbox_to_anchor=(0, 1))
            Nom = 'EqAndSim'

    # Plot format
    ax.set_xlabel('k', size=16)
    ax.set_ylabel('Proportion', size=16)
    ax.tick_params(labelsize=16)
    plt.xticks(np.arange(0, 1.2, step=0.25))
    ax.set_ylim((-0.03, 1.03))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    
    plt.yticks(np.arange(.5, .9, 0.1))

    # Save the figure
    plt.savefig('Figures/' + Name+ '_' + Nom + '.pdf', bbox_inches='tight')
    plt.savefig('Figures/' + Name + '_'+ Nom + '.jpg', bbox_inches='tight')
    plt.show()
    plt.close()

#%%    
#FIGURE 2
# Figure with rejection. You can plot the simulation, the equation, or both.
# We provide all three options

elseClause = 'rejection'  # can be 'rejection' or 'pass'
Condition = '2-4'

Name = 'Simulations_Else=' + elseClause + '_Error'
step = 0.05
K = np.arange(0.0, 1 + step, step)  # Values for k
interpolators = []
draw_error(K, elseClause, Name, interpolators, simulate=True, equation=True)

draw_error(K, elseClause, Name, interpolators, simulate=False, equation=True)

draw_error(K, elseClause, Name, interpolators, simulate=True, equation=False)

#%%
#FIGURE 2
# The same as the previous figures for the model without rejection
elseClause = 'pass'  # can be 'rejection' or 'pass'
Condition = '2-4'

Name = 'Simulations_Else=' + elseClause + '_Error'
step = 0.05
K = np.arange(0.0, 1 + step, step)  # Values for k
interpolators = []
draw_error(K, elseClause, Name, interpolators, simulate=True, equation=True)

draw_error(K, elseClause, Name, interpolators, simulate=False, equation=True)

draw_error(K, elseClause, Name, interpolators, simulate=True, equation=False)

#%% Graph interpolated data in the equation
#FIGURE 3

#Data from real experiments 
data = pd.read_csv('ExportForPython.csv')  # simulation

#Model conditions
elseClause = 'rejection'  # can be 'rejection' or 'pass'
Condition = '2-4'
Name = 'Simulations_Else=' + elseClause + '_Error'

# Choose how fine we want the k mesh to be (only for the equation)
step = 0.01
K = np.arange(0.0, 1 + step, step)  # Values for k

group = data.groupby('cohLabel').mean().isPol.values

#make the interval errors
mean = data.groupby('cohLabel').mean().cohProportion.values
std = data.groupby('cohLabel').std().cohProportion.values / np.sqrt(data.groupby('cohLabel').count().cohProportion.values)

interpolators = [[mean[i] - std[i], mean[i] + std[i], group[i]] for i in range(len(group))]

draw_interpolation(K, elseClause, Name, interpolators)


#%% 
#Extra (not in the paper)
#Create a figure for a fixed k of the population evolution

k = 0.15
elseClause = 'rejection'  # can be 'rejection' or 'pass'
Name = 'Simulations_Else=' + elseClause + '_Classic'

# Load data
df = pd.read_csv(Name + '/Temporal_k=' + str(round(k, 2)) + '.csv')  # simulation
# Trim df
df = df.T[1:15]
# Match the lengths of equations and simulations
final = int(df[0][-1])
res = solve_single_equation(k, elseClause, final)  # Equation

# Figures
fig, ax = plt.subplots(figsize=(8, 5))

ax.set_prop_cycle(cycler('color', ['purple', 'orangered', 'silver', 'orchid']))

C, I, A, T = ax.plot(df[0], df.iloc[:, 1:].values, marker='o', linewidth=1, alpha=1, markersize=10)
EC, EI, EA, ET = ax.plot(np.array(res.t), np.array(res.y.T), linewidth=3, linestyle='--', alpha=0.7, label='Equations')

# Labels
ax.legend([C, I, A, T, EC], ['Coherent', 'Incoherent', 'Apathetic', 'Weak', 'Equations'], fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_xlabel('Time', size=16)
ax.set_ylabel('Populations', size=16)
ax.set_title('k=' + str(k), size=16)
ax.tick_params(labelsize=16)
ax.set_ylim((-0.03, 1.03))


#%%
