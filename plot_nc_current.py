import netCDF4           as nc
import numpy             as np
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset
import datetime, math
# from mpl_toolkits.basemap import Basemap
# k = Basemap(projection='merc',urcrnrlat=21, llcrnrlat=23,llcrnrlon=120, urcrnrlon=122) 

nc_file2 = r"C:\Users\USER\Desktop\OCMweb20220414.nc"
rootgrp2 = Dataset(nc_file2, "r", format="NETCDF4")

print(nc_file2)


def print_info():
    print(nc_file1,rootgrp1)
    print(nc_file1, 'water_u shape:',rootgrp1.variables['WATER_U'].shape)
    print(rootgrp1.variables['WATER_U'][:].data)
    print('\n\n***\n\n')
    print(nc_file2,rootgrp2)

    print('water_u shape:', rootgrp2.variables['water_u'][0][0].shape)
    print('water_v shape:', rootgrp2.variables['water_v'][0][0].shape)
    print('lat     shape:', rootgrp2.variables['lat'].shape)
    print('lon     shape:', rootgrp2.variables['lon'].shape)


def xy2degree(x,y):
    ans = 0
    if math.atan2(x,y)/math.pi*180 < 0:
        ans = math.atan2(x,y)/math.pi*180 + 360
    else:
        ans = math.atan2(x,y)/math.pi*180
    return(ans)
    

def plot_singe_point():

    target_lat = 24.2239
    target_lon = 120.4197
    
    target_name = 'Penghu'
    target_lat = 23.7283
    target_lon = 119.5519    
    
     
    # target_name = 'Hsinchu'
    # target_lat = 24.7628
    # target_lon = 120.8428

    # 台中港北堤燈塔
    # target_name = 'Taichung'
    # target_lat = 24.2997
    # target_lon = 120.4867

    # 緯度
    lat = rootgrp2.variables['lat']
    LATcloset = np.array(([math.sqrt(float((i-target_lat)*(i-target_lat))) for index, i in enumerate(lat)]))
    LATid     =  np.where(LATcloset == LATcloset.min())[0][0]

    LATcloset = (lat[np.where(LATcloset == LATcloset.min())[0][0]])

    # 經度
    lon = rootgrp2.variables['lon']
    LONcloset = np.array(([math.sqrt(float((i-target_lon)*(i-target_lon))) for index, i in enumerate(lon)]))
    LONid     =  np.where(LONcloset == LONcloset.min())[0][0]
    LONcloset = (lon[np.where(LONcloset == LONcloset.min())[0][0]])

    print(LATcloset, LATid)
    print(LONcloset, LONid)

    # 時間管理大師
    t   = rootgrp2.variables['time']
    init_t   =  datetime.datetime(1800, 1,  1,  0, 0)
    start_t  =  datetime.datetime(2022, 4, 14, 22, 0)
    end_t    =  datetime.datetime(2022, 4, 14, 22, 0)+datetime.timedelta(hours=24)
    
    log = open(r'C:\Users\USER\Desktop\{}.csv'.format(target_name), 'w')
    log.write('{},{}\n'.format(start_t, end_t))
    log.write('{},{}\n'.format('CURRENT SPEED(m/s))', 'CURRENT DIRECTION(degree)'))
    for i in range(len(t)):
        theTIME = init_t+datetime.timedelta(hours=int(t[i]))
        # print(theTIME)
        if theTIME == start_t:
            start_id = i
        elif theTIME == end_t:
            end_id = i

    vs = [];
    ds = [];
    for i in range(0, end_id-start_id):
        u = rootgrp2.variables['water_u'][start_id:end_id]
        v = rootgrp2.variables['water_v'][start_id:end_id]


        uu = rootgrp2.variables['water_u'][start_id:end_id][i][0][LONid][LATid]
        vv = rootgrp2.variables['water_v'][start_id:end_id][i][0][LONid][LATid]

        
        scale = math.sqrt(uu*uu+vv*vv)
        direction = xy2degree(uu,vv)
        vs.append(scale)
        ds.append(direction)
        print(scale, xy2degree(uu,vv))
        log.write('{},{}\n'.format(scale, xy2degree(uu,vv)))

    title1 = '{} CURRENT SPEED(m/s)({},{}) \nfrom {} to {}'.format(target_name       ,target_lon,target_lat,start_t, end_t)    
    title2 = '{} CURRENT DIRECTION(degree)({},{}) \nfrom {} to {}'.format(target_name, target_lon,target_lat,start_t, end_t)    

    ax1 = plt.subplot(2,1,1)
    plt.plot(vs)
    plt.title(title1)
    plt.grid()
    ax1.set_xticks(range(0,24,1))
    ax1.set_xticks([0,20], minor=True)

    ax2 = plt.subplot(2,1,2)
    plt.subplot(2,1,2)
    plt.plot(ds)
    plt.title(title2)
    plt.grid()

    ax2.set_xticks(range(0,24,1))

    plt.show()

   
def plot_all():

    for i in range(1, 5):
        #print(i)
        u = rootgrp2.variables['water_u'][i][0]
        v = rootgrp2.variables['water_v'][i][0]

        m = np.sqrt(np.power(u, 2) + np.power(v, 2))


        x,y = np.meshgrid(lon, lat)

        #x,y = k(x,y)
        
        
        plt.figure(i)
        fig = plt.quiver(x, y, u ,v, m ,scale = 10)
        # plt.xlim(119, 123)
        plt.xlim(120.425-0.01, 120.425+0.01)
        # plt.ylim(21 , 26)
        plt.ylim(24.175-.001 , 24.175+.001)
        plt.grid()
        cb = plt.colorbar(fig)
        
    plt.show()






plot_singe_point()