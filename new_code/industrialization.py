from experiments import hyperparameter_tuning
import pandas as pd

def generate_parameters(intervals_dict):

    parameters_dict = {
    "RIDER": [],
    "DRIVER": [],
    "WALKING" : [],
    "DETOUR": []
    }
    keys = intervals_dict.keys()
   
    for parameter in keys :    
               
        minimum = intervals_dict[parameter][0]
        maximum = intervals_dict[parameter][1]
        step = intervals_dict[parameter][2]

        value = minimum
        while value <= maximum :
                        
            parameters_dict[parameter].append([value])
            value += step



    return parameters_dict

def initialize_dataframe():
    df_path = 'dataframe/simulation_history_df.pkl'
    df_unpickled = pd.read_pickle(df_path)
    columns = list(df_unpickled)
    df = pd.DataFrame(columns = columns)
    df.to_pickle(path = df_path)
    return df

df = initialize_dataframe()
df_unpickled = pd.read_pickle('dataframe/simulation_history_df.pkl')
print(df_unpickled.head(5))

intervals_dict = {"RIDER" : [1,9,2],"DRIVER" : [1,9,2],"WALKING" : [4,6,1],"DETOUR" : [0,0.30,0.05]}

print(intervals_dict)

parameters_dict = generate_parameters(intervals_dict)

print(parameters_dict)

hyperparameter_tuning(parameters_dict['RIDER'],parameters_dict['DRIVER'],parameters_dict['WALKING'],parameters_dict['DETOUR'])

