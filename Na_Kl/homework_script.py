print("Let's start!")
import os   # allows python to handle files as in bash
import iris    #  handling cubes of big data
import iris.coord_categorisation  # allows you to add new coordinates to your data cube
import iris.plot as iplt # a quickplot option from the Iris package
import iris.quickplot as qplt

import matplotlib.pyplot as plt # the package doing the plotting
import datetime # handles dates

import cartopy  # helps to create maps
import cartopy.crs as ccrs # helps to create maps
import numpy as np  # handles arrays
# this makes sure that your plots pop up in the notebook and no extra window is opened: 
%matplotlib inline  
# Some defaults:
plt.rcParams['figure.figsize'] = (12, 5)  # Default plot size
np.set_printoptions(threshold=20)  # avoid to print very large arrays on screen

path ='/nfs/a266/data/CMIP5_AFRICA/mdlgrid/HadGEM2-ES/historical/'
file = 'tas_day_HadGEM2-ES_africa_historical_r1i1p1_full.nc'

iris.FUTURE.netcdf_promote = True
cubes = iris.load(path+file)
print(cubes)

f=plt.figure()   # open a figure
for t in range(4):   # start loop of 0,1,2,3 - python neglects the last step in ranges! 
    # specify plot axis with projection. 2,2,t+1 means a 2x2 plot with t+1 being the current plot index. 
    ax = f.add_subplot(2,2,t+1, projection=ccrs.PlateCarree())    # set ploting area to 2by2
    iplt.contourf(cubes[0][t,:,:])  # filled contour plot
    ax.coastlines()  # add coastlines to axis
    # Gridlines
    xl = ax.gridlines(draw_labels=True) # draw gridlines
    xl.xlabels_top = False
    xl.ylabels_right = False
    # Countries
    ax.add_feature(cartopy.feature.BORDERS, linestyle='--')
    plt.colorbar()
plt.show()

# take a subset for west africa only

WA_lat=iris.Constraint(latitude=lambda cell: 4 <= cell <= 25.0) # latitude constraint 4-25N
WA_lon=iris.Constraint(longitude=lambda cell: -18 <= cell <= 25.0) # longitude constraint 18W - 25E

precip = precip.extract(WA_lat & WA_lon) # apply constraints
precip.convert_units('Celsius')  # convert unit

# Add the month coordinate
iris.coord_categorisation.add_month_number(precip, 'time', name='month')

perc = precip.aggregated_by('month', iris.analysis.PERCENTILE, percent=95)

qplt.contourf(perc[7])
d = plt.gca() # get axis object
d.coastlines() # to draw coastlines


