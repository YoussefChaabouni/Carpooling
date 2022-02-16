'''
In this file, we allow experiments on specific variables with the ability to save the results.
The hyperparameters are :
 - Drivers distribution
 - Riders distribution
 - Walking speed
 - detour rate 
'''
from mapGeneration import data_generation
from paper_friendly_all_systems_simulation import simulation, plot_data
import os
import pickle

riders_distribution = [8.3]
drivers_distribution = [7]
walking_speed = [3,5,10]
detour_ratio = [0.15,0.5,0.75]


def run_simulation(drivers_distribution,riders_distribution,walking_speed,detour_ratio):
    
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
                    EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES  = simulation(drivers,riders_list,G=G,save_path=newpath)
                    plot_data(EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES,newpath)
                    save_results_data(newpath,EFFECTIVE_RIDERS, EFFECTIVE_DRIVERS, ALL_GRAPHS, EFFECTIVE_SOLUTIONS, EFFECTIVE_TIMES)
                    #opening the experiments data logs and writing the variables
                    with open('experiments\experiments_data.txt', 'a') as the_file:
                        the_file.write("______________experiment number "+str(experiment_number)+"_______________\n")
                        the_file.write("Drivers distribution = "+str(dd)+"\n")
                        the_file.write("Riders distribution = "+str(rd)+"\n")
                        the_file.write("Walking speed = "+str(ws)+"\n")
                        the_file.write("Detour ratio = "+str(dr)+"\n")



                    experiment_number +=1
            
    return 0


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


run_simulation(drivers_distribution,riders_distribution,walking_speed,detour_ratio)
