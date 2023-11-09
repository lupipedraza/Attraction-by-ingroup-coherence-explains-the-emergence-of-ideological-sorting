#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% 
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
current_directory = os.getcwd()
#%% 
# The Agent class is the object where we perform the simulation
class Agents():

    def __init__(self, n, dim):
        # The 'State' variable stores the opinions of the 'n' agents, and all interactions are based on this variable
        self.State = np.random.randint(-1, 2, size=(n, dim))

        self.n = n
        self.dim = dim

    def CalculateIdeology(self):
        # We calculate ideology as the sum of opinions for each agent divided by the dimension
        self.Ideology = np.sum(self.State, axis=1) / self.dim
        
    def Match(self):
        # Pairs of agents to interact with are randomly shuffled
        self.Js = list(range(self.n))
        np.random.shuffle(self.Js)
        self.Is = range(self.n)

    def Calculate_Similarities(self):
        # Similarity is calculated using the Manhattan distance
        self.S = 1 - np.sum(abs(self.State - self.State[self.Js]), axis=1) / float(2 * self.dim)

    def IdeologicalIdentity(self):
        Identity = self.Ideology * self.Ideology[self.Js]
        self.Identity = [int(I > 0) for I in Identity]

    def InteractionProbability(self, k):
        # Different variants of the model are calculated here. The final one used is (1-k) * S + ( k) * Ideology * Identity

        # 2 parameters - Sigma
        self.P = (1-k) * (self.S) + np.array([(k) * (abs(self.Ideology[self.Js[i]])) * self.Identity[i] for i in range(self.n)])


    def AttractionOrRejection(self, Condition):
        # Different model variants. Finally, we use 2/4
        self.MixedState = self.State[self.Js].copy()

        if Condition == '3-4':
            self.Condition_Tol = self.S > (3. / 4)
        elif Condition == '2-4':
            self.Condition_Tol = self.S > (2. / 4)
        elif Condition == 'Max2':
            self.Condition_Tol = np.max(np.abs(self.State - self.MixedState), axis=1) < 2

    def Direction(self):
        # Decide in which direction each agent moves in case an action is taken
        different = np.array([self.State[:, s] - self.MixedState[:, s] != 0 for s in range(self.dim)])
        self.change = np.zeros(self.n, dtype=np.uint8)
        for i in range(self.n):
            if self.Condition_Tol[i]:  # If they are attracted
                # Choose one of the differences
                true_values = np.where(different[:, i])[0]
                if len(true_values) > 0:
                    self.change[i] = int(np.random.choice(true_values))
            else:
                # Choose one at random
                self.change[i] = int(np.random.randint(self.dim))

    def Interaction(self, Condition, elseClause):
        # Choose which agents take action
        Condition_prob = np.random.uniform(size=self.n) < self.P

        # For those who take action, perform the movement
        for i in np.where(Condition_prob)[0]:
            # Look for differences
            if sum(self.State[i] == self.MixedState[i]) < 2:
                if self.Condition_Tol[i]:  # They are attracted
                    if self.State[i][self.change[i]] < self.MixedState[i][self.change[i]]:
                        self.State[i][self.change[i]] += 1
                    elif self.State[i][self.change[i]] > self.MixedState[i][self.change[i]]:
                        self.State[i][self.change[i]] -= 1
                else:  # Outside the attraction limit
                    if elseClause == 'pass':
                        pass
                    elif elseClause == 'rejection':
                        if self.State[i][self.change[i]] == 0:
                            if self.MixedState[i][self.change[i]] > 0:
                                self.State[i][self.change[i]] += 1
                            elif self.MixedState[i][self.change[i]] < 0:
                                self.State[i][self.change[i]] -= 1

def run(n, dim, num_interactions, k, Condition, elseClause):
    # Function that executes one step in the run
    Agents_obj = Agents(n, dim)
    History = []
    for c in range(num_interactions):
        Agents_obj.CalculateIdeology()
        Agents_obj.Match()
        Agents_obj.Calculate_Similarities()
        Agents_obj.IdeologicalIdentity()
        Agents_obj.AttractionOrRejection(Condition)
        Agents_obj.Direction()
        Agents_obj.InteractionProbability(k)
        Agents_obj.Interaction(Condition, elseClause)
        History.append(Agents_obj.State.copy())
    return History

