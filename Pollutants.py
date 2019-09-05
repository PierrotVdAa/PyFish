"""
Pollution in North Sea seafood
date: 05/09/2019
author: Pierrot Van der Aa

Analyse the type of pollutant at a given time in the area 51-60° latitude and 0-8° longitude
"""

path = 'D:/Documents/Google Drive Cloud/Marine Hackathon'
dataraw = open('%s/North_biota_unrestricted_transposed_flitered_2010_2017.csv' %path,'r')

"""
firstNlines=dataraw.readlines()[0:5]
print(firstNlines)
"""

data=[]
for elem in dataraw:
    m = elem.split(',')
    data.append(m)
#print(data[0])
title_time = (data[0][2]) #yyyy-mm-ddThh:mm:ss.sss
title_longitude = (data[0][3]) #Longitude [degrees_east]
title_latitude = (data[0][4]) #Latitude [degrees_north]
title_value = (data[0][21]) #Value
title_unit = (data[0][23]) #Units
title_pollutant = (data[0][29]) #S27_altlabel

ltime,llongitude,llatitude,lvalue,lunit,lpollutant = [],[],[],[],[],[]
k = 0
for i in range(1,len(data)):
    time = data[i][2]
    longitude = data[i][3]
    latitude = data[i][4]
    value = data[i][21]
    unit = data[i][23]
    pollutant = data[i][29]
    if len(time) !=0 and len(longitude) !=0 and len(latitude) !=0 and len(value) !=0 and unit == 'ug/kg'  and pollutant in ['As','Cd','Pb','total_Hg','Zn']:
        k+=1
        ltime.append(data[i][2])
        llongitude.append(data[i][3])
        llatitude.append(data[i][4])
        lvalue.append(data[i][21])
        lunit.append(data[i][23])
        lpollutant.append(data[i][29])
#print(k)

"""
Now we want to create a new list with the answer to 'is this pollutant in toxic concentration?'
"""
#definition of the legal thresholds
lim_as = 100 #legal limit for As (Arsenic)
lim_cd = 50 #legal limit for Cd (Cadmium)
lim_pb = 300 #legal limit for Pb (Lead)
lim_hg = 1000 #legal limit for total_Hg (mercury)
lim_zn = 120000 #legal limit for Zn (Zinc)


d = 0
ldanger = []
for i in range(len(lpollutant)):
    if lpollutant[d] == 'As' and int(lvalue[d])>100:
        ldanger.append('danger')
    elif lpollutant[d] == 'Cd' and int(lvalue[d])>50:
        ldanger.append('danger')
    elif lpollutant[d] == 'Pb' and int(lvalue[d])>300:
        ldanger.append('danger')
    elif lpollutant[d] == 'total_Hg' and int(lvalue[d])>1000:
        ldanger.append('danger')
    elif lpollutant[d] == 'Zn' and int(lvalue[d])>120000:
        ldanger.append('danger')
    else: 
        ldanger.append('safe')
    d+=1
#print(d)
print(ldanger)

"""
Note from discussion about the script of Thomas:
There are less time points than total datapoints because several measurements the same day of different components at different location.
For the following steps, we can use the 'groupby' and the 'mean' functions from the pandas package. 
The groupby function can make the unique set of time, latitude, longitude, polutant, etc.
So we get an average per location and day of the pollutant value. This gives a 300 datapoints final dataset
"""
