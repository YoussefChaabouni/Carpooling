import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

def served_unserved_calculus(row):
	carpooling = 0
	foot = 0
	transit = 0
	no_solution = 0
	integrated = 0

	for solution in row['EFFECTIVE_SOLUTIONS'][2]:
		if solution == "carpooling":
			carpooling +=1
		if solution == "transit":
			transit += 1
		if solution == "foot":
			foot += 1
		if solution == "no solution":
			no_solution +=1
		if solution == "integrated":
			integrated +=1

	NUMBER_OF_RIDERS = len(row['EFFECTIVE_SOLUTIONS'][2])

	carpooling = carpooling / NUMBER_OF_RIDERS
	foot = foot / NUMBER_OF_RIDERS
	transit = transit / NUMBER_OF_RIDERS
	no_solution = no_solution / NUMBER_OF_RIDERS
	integrated = integrated / NUMBER_OF_RIDERS

	served_ratio = carpooling + foot + transit + integrated

	return served_ratio, no_solution, integrated
	
	
def average_vehicule_occupancy_calculus(row):
	means = []
	for system in range(1,3):
		mean = 0
		for d in row['EFFECTIVE_DRIVERS'][system]:
			current_capacity_list = d.get_current_capacity()
			maximum_capacity = d.max_capacity
			riders_aboard = maximum_capacity - np.array(current_capacity_list)
			mean += np.max(riders_aboard)
		means.append(mean/len(row['EFFECTIVE_DRIVERS'][system]))
	return means[0], means[1]
	
	
def average_waiting_walking_time(row):
	avg_waiting = []
	avg_walking = []
	for system in range(3):

		average_walking = 0
		average_waiting = 0
		relevant_rider_counter = 0 #don't count not served riders
		for rider in row['EFFECTIVE_RIDERS'][system] :
			if rider.waiting_time != np.Infinity and rider.born_time<60:
				average_walking += rider.walking_distance*5
				average_waiting += rider.waiting_time
				relevant_rider_counter +=1
		
		average_walking =(average_walking)/ relevant_rider_counter
		average_waiting /= relevant_rider_counter
		avg_waiting.append(average_waiting)
		avg_walking.append(average_walking)
	return avg_waiting, avg_walking

def plot_evolution_by_parameter(df_analysis,parameter : str,result_metric : str,savepath):

	
	g = sns.catplot(
    data=df_analysis, kind="bar",
    x=parameter, y=result_metric,
    ci="sd", palette="dark", alpha=.6, height=6
	)
	g.despine(left=True)
	g.set_axis_labels(parameter, result_metric)	

	if savepath != "" :
		plt.savefig(savepath+"/Evolution par paramètre.png",format='png')
	plt.show()

def df_analysis_preprocessing(df_analysis):
	
	for key in df_analysis['PARAMETRES'][0].keys():

		parameter_list = []

		for id,row in df_analysis.iterrows():
			parameter_list.append(row['PARAMETRES'][key])

		df_analysis[str.upper(key)] = parameter_list
	
	return df_analysis
	
def heatmap(df_analysis,columns,savepath):

	plt.figure(figsize=(10, 6))

	dataframe = df_analysis[columns]
	sns.heatmap(dataframe.corr(), vmin=-1, vmax=1, annot=True)
	plt.show()
	if savepath != "" :
		plt.savefig(savepath+"/Heatmap.png",format='png')

def all_row_analysis(df_analysis):
	list_served_ratio = []
	list_unserved_ratio = []
	list_integrated_ratio = []
	list_avg_max_occupancy_current = []
	list_avg_max_occupancy_integrated = []
	list_avg_waiting_time_no_cp = []
	list_avg_waiting_time_current = []
	list_avg_waiting_time_integrated = []
	list_avg_walking_time_no_cp = []
	list_avg_walking_time_current = []
	list_avg_walking_time_integrated = []
	
	for id, row in df_analysis.iterrows():
		served_ratio, no_solution, integrated = served_unserved_calculus(row)
		list_served_ratio.append(served_ratio)
		list_unserved_ratio.append(no_solution)
		list_integrated_ratio.append(integrated)
		
		avg_current, avg_integrated = average_vehicule_occupancy_calculus(row)
		list_avg_max_occupancy_current.append(avg_current)
		list_avg_max_occupancy_integrated.append(avg_integrated)
		
		avg_waiting, avg_walking = average_waiting_walking_time(row)
		list_avg_waiting_time_no_cp.append(avg_waiting[0])
		list_avg_waiting_time_current.append(avg_waiting[1])
		list_avg_waiting_time_integrated.append(avg_waiting[2])
		list_avg_walking_time_no_cp.append(avg_walking[0])
		list_avg_walking_time_current.append(avg_walking[1])
		list_avg_walking_time_integrated.append(avg_walking[2])
		
		
	df_analysis['SERVED_RATIO'] = list_served_ratio
	df_analysis['UNSERVED_RATIO'] = list_unserved_ratio
	df_analysis['INTEGRATED_RATIO'] = list_integrated_ratio
	df_analysis['AVG_MAX_OCCUPANCY_CURRENT'] = list_avg_max_occupancy_current
	df_analysis['AVG_MAX_OCCUPANCY_INTEGRATED'] = list_avg_max_occupancy_integrated
	df_analysis['AVG_WAITING_TIME_NO_CP'] = list_avg_waiting_time_no_cp
	df_analysis['AVG_WAITING_TIME_CURRENT'] = list_avg_waiting_time_current
	df_analysis['AVG_WAITING_TIME_INTEGRATED'] = list_avg_waiting_time_integrated
	df_analysis['AVG_WALKING_TIME_NO_CP'] = list_avg_walking_time_no_cp
	df_analysis['AVG_WALKING_TIME_CURRENT'] = list_avg_walking_time_current
	df_analysis['AVG_WALKING_TIME_INTEGRATED'] = list_avg_walking_time_integrated	
	#print(df_analysis.head(5))

def main():
	df_path = 'dataframe/simulation_history_df.pkl'
	df_unpickled = pd.read_pickle(df_path)
	df_analysis = df_unpickled.copy()
	print(df_analysis.head(5))	
	all_row_analysis(df_analysis)
	df_analysis = df_analysis_preprocessing(df_analysis)
	print(df_analysis.head(5))
	plot_evolution_by_parameter(df_analysis,parameter= "DETOUR_RATIO",result_metric = "SERVED_RATIO" ,savepath = "")
	columns = ['SERVED_RATIO','INTEGRATED_RATIO','AVG_MAX_OCCUPANCY_CURRENT','AVG_MAX_OCCUPANCY_INTEGRATED',
	'AVG_WAITING_TIME_INTEGRATED' , 'AVG_WALKING_TIME_NO_CP','AVG_WALKING_TIME_CURRENT' , 'AVG_WALKING_TIME_INTEGRATED',
	'DRIVERS_DISTRIBUTION',  'RIDERS_DISTRIBUTION'  ,'WALKING_SPEED'  ,'DETOUR_RATIO']
	heatmap(df_analysis,columns,"")

main()
	