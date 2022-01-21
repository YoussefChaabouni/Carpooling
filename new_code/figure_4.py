import numpy as np
import matplotlib.pyplot as plt

# regarder les point de départ et d'arriver et executer la fonction du graph
# regarder la trajectory pour la liste des arrival times [-1] - [0]

def figure_4(T_t,T_d, C_t,C_d, I_t,I_d, T_d_inf,C_d_inf,I_d_inf):
	# T, C, I : Transit(no carpooling), Carpooling only, Integrated
	# _t : time in minutes
	# _d : distance in km
	# _inf : with infinite time (unserved riders)

	fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True,gridspec_kw={'height_ratios': [1, 3]}) # 'width_ratios'

	fig.suptitle('Systems comparison',fontsize = 20)

	#plt.xlabel("km")
	#plt.ylabel("minutes")

	axs[0,0].scatter(T_d_inf, np.random.random(len(T_d_inf))*100,color='green',s=1.75) # blue,green,red,purple
	axs[1,0].scatter(T_d, T_t,color='green',s=1.75)
	axs[1,0].set_xlabel("Travel time (minutes)")
	axs[1,0].set_ylabel("Distance between origin and destination (km)")

	axs[1,0].grid()
	axs[1,0].set_title('No carpooling system',fontsize = 10)

	axs[0,1].scatter(C_d_inf, np.random.random(len(C_d_inf))*100,color='orange',s=1.75) # blue,green,red,purple
	axs[1,1].scatter(C_d, C_t,color='orange',s=1.75)

	axs[1,1].grid()
	axs[1,1].set_title('Current system',fontsize = 10)

	axs[0,2].scatter(I_d_inf, np.random.random(len(I_d_inf))*100,color='purple',s=1.75) # blue,green,red,purple
	axs[1,2].scatter(I_d, I_t,color='purple',s=1.75)

	axs[1,2].grid()
	axs[1,2].set_title('Integrated system',fontsize = 10)


	plt.show()

if __name__=="__main__":
	vecteur1 = np.random.random(100)*100
	vecteur2 = np.linspace(1,100,100)
	vecteur3 = np.random.random(50)*100
	figure_4(vecteur1,vecteur2,vecteur1,vecteur2,vecteur1,vecteur2, vecteur3,vecteur3,vecteur3)