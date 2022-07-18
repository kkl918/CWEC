import netCDF4           as nc
import numpy             as np
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset
import datetime, math
# from mpl_toolkits.basemap import Basemap
# k = Basemap(projection='merc',urcrnrlat=21, llcrnrlat=23,llcrnrlon=120, urcrnrlon=122) 

# nc_file2 = r"O:\loc_data\Taiwan\CURRENTS\OCMweb20220418_new3.nc"
# nc_file2 = r"O:\loc_data\Taiwan\CURRENTS\OCMwebT20210621-30.nc"
# nc_file2 = r"O:\loc_data\Taiwan\CURRENTS\OCMweb20210818_new3.nc"
nc_file2 = r"C:\Users\USER\Desktop\OCMweb20220709.nc"
rootgrp2 = Dataset(nc_file2, "r", format="NETCDF4")

print(nc_file2)



def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def print_info():

    # init_t   =  datetime.datetime(2000, 1,  1,  0, 0)+ datetime.timedelta(hours=1941337)
    # print(init_t)
    # start_t  =  datetime.datetime(2021, 6, 21, 0, 0) + datetime.timedelta(hours=0)
    # end_t    =  start_t                              + datetime.timedelta(hours=buf)

    t = rootgrp2.variables
    print(t)
    # print(t.units)
    
    # t.units = 'hours since 2000-01-01 00:00:00'
    
    # print(t)
    # t.axis = 'T'
    # t.reference =  'UTC'
    
    
    # u = rootgrp2.variables['water_u']
    # print(u.initial_time)
    # u = rootgrp2.variables['time'].unlimited dimensions
    
    # print('\nVar shape:')
    for i in rootgrp2.variables.keys():
        print(i,rootgrp2.variables[i].shape)
    
    # print(rootgrp2.variables['water_u'][:].data)
    # print(rootgrp2.variables['water_v'])
    # print(rootgrp2.variables['WATER_U'][:].data)




def xy2degree(x,y):
    ans = 0
    if math.atan2(y,x)/math.pi*180 < 0:
        ans = math.atan2(y,x)/math.pi*180 + 360
    else:
        ans = math.atan2(y,x)/math.pi*180
    
    return(ans)
    

def plot_singe_point():
    target_name = 'OCMweb'
    target_lat = 23.4532
    target_lon = 119.203
    
    # target_name = 'Penghu'
    # target_lat = 23.7283
    # target_lon = 119.5519    
    
     
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
    buf = 24

    t   = rootgrp2.variables['time']
    
    print(t)
    
    

    
    init_t   =  datetime.datetime(2000, 1,  1,  0, 0)
    start_t  =  datetime.datetime(2022, 7,  9, 0, 0) + datetime.timedelta(hours=0)
    end_t    =  start_t                              + datetime.timedelta(hours=buf)

    log = open(r'C:\Users\USER\Desktop\{}.csv'.format(target_name), 'w')
    log.write('Location,{},{}\n'.format(LATcloset, LONcloset))
    log.write('{},{},{},U,V\n'.format('TIME', 'CURRENT SPEED(m/s))', 'CURRENT DIRECTION(degree)'))


        # print(theTIME, end_t)
    ss = [];
    ds = [];
    us = [];
    vs = [];
    xs = [];
    ys = [];
    # for i in range(0, end_id-start_id):
    end_id = 48
    start_id = 24
    
    for i in range(len(t)):
        theTIME = init_t + datetime.timedelta(hours=int(t[i]))
        # print(theTIME)
        if theTIME == start_t:
            start_id = i
        elif theTIME == end_t:
            end_id = i    
    
    for i in range(0, end_id-start_id):
        u = rootgrp2.variables['water_u'][start_id:end_id]
        v = rootgrp2.variables['water_v'][start_id:end_id]

        time = init_t + datetime.timedelta(hours=rootgrp2.variables['time'][start_id:end_id][i])
        uu   = rootgrp2.variables['water_u'][start_id:end_id][i][0][LONid][LATid]
        vv   = rootgrp2.variables['water_v'][start_id:end_id][i][0][LONid][LATid]
        
        rho, phi = cart2pol(uu, vv)
        
        
        
        scale = math.sqrt(uu*uu+vv*vv)
        direction = xy2degree(uu,vv)
        
        ss.append(scale)
        ds.append(direction)
        # ds.append(phi)
        us.append(uu)
        vs.append(vv)
        xs.append(i)
        ys.append(0)
        
        # print(time, scale, xy2degree(uu,vv), uu, vv)
        
        log.write('{}, {},{},{},{}\n'.format(time, scale, xy2degree(uu,vv), uu, vv))
        print('{}, {},{},{},{}\n'.format(time, scale, xy2degree(uu,vv), uu, vv))
    
    
    
    title1 = '{} Location {},{}(Given {}, {}) \n[{}] hrs from {} to {}'.format(target_name , str(LATcloset)[0:5], str(LONcloset)[0:5],target_lon ,target_lat,buf ,start_t, end_t)    
    title2 = '{} CURRENT DIRECTION(degree)({},{}) \nfrom {} to {}'.format(target_name, target_lon,target_lat,start_t, end_t)    

    ax1 = plt.subplot(3,1,1)
    plt.plot(vs)
    plt.title(title1)
    plt.grid()
    ax1.set_ylabel('SPEED(m/s)')
    ax1.set_xticks(range(0,buf,1))
    

    ax2 = plt.subplot(3,1,2)
    ax2.set_ylabel('DIRECTION(degree)')
    # plt.subplot(3,1,2)
    plt.plot(ds)
    # plt.title(title2)
    plt.grid()

    ax2.set_yticks(range(0,360,100))
    ax2.set_xticks(range(0,buf,1))

    ax3 = plt.subplot(3,1,3)
    ax3.set_ylim(0,0.5)
    ax3.set_xticks(range(0,buf,1))
    
    m = np.sqrt(np.power(us, 2) + np.power(vs, 2))
    
    fig = plt.quiver(xs, ys, us ,vs, m, scale=10)
    cb  = plt.colorbar(fig , orientation='horizontal')
    fig.set_clim(vmin=0, vmax=2)
    plt.grid()
    
    plt.show()

