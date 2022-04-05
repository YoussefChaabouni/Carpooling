'''
In this file, we allow experiments on specific variables with the ability to save the results.
The hyperparameters are :
 - Drivers distribution
 - Riders distribution
 - Walking speed
 - detour rate 
'''
from mapGeneration import data_generation
from PersonClasses import Rider
from mapGeneration import load_simulation_data
from paper_friendly_all_systems_simulation import simulation, plot_data
import os
import pickle
import numpy as np

number_of_simulations = 10 #this number allows to run a single simulation multiple times
riders_distribution = [8.3]
drivers_distribution = [4.8]
walking_speed = [5]
detour_ratio = [0.15]


def run_simulations(drivers_distribution,riders_distribution,walking_speed,detour_ratio):
    
    experiment_number = 1

    if not os.path.exists('experiments'):

        os.makedirs("experiments")
    else:
        import shutil
        shutil.rmtree('experiments/') 
        os.makedirs("experiments")

    total_number_of_experiments = len(drivers_distribution)*len(walking_speed)*len(detour_ratio)*len(riders_distribution)
    # empty experiments data file
    open('experiments/experiments_data.txt', 'w').close()
    

    data_generation()

    simulations_list, data_index = load_simulation_data(drivers_distribution,riders_distribution,walking_speed,detour_ratio)

    for i in range(len(simulations_list)):
                    
                    #np.random.seed(123)
                    experiment_number = i+1
                    drivers = simulations_list[i][1]
                    riders_list = simulations_list[i][0]
                    G = simulations_list[i][2]

                    dd = data_index[i][0]
                    rd = data_index[i][1]
                    ws = data_index[i][2]
                    dr = data_index[i][3]

                    print("experiment number = ",experiment_number,"/",total_number_of_experiments)
                    # directory containing the results

                    global_riders = []
                    global_drivers = []
                    global_solutions = []
                    global_times = []

                    newpath = 'experiments/'+'exp_'+str(experiment_number)
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    #else :
                        # remove the directory if it had previous experiments
                    #    os.remove(newpath)
                    #    os.makedirs(newpath)
                


                    EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES  = simulation(drivers,riders_list,G=G,save_path=newpath)
                    
                    plot_data(EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES,newpath)
                    save_results_data(newpath,EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES)

                    global_riders.append(EFFECTIVE_RIDERS)
                    global_drivers.append(EFFECTIVE_DRIVERS)
                    global_solutions.append(EFFECTIVE_SOLUTIONS)
                    global_times.append(EFFECTIVE_TIMES)
                
                    #opening the experiments data logs and writing the variables
                    with open('experiments\experiments_data.txt', 'a') as the_file:
                        the_file.write("______________experiment number "+str(experiment_number)+"-_______________\n")
                        the_file.write("Drivers distribution = "+str(dd)+"\n")
                        the_file.write("Riders distribution = "+str(rd)+"\n")
                        the_file.write("Walking speed = "+str(ws)+"\n")
                        the_file.write("Detour ratio = "+str(dr)+"\n")



                    #experiment_number +=1
            
    return EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, EFFECTIVE_SOLUTIONS,EFFECTIVE_TIMES


def save_results_data(path,EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES):

        
        # creating data folder
        newpath = path+"/data"
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        # Saving the objects:
        with open(newpath+'/'+'riders.pkl', 'wb') as f:  
            pickle.dump(EFFECTIVE_RIDERS, f)
        
        with open(newpath+'/'+'drivers.pkl', 'wb') as f:  
            pickle.dump(EFFECTIVE_DRIVERS, f)

        with open(newpath+'/'+'solutions.pkl', 'wb') as f:  
            pickle.dump(EFFECTIVE_SOLUTIONS, f)

        with open(newpath+'/'+'times.pkl', 'wb') as f:  
            pickle.dump(EFFECTIVE_TIMES, f)

        with open(newpath+'/'+'graphs.pkl', 'wb') as f:  
            pickle.dump(ALL_GRAPHS, f)

        # Getting back the objects:
        #with open('objs.pkl') as f:  # Python 3: open(..., 'rb')
        #    obj0, obj1, obj2 = pickle.load(f)
        
        return 0
'''
def make_average(global_riders,global_drivers,global_solutions,global_times):

    riders = []
    drivers = []
    solutions = []
    times = []

    for i in range(len(global_riders[0])):
        r = Rider(
        pos_depart = global_riders[0][i].pos_depart,
        pos_arrivee = global_riders[0][i].pos_depart,
        ID = global_riders[0][i].id,
        born_time=global_riders[0][i].born_time,
        walking_speed = global_riders[0][i].walking_speed,
        trajectory=)
        r.trajectory = Trajectory(means_list=[Foot(Speed=5/60,ID="init "+r.get_id())],
        arr_time_list=[r.born_time],
        dep_time_list=[r.born_time],
        
        node_list=[r.pos_depart]   
        )

    return riders,drivers,solutions,times
'''
EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, EFFECTIVE_SOLUTIONS,EFFECTIVE_TIMES = run_simulations(drivers_distribution,riders_distribution,walking_speed,detour_ratio)
