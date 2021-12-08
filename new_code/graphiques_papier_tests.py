import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True,gridspec_kw={'height_ratios': [1, 3]}) # 'width_ratios'

fig.suptitle('Systems comparaison')

var1 = np.linspace(1,10,25)
var2 = np.linspace(1,10,25)*2
var3 = np.linspace(1,10,25)*3


axs[0,0].scatter(var1, var2,color='green',s=1.75) # blue,green,red,purple
axs[1,0].scatter(var1, var3,color='green',s=1.75)

axs[1,0].grid()
axs[1,0].set_title('No carpooling system')

axs[0,1].scatter(var1, var2,color='orange',s=1.75) # blue,green,red,purple
axs[1,1].scatter(var1, var3,color='orange',s=1.75)

axs[1,1].grid()
axs[1,1].set_title('Current system')

axs[0,2].scatter(var1, var2,color='purple',s=1.75) # blue,green,red,purple
axs[1,2].scatter(var1, var3,color='purple',s=1.75)

axs[1,2].grid()
axs[1,2].set_title('Integrated system')

plt.show()