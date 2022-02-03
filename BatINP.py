import datetime

def init() :
    global ship_name     
    global Year          
    global Month         
    global Day           
    global Hour          
    global Minute        
    global counter       
    global Scenario_name 
    global SpillTime1    
    global WRF           

    ship_name     = 'LIDIA'
    Year          = '2022'
    Month         = '1'
    Day           = '5'
    Hour          = '10'
    Minute        = '0'
    counter       = 181
    Scenario_name = '{}OCA-{}-{}{}-{}'.format(str(int(Year)-1911), ship_name, Month.zfill(2), Day.zfill(2) , str(counter))
    SpillTime1    = '{} {} {} {} {}'  .format(Year               , Month    , Day  , Hour, Minute)
    WRF           = 'test'
    
    # print(Scenario_name, SpillTime1)

def create_INP():
    k=  "[OILMAPW]                                        ,\
        Scenario={}                                       ,\
        Description=description                           ,\
        Spill Lon=116.730108333333                        ,\
        Spill Lat=20.72446                                ,\
        Release Duration=4                                ,\
        Amount Spilled=55000                              ,\
        Oil Units=1                                       ,\
        SIMAP Oil Database=0                              ,\
        Start Year={}                                     ,\
        Start Month={}                                    ,\
        Start Day={}                                      ,\
        Start Hour={}                                     ,\
        Start Minute=0                                    ,\
        Scenario TimeZone=8                               ,\
        Scenario TimeZone String=(GMT+08:00)              ,\
        Spill Sources=1                                   ,\
        Splon1=116.730108333333                           ,\
        Splat1=20.72446                                   ,\
        SpillTime1={}                                     ,\
        Duration1=4                                       ,\
        Amount1=55000                                     ,\
        OilUnit1=1                                        ,\
        RlsDepth1=0                                       ,\
        Use Poly Spill=0                                  ,\
        Poly Spill Vertices=0                             ,\
        Simulation Length=24                              ,\
        Time Units=0                                      ,\
        Number Of Wind Files=0                            ,\
        Windfile1={}                                      ,\
        Wnd1LON=0                                         ,\
        Wnd1LAT=0                                         ,\
        Wind TimeZone=0                                   ,\
        Wind TimeZone String=No Time Zone Selected        ,\
        Original Current File=                            ,\
        Current File=PI-400M-1060623.CIR                  ,\
        Current File2=                                    ,\
        Current Next=                                     ,\
        Current Components=255                            ,\
        GIR Components=                                   ,\
        High Tide=0                                       ,\
        High Tide Minute=0                                ,\
        Current TimeZone=0                                ,\
        Current TimeZone String=No Time Zone Selected     ,\
        VelocityScale=1                                   ,\
        tc_station=                                       ,\
        tc_region=0                                       ,\
        tc_index=0                                        ,\
        tc_lon=0                                          ,\
        tc_lat=0                                          ,\
        Second Current=                                   ,\
        Feg_VScale=0                                      ,\
        Velocity Output=0                                 ,\
        Velocity Output DBF=0                             ,\
        Grid File=TWCTBOUNDARY_V12_3.BDM                  ,\
        Ice File=_NO_DATA.ICE                             ,\
        Reed File=                                        ,\
        Oil Name=Diesel (2002)                            ,\
        Oil Database=0                                    ,\
        Oil Density=.831                                  ,\
        Oil Density Temp=15                               ,\
        Oil Viscosity=2.76                                ,\
        Oil Tension=27.5                                  ,\
        Oil MaxWater=0                                    ,\
        Oil MinThick=.01                                  ,\
        Oil FlashPt=-999999                               ,\
        Oil InitialBP=368.393                             ,\
        Oil Gradient=392.741                              ,\
        Oil EvapA=8.78                                    ,\
        Oil EvapB=12.25                                   ,\
        Air Temp=15                                       ,\
        Water Temp=20                                     ,\
        Ideltat=30                                        ,\
        out_intvl=30                                      ,\
        ddxy=10                                           ,\
        chezy_on=0                                        ,\
        vdiffus=999                                       ,\
        droplet_dmin=999                                  ,\
        droplet_dmax=999                                  ,\
        nsp_rls=300                                       ,\
        wspil_min=0                                       ,\
        DaysSpilletsLive=0                                ,\
        wndfactor=3.5                                     ,\
        wndangle=0                                        ,\
        C_spread=150                                      ,\
        thkmin=.0001                                      ,\
        c2_mousse=.000002                                 ,\
        wndfactor_medice=3.3                              ,\
        wndangle_medice=35                                ,\
        wndfactor_hvyice=0                                ,\
        wndangle_hvyice=0                                 ,\
        PackFactor=.5                                     ,\
        OilNanoMeter=0                                    ,\
        Make DBF=0                                        ,\
        Contours On=-1                                    ,\
        X Contour Cells=50                                ,\
        Y Contour Cells=50                                ,\
        Floating Contour Grid=-1                          ,\
        Gaussian Off=0                                    ,\
        clipThicknessContour=-1                           ,\
        polyContours On=0                                 ,\
        PolyOutputSec=0                                   ,\
        Make Probability Envelope=0                       ,\
        Wind Speed Variability=30                         ,\
        Wind Direction Variability=30                     ,\
        Current Speed Variability=30                      ,\
        Current Direction Variability=30                  ,\
        Slippery Shore=0                                  ,\
        Evaporation On=-1                                 ,\
        Entrainment On=-1                                 ,\
        Use Ice=0                                         ,\
        IceNoYear=0                                       ,\
        UseDryWet=0                                       ,\
        Matroos_bathy_file=                               ,\
        WaterDepthFile=                                   ,\
        Use Wind Forced Residual=0                        ,\
        Wind Averaging Hrs=0                              ,\
        Reference Wind Speed=0                            ,\
        AOI Window=0                                      ,\
        UserDefinedXMax=0                                 ,\
        UserDefinedYMax=0                                 ,\
        UserDefinedXMin=0                                 ,\
        UserDefinedYMin=0                                 ,\
        Entrainment=0                                     ,\
        Trajectory Mode=0                                 ,\
        Default Depth=0                                   ,\
        Extra Fates=0                                     ,\
        Water Density Up=0                                ,\
        Water Density Low=0                               ,\
        pycnocline=0                                      ,\
        CSS=0                                             ,\
        Salinity=0                                        ,\
        SS Settle Vel=0                                   ,\
        UseResponseCalculator=0                           ,\
        UseDispersant=0                                   ,\
        Use TC Stations=0                                 ,\
        TC Search Distance=2                              ,\
        Number TC Stations=0                              ,\
        optFixOrExpandGrid=0                              ,\
        GridArrayImaxs=100                                ,\
        GridArrayJmaxs=100                                ,\
        GridArrayKmaxs=5                                  ,\
        stocOptFixOrExpandGrid=0                          ,\
        StochArrayImaxs=0                                 ,\
        StochArrayJmaxs=0                                 ,\
        DBF Shore=0                                       ,\
        DBF shore name=                                   ,\
        DatumOffset=0                                     ,\
        ShorelineTypeFile=                                ,\
        Default Shore Type=Sand (narrow shore)            ,\
        Include Decay=0                                   ,\
        Default Winds=0                                   ,\
        Ice Removed=0                                     ,\
        WindDllErrMess=no error                           ,\
        CurrDllErrMess=no error                           ,\
        Subset Point Type 0=5                             ,\
        Subset Color 0=11370057                           ,\
        Subset Label 0=Surface                            ,\
        Subset Line Type 0=5                              ,\
        HorzAnnotation 0=0                                ,\
        Subset Point Type 1=11                            ,\
        Subset Color 1=8388736                            ,\
        Subset Label 1=Surface                            ,\
        Subset Line Type 1=5                              ,\
        HorzAnnotation 1=0                                ,\
        Subset Point Type 2=7                             ,\
        Subset Color 2=1052904                            ,\
        Subset Label 2=Surface                            ,\
        Subset Line Type 2=5                              ,\
        HorzAnnotation 2=0                                ,\
        Subset Point Type 3=9                             ,\
        Subset Color 3=3181821                            ,\
        Subset Label 3=Surface                            ,\
        Subset Line Type 3=5                              ,\
        Subset Point Type 4=2                             ,\
        Subset Color 4=11979025                           ,\
        Subset Label 4=Surface                            ,\
        Subset Line Type 4=5                              ,\
        Subset Point Type 5=10                            ,\
        Subset Color 5=378107                             ,\
        Subset Label 5=Surface                            ,\
        Subset Point Type 6=2                             ,\
        Subset Color 6=16777215                           ,\
        YaxisLabel=Thickness (m)                          ,\
        manualMinY=0                                      ,\
        manualMaxY=0                                      ,\
        manualScaleControlY=0                             ,\
        manualMinX=0                                      ,\
        manualScaleControlX=1                             ,\
        Graph MainTitle=Weathering/Fates for Diesel (2002),\
        Graph SubTitle=                                   ,\
        Graph Label Bold=True                             ,\
        Show Annotations=True                             ,\
        Allow Annotation Control=True                     ,\
        Allow Graph Zooming=1                             ,\
        Graph Gridline Control=1                          ,\
        Graph Font Size=1                                 ,\
        Graph Yaxis Scale=1                               ,\
        Graph Xaxis Scale=1                               ,\
        Scale For Ydata=0                                 ,\
        Scale For Xdata=0                                 ,\
        Graph Settings Overwrite=True                     ,".format(Scenario_name, str(int(Year)), str(int(Month)), str(int(Day)), Hour, SpillTime1, WRF)
    # Q = k.replace(' ', '').split(',')
    Q = ' '.join(k.split())
    Q = Q.split(',')

    with open(r'O:\loc_data\Taiwan\RUNDATA\{}.INP'.format(Scenario_name), 'w', encoding='utf8') as f:
        f.write('[OILMAPW]'+'\n')
        for i in Q[1:]:
            f.write(i[1:-1]+'\n')
            # print(i[1:])



init()
for i in range(1,2):
    today     = datetime.datetime.today()
    # today    += datetime.timedelta(days=1)
    today    += datetime.timedelta(days=i)
    s         = today.strftime("%Y%m%d")
    Month     = today.strftime("%m")
    Day       = today.strftime("%d")
    Hour      = '10'
    counter   = counter + 1
    Scenario_name = '{}OCA-{}-{}{}-{}'.format(str(int(Year)-1911), ship_name, Month.zfill(2), Day.zfill(2) , str(counter))
    SpillTime1    = '{} {} {} {} {}'  .format(Year               , Month    , Day  , Hour, Minute)
    print(Scenario_name, SpillTime1)

    create_INP()
    counter       = counter + 1    
    Hour          = '18'
    Scenario_name = '{}OCA-{}-{}{}-{}'.format(str(int(Year)-1911), ship_name, Month.zfill(2), Day.zfill(2) , str(counter))
    SpillTime1    = '{} {} {} {} {}'  .format(Year               , Month    , Day  , Hour, Minute)   
    

    create_INP()

    print(Scenario_name, SpillTime1)
