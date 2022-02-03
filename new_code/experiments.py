'''
In this file, we allow experiments on specific variables with the ability to save the results.
The hyperparameters are :
 - Drivers distribution
 - Riders distribution
 - Walking speed
 - detour rate 
'''
from mapGeneration import data_generation
from paper_friendly_all_systems_simulation import simulation
import os

riders_distribution = [2]
drivers_distribution = [1]
walking_speed = [4,6,8,10]
detour_ratio = [0.15,0.25,0.35]


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

    for dd in drivers_distribution:
        for rd in riders_distribution :
            for ws in walking_speed :
                for dr in detour_ratio:
                    print("experiment number = ",experiment_number,"/",total_number_of_experiments)
                    # directory containing the results
                    newpath = 'experiments/'+'exp_'+str(experiment_number) 
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    #else :
                        # remove the directory if it had previous experiments
                    #    os.remove(newpath)
                    #    os.makedirs(newpath)
                    

                    # run simulation and data generation
                    riders_list, drivers, G = data_generation(dd,rd,ws,dr)
                    plots = simulation(drivers,riders_list,G=G,save_path=newpath)

                    #opening the experiments data logs and writing the variables
                    with open('experiments\experiments_data.txt', 'a') as the_file:
                        the_file.write("______________experiment number "+str(experiment_number)+"_______________\n")
                        the_file.write("Drivers distribution = "+str(dd)+"\n")
                        the_file.write("Riders distribution = "+str(rd)+"\n")
                        the_file.write("Walking speed = "+str(ws)+"\n")
                        the_file.write("Detour ratio = "+str(dr)+"\n")



                    experiment_number +=1
            
    return 0

run_simulations(drivers_distribution,riders_distribution,walking_speed,detour_ratio)