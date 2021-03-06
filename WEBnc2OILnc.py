import os, subprocess, shutil, datetime
from pathlib import Path

def mergeBYday(day):
    # day  = '20211229'
    U    = r'/home1/cwecA/OPENDAP/{}/UCURR.{}00.nc.nc4'          .format(day, day)
    V    = r'/home1/cwecA/OPENDAP/{}/VCURR.{}00.nc.nc4'          .format(day, day)
    fn   = r'/home1/cwecA/OPENDAP/{}/temp{}.nc'                  .format(day, day)
    dump = r'/home1/cwecA/OPENDAP/{}/dump.nc'                    .format(day, day)
    out  = r'/home1/cwecA/OPENDAP/{}/OCMweb{}.nc'                .format(day, day)
     
    mon  = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC/{}'.format(day[0:6])
    nas  = r'/mnt/CWEC2NAS/External_IN/CWB/OCM/NC/{}/OCMweb{}.nc'.format(day[0:6], day)


    # MonthFolder = Path(mon)
    # Path.mkdir(MonthFolder, parents=True, exist_ok=True)

    if os.path.isfile(U) and os.path.isfile(U):
        # print(U, V, fn)
        subprocess.run(["ncks", "-A", U, fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(["ncks", "-A", V, fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(['ncrename', '-h', '-O', '-v', 'UCURR', 'water_u', fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.run(['ncrename', '-h', '-O', '-v', 'VCURR', 'water_v', fn], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.call('{} {} {} {}'.format('ncdump', fn, '>', dump), shell=True)
        subprocess.run(['sed', '-i', "s/int time/double time/g", dump], stdout=subprocess.PIPE, universal_newlines=True)
        subprocess.call('{} {} {} {}'.format('ncgen', dump, "-o", out), shell=True)
        
        if os.path.isfile(out):
            if not os.path.isdir(mon):
                os.mkdir(mon)
        shutil.copy(out, nas)
        print('[Done] {}'.format(day))
        # if result.stderr != None:
            # print(result.stdout)
            # print(result.stderr)
    else:
        print('File not exist.')

for i in range(1,6):
    today     = datetime.datetime.today()
    nextday  = today + datetime.timedelta(days=1)
    mergeBYday(nextday.strftime("%Y%m%d"))
    
# ncdump /home1/cwecA/OPENDAP/20211229/OCNweb20211229.nc > /home1/cwecA/OPENDAP/20211229/nc.dump    