def draw_hist(Agents, dim, n):
    # This function plots the histogram in a state and returns the values of the 3x3 matrix with population density
    hist = plt.hist2d([x[0] for x in Agents], [x[1] for x in Agents], bins=3, range=[[-1.5, 1.5], [-1.5, 1.5]], cmap=plt.get_cmap('BuPu'), vmin=0, vmax=n / 2)
    plt.clf()
    plt.close()
    return hist[0]
#%%

def Total_Run(Name, Condition, elseClause, K, num_interactions=700, Repetitions=40):
  
    '''
    Run a simulation and record the results.

    Args:
        Name (str): The name of the directory where the results will be saved.
        Condition: The bounded confidence condicion. '2-4', '3-4' and 'Max2' are the possible values.
        elseClause (bool): The condition to apply if 'Condition' is False. The possible values are 'rejection' or 'pass'.
        K (list): A list of parameter values to be tested.
        num_interactions (int, optional): Total number of interactions to simulate (default is 700).
        Repetitions (int, optional): Number of repetitions for each parameter value (default is 40).

    This function runs a simulation with the specified parameters and records the results in CSV files.
    '''    
    
    n = 1000 # Agent number
    dim = 2 # Opinion dimension

    for k in K:
        # Define the step interval for saving results
        step=10
        #Save the information every 'step' interactions
        Coherent_temp = np.zeros(int(num_interactions / step))
        Incoherent_temp = np.zeros(int(num_interactions / step))
        Apathetic_temp = np.zeros(int(num_interactions / step))
        Weak_temp = np.zeros(int(num_interactions / step))

        for v in range(Repetitions):
            History = run(n, dim, num_interactions, k, Condition, elseClause)

            for i in range(0, int(num_interactions / step)):
                hist = draw_hist(History[i * step], dim, n)
                Step_coherent = ((hist[0, 0] + hist[2, 2]) / n)
                Step_incoherent = ((hist[0, 2] + hist[2, 0]) / n)
                Step_Apathetic = ((hist[1, 1]) / n)
                Step_Weak = (hist[1, 0] + hist[1, 2] + hist[0, 1] + hist[2, 1]) / n

                Coherent_temp[i] += (Step_coherent / Repetitions)
                Incoherent_temp[i] += (Step_incoherent / Repetitions)
                Apathetic_temp[i] += (Step_Apathetic / Repetitions)
                Weak_temp[i] += Step_Weak / Repetitions

        # Save the data every 10 times
        df_temp = pd.DataFrame([range(0, num_interactions, 10), Coherent_temp, Incoherent_temp, Apathetic_temp, Weak_temp])
        df_temp.to_csv(Name + '/Temporal_k=' + str(round(k, 2)) + '.csv')
        
#%% 
def Total_Run_Error(Name, Condition, elseClause, K, num_interactions, Repetitions):

    """
    Run a simulation, save final states, and calculate the error.

    Args:
        Name (str): The name of the directory where the results will be saved.
        Condition: The bounded confidence condicion. '2-4', '3-4' and 'Max2' are the possible values.
        elseClause (bool): The condition to apply if 'Condition' is False. The possible values are 'rejection' or 'pass'.
        K (list): A list of parameter values to be tested.
        num_interactions (int): Total number of interactions to simulate.
        Repetitions (int): Number of repetitions for each parameter value.

    This function runs a simulation with the specified parameters and records the final states and their errors in CSV files.
    """

    # Number of agents in the simulation
    n = 1000

    # Dimension of the opinion space
    dim = 2     


    Total_mean = []
    Total_error = []

    for k in K:
        
        # Initialize arrays to store final states
        Final_Coherent = np.zeros(Repetitions)
        Final_Incoherent = np.zeros(Repetitions)
        Final_Apathetic = np.zeros(Repetitions)
        Final_Weak = np.zeros(Repetitions)

        for v in range(Repetitions):
            # Run the simulation and get the history
            History = run(n, dim, num_interactions, k, Condition, elseClause)

            # Save all results for the final state
            hist = draw_hist(History[-1], dim, n)
            Final_Coherent[v] = ((hist[0, 0] + hist[2, 2]) / n)
            Final_Incoherent[v] = ((hist[0, 2] + hist[2, 0]) / n)
            Final_Apathetic[v] = ((hist[1, 1]) / n)
            Final_Weak[v] = (hist[1, 0] + hist[1, 2] + hist[0, 1] + hist[2, 1]) / n

            #print('v=', v)
        #print('k=', k)

        # Save all the final states to calculate the error
        df_Final = pd.DataFrame([Final_Coherent, Final_Incoherent, Final_Apathetic, Final_Weak],
                                ['Coherent', 'Incoherent', 'Apathetic', 'Weak'])
        
        csv_name= Name + '/Finals_Error' + str(k) + '.csv'
        df_Final.to_csv(csv_name)
        print(csv_name)

        # calculate the mean and error for each value for each k.
        mean = (df_Final.T[1:]).mean(axis=0)
        error = (df_Final.T[1:]).std(axis=0)
        Total_mean.append(mean)
        Total_error.append(error)
        
    #make dataframes
    Total_mean = np.array(Total_mean)
    Total_error = np.array(Total_error)
    
    df_mean = pd.DataFrame([K, Total_mean.T[0], Total_mean.T[1], Total_mean.T[2], Total_mean.T[3]],
                           ['K', 'Coherent', 'Incoherent', 'Apathetic', 'Weak'])
    df_error = pd.DataFrame([K, Total_error.T[0], Total_error.T[1], Total_error.T[2], Total_error.T[3]],
                                ['K', 'Coherent', 'Incoherent', 'Apathetic', 'Weak'])

    df_mean.to_csv(Name + '/Finals_mean.csv')
    df_error.to_csv(Name + '/Finals_error.csv')

        
