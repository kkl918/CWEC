import netCDF4           as nc
import numpy             as np
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset

# from mpl_toolkits.basemap import Basemap
# k = Basemap(projection='merc',urcrnrlat=21, llcrnrlat=23,llcrnrlon=120, urcrnrlon=122) 

nc_file2 = r"O:\loc_data\Taiwan\CURRENTS\OCMweb20220112.nc"
rootgrp2 = Dataset(nc_file2, "r", format="NETCDF4")

# print(nc_file1,rootgrp1)
# print(nc_file1, 'water_u shape:',rootgrp1.variables['WATER_U'].shape)
# print(rootgrp1.variables['WATER_U'][:].data)
# print('\n\n***\n\n')
# print(nc_file2,rootgrp2)

print(nc_file2)
# print('water_u shape:', rootgrp2.variables['water_u'][0][0].shape)
# print('water_v shape:', rootgrp2.variables['water_v'][0][0].shape)
# print('lat     shape:', rootgrp2.variables['lat'].shape)
# print('lon     shape:', rootgrp2.variables['lon'].shape)


lat = rootgrp2.variables['lat']
lon = rootgrp2.variables['lon']




for i in range(1, 2):
    # print(i)
    u = rootgrp2.variables['water_u'][i][0]
    v = rootgrp2.variables['water_v'][i][0]

    m = np.sqrt(np.power(u, 2) + np.power(v, 2))


    x,y = np.meshgrid(lon, lat)

    # x,y = k(x,y)
    
    
    plt.figure(i)
    fig = plt.quiver(x, y, u ,v, m ,scale = 10)
    plt.xlim(119, 123)
    plt.ylim(21 , 26)
    cb = plt.colorbar(fig)
    
    


plt.show()



