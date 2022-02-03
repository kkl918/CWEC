import netCDF4 as nc
from netCDF4 import Dataset

nc_file1 = r"C:\Users\USER\Desktop\OCMweb20220120.nc"
# nc_file2 = r"C:\Users\USER\Desktop\OCM2T20220112.nc"
# nc_file = r"/home1/cwecA/OPENDAP/20220111/OCMweb202111.nc"
# nc_file = r"/home1/cwecA/OPENDAP/20220111/OCMweb20220111.nc"
rootgrp1 = Dataset(nc_file1, "r", format="NETCDF4")
rootgrp2 = Dataset(nc_file2, "r", format="NETCDF4")
print(rootgrp1.variables.keys())
print('\n\n***\n\n')
print(rootgrp1.variables)
# lev  =rootgrp.variables['lev'][:].data
# print(lev)