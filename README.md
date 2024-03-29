# Attraction by ingroup coherence explains the emergence of ideological sorting

These are the scripts and simulated data for:

> Zimmerman, F., Pedraza, L., Navajas, J., & Balenzuela, P. (2023). Attraction by ingroup coherence drives the emergence of ideological sorting. arXiv preprint arXiv:2304.12559.

## Project abstract

Political polarization has become a growing concern in democratic societies, as it drives tribal alignments and erodes civic deliberation among citizens. Given its prevalence across different countries, previous research has sought to understand the conditions under which people tend to endorse extreme opinions. However, in polarized contexts, citizens not only adopt more extreme views but also become more correlated across issues which are, a priori, seemingly unrelated. This phenomenon, known as “ideological sorting”, has been increasing in recent years but the micro-level mechanisms underlying its emergence remain poorly understood. Here, we study the conditions under which a social dynamic system is expected to become ideologically sorted as a function of the mechanisms of interaction between its individuals. To this end, we developed and analyzed a multidimensional agent-based model that incorporates two mechanisms: homophily (where people tend to interact with those holding similar opinions) and ingroup-coherence favoritism (where people tend to interact with ingroups holding politically coherent opinions). We developed and solved the model’s master equations that perfectly describe the system’s dynamics and found that ideological sorting only emerges in models that include ingroup-coherence favoritism. We then compared the model’s outcomes with empirical data proceeding from 24,035 opinions across 67 topics, and found that ingroup-coherence favoritism is significantly present in datasets that measure political attitudes, but it is absent across non-political topics. Overall, this work combines theoretical approaches from system dynamics with model-based analyses of empirical data to uncover a potential mechanism underlying the pervasiveness of ideological sorting.


## Necessary packages for this model

* Python: All Python packages for this project can be found in <requirements.txt> and can easily be installed with <pip install -r requirements.txt> from command line.

* R: dplyr, haven.
	
This repository comprises the following components:

**Scripts**:

* **simulations.py**: This script contains the code required to perform simulations of the model.
* **load_equations.py**: It encompasses the analytically developed equations.
* **draw_all.py**: This script is designed for plotting the simulation results, conducting comparisons with the equations, and analyzing them alongside the empirical data.
* **CompleteAnalysis.r**: This script facilitates the processing and derivation of the mean proportion of coherence from the data.

**Data and Simulations**:

* **ExportFromPython.csv**: This file stores the processed real data.
* **Simulations_Else=rejection_Classic.txt**: These files encompass all simulations, including intermediate states, pertaining to the mean proportions of each population within the repulsive model.
* **Simulations_Else=pass_Classic.txt**: These files contain all simulations, including intermediate states, pertaining to the mean proportions of each population within the non-repulsive model.
* **Simulations_Else=rejection_Error.txt**: These files capture the final states of each simulation for every instance, providing insights into the error distribution within the repulsive model.
* **Simulations_Else=pass_Error.txt**: These files record the ultimate states of each simulation for each occurrence, providing insights into the error distribution within the non-repulsive model.

**Figures**:

The generated graphics are also accessible in both .pdf and .jpg formats.