def check_array_value():
    lost_array = 0
    init_t   =  datetime.datetime(2000, 1,  1,  0, 0)
    start_t  =  datetime.datetime(2022, 7,  9, 0, 0) + datetime.timedelta(hours=0)
    end_t    =  start_t                              + datetime.timedelta(hours=24)

    # end_id = 48
    # start_id = 24

    lat = rootgrp2.variables['lat']
    lon = rootgrp2.variables['lon']

    for i in range(1, 120):
        #print(i)
        u = rootgrp2.variables['water_u'][i][0]
        v = rootgrp2.variables['water_v'][i][0]    

        u_all_zeros = not np.any(u)
        v_all_zeros = not np.any(v)
        
        time = init_t + datetime.timedelta(hours=rootgrp2.variables['time'][:][i])
        
        if u_all_zeros or v_all_zeros == 1:
            lost_array += 1
            # print(i, time)
    print("LOST:{}/120".format(lost_array))

def plot_all():   
    lat = rootgrp2.variables['lat']
    lon = rootgrp2.variables['lon']


    for i in range(1, 120):
        #print(i)
        u = rootgrp2.variables['water_u'][i][0]
        v = rootgrp2.variables['water_v'][i][0]

        m = np.sqrt(np.power(u, 2) + np.power(v, 2))


        x,y = np.meshgrid(lon, lat)

        # print(u)
        

        
        plt.figure(i)
        fig = plt.quiver(x, y, u ,v, m ,scale = 30)
        # plt.xlim(119, 123)
        # plt.xlim(120.425-0.01, 120.425+0.01)
        # plt.ylim(21 , 26)
        # plt.ylim(24.175-.001 , 24.175+.001)
        plt.grid()
        cb = plt.colorbar(fig)
        
    # plt.show()


def write_nc():
    ncfile  = Dataset(r'C:\Users\USER\Desktop\new.nc',mode='w',format='NETCDF4_CLASSIC') 
    lat_dim = ncfile.createDimension('lat', 73)     # latitude axis
    lon_dim = ncfile.createDimension('lon', 144)    # longitude axis
    time_dim = ncfile.createDimension('time', None) # unlimited axis (can be appended to).
    
    for dim in ncfile.dimensions.items():
        print(dim)


    lat = ncfile.createVariable('lat', np.double, ('lat',))
    lat.units = 'lat'
    lat.long_name = 'latitude'
    
    lon = ncfile.createVariable('lon', np.double, ('lon',))
    lon.units = 'lon'
    lon.long_name = 'longitude'
    
    time = ncfile.createVariable('time', np.double, ('time',))
    time.units = 'hours since 1800-01-01'
    time.long_name = 'time'
    
    # Define a 3D variable to hold the data
    water_u = ncfile.createVariable('water_u',np.double,('time','lat','lon')) # note: unlimited dimension is leftmost
    water_u.units = 'm/s' # degrees Kelvin
    water_u.standard_name = 'U' # this is a CF standard name
    
    water_v = ncfile.createVariable('water_v',np.double,('time','lat','lon')) # note: unlimited dimension is leftmost
    water_v.units = 'm/s' # degrees Kelvin
    water_v.standard_name = 'V' # this is a CF standard name
    

def main():
    print_info()
    # write_nc()
    # plot_singe_point()
    # plot_all()
    check_array_value()
main()