#%% Run for various k values, REJECTION saving the error 

# Conditions
step = 0.05 #For the value of k
K = np.arange(0, 1 + step, step)
Condition = '2-4' # For other  model variants. We finally only use 2-4
elseClause = 'rejection' 


#File and directory names
Name = 'Simulations_Else=' + elseClause + '_Error'


final_directory = os.path.join(current_directory, Name)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
   
#RUN
Total_Run_Error(Name, Condition, elseClause, K, num_interactions=100, Repetitions=100)


#%% Run for various k values, saving temporal data but not the error

# Conditions
step = 0.05 #For the value of k
K = np.arange(0, 1 + step, step)
Condition = '2-4' # For other  model variants. We finally only use 2-4
elseClause = 'rejection' 


#File and directory names
Name = 'Simulations_Else=' + elseClause + '_Classic'


final_directory = os.path.join(current_directory, Name)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
   
   
Total_Run(Name, Condition, elseClause, K, num_interactions=100, Repetitions=100)


#%% Run for various k values, saving the error (Can be adapted to save temporary data but not the error)

# Conditions
step = 0.05
K = np.arange(0, 1 + step, step)
Condition = '2-4'
elseClause = 'pass'

#File and directory names
Name = 'Simulations_Else=' + elseClause + '_Error'

final_directory = os.path.join(current_directory,  Name)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
    
#RUN
Total_Run_Error(Name, Condition, elseClause, K, num_interactions=100, Repetitions=100)


#%% Run for various k values, saving the error (Can be adapted to save temporary data but not the error)

# Conditions
step = 0.05
K = np.arange(0, 1 + step, step)
Condition = '2-4'
elseClause = 'pass'

#File and directory names
Name = 'Simulations_Else=' + elseClause + '_Classic'

final_directory = os.path.join(current_directory,   Name)
if not os.path.exists(final_directory):
   os.makedirs(final_directory)
    
#RUN
Total_Run(Name, Condition, elseClause, K, num_interactions=100, Repetitions=100)


#%% 3D Histogram Figure
##Figure 2 inset: 3d histograms

#Modelo conditions
elseClause = 'rejection'
Name =  'Histogram_Else=' + elseClause 

k = 0.8
n = 1000
dim = 2
num_interactions = 300
hist = np.zeros((3, 3))
Repetitions = 10

#Run but save the final hisogram
for v in range(Repetitions):
    History = run(n, dim, num_interactions, k, Condition, elseClause)
    hist += draw_hist(History[-1], dim, n) / Repetitions

hist = hist / n

#PLOT
xedges = np.array([-1, 0, 1])
yedges = np.array([-1, 0, 1])

xpos, ypos = np.meshgrid(xedges + 0.25, yedges + 0.25, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0

# Construct arrays with the dimensions for the 16 bars.
dx = dy = 0.5 * np.ones_like(zpos)
dz = hist.ravel()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
ax.invert_xaxis()
plt.xticks(xedges + 0.5, xedges)
plt.yticks(yedges + 0.5, yedges)
ax.set_zticks([0, 0.1, 0.2, 0.3])

plt.savefig("Distribution_No_Politicians.png", transparent=True) #k=0.1
#plt.savefig("Distribution_Politicians.png", transparent=True) #k=0.9