@author Paul Ardant & Cheikh Malainine Cheikh Melainine

This is the result of our work from the "Pooling for the first and last mile" paper
You can find the said paper in carpooling.pdf

Here is how this branch's folder works :
  - Diagramme de classe : self explanatory
  - includes : everything you need to make simulations.
      --> the different classes from the diagram are implement in 3 files (graphClasses.py, personClasses.py and vehicleClasses.py)
      --> Algorithms.py contains the different algorithms described in the paper
      --> Simulation_variable.py is the file where you can easily changes the variables of each simulation
      --> Simulation1 launches a simulation based on the first 3 algorithms 
      --> Simulation2 is the first type of simulation we made : it launches a simulation based on the first 3 algorithms only
      --> Simulation3 launches a simulation based on all 4 algorithms
      --> Simulation4 launches a simulation based on the first 3 algorithms
      --> plotMap.py and ploting_results.py are used to hace a visual result of the simulations

  - Results : saves data from simulation so that the data we have can be more precise
      --> see the README.md file for more details

The file running_sim1.sh is used to execute repeeadly the file Simulation1.py (the number of simulation is asked when executing the file)
The file running_sim2.sh is used to execute repeeadly the file Simulation2.py (the number of simulation is asked when executing the file)
## It's important to change the files in Simulation1 or 2 before launching several simulation if the paremeters have changed
## Also don't forget to uncomment the end of those files in order to save the results
