## plot intgeration efficiencies on x and y axis
import pandas as pd
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.linalg

# test function
def function(data, b, c):
    x = data[0]
    y = data[1]
    return (x**b) + (y**c)





df=pd.read_excel('Intgeration_efficiencies.xlsx')
dispens_df=df[df['Phenotype']=='Dispensable'] ## dispensible genes


df_plot=dispens_df[['integration_effciencies','left_arm_length','right_arm_length']]
df_plot=df_plot.dropna(axis=0)
# Data for three-dimensional scattered points
X=df_plot['left_arm_length'].values
Y= df_plot['right_arm_length'].values
# Z=np.sqrt(df_plot['integration_effciencies'].values)
Z=df_plot['integration_effciencies'].values
value_max=15000
X2=X[(X<value_max) & (Y<value_max)]
Y2=Y[(X<value_max) & (Y<value_max)]
Z2=Z[(X<value_max) & (Y<value_max)]

data = np.c_[X2,Y2,Z2]

# regular grid covering the domain of the data
mn = np.min(data, axis=0)
mx = np.max(data, axis=0)
npoints=30
X1,Y1 = np.meshgrid(np.linspace(mn[0], mx[0],npoints ), np.linspace(mn[1], mx[1],npoints))
XX = X1.flatten()
YY = Y1.flatten()
order=2
if order==1:
    # best-fit linear plane (1st-order)
    A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients

    # evaluate it on grid
    Z1 = C[0]*X1 + C[1]*Y1 + C[2]
else:
    # best-fit quadratic curve
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])

    # evaluate it on a grid
    Z1 = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X1.shape)









# parameters, covariance = curve_fit(function, [X2, Y2], Z2)
# model_x_data = np.linspace(min(X2), max(X2), 30)
# model_y_data = np.linspace(min(Y2), max(Y2), 30)
# X1, Y1 = np.meshgrid(model_x_data, model_y_data)
# # calculate Z coordinate array
# Z1 = function(np.array([X1, Y1]), *parameters)

# Rotate it
fig = plt.figure()
ax = fig.gca(projection='3d')
#surf=ax.plot_trisurf(X,Y,Z, cmap=cm.jet, linewidth=0.2)



surf = ax.plot_surface(X1, Y1, Z1, cmap=cm.jet,linewidth=0.5, antialiased=False)
#
# surf=ax.scatter(X, Y, Z, c=Z,cmap=cm.jet)
# surf=ax.plot_wireframe(X1, Y1, Z1, rstride=10, cstride=10)

fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel('left_arm_length')
ax.set_ylabel('right_arm_length')
ax.set_zlabel('integration effciencies')
plt.show()





# ax.scatter3D(, c= df_plot['integration_effciencies'].values, cmap='Greens');
import pdb; pdb.set_trace()
