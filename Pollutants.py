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
    time = data[i][19]
    longitude = data[i][3]
    latitude = data[i][4]
    value = data[i][21]
    unit = data[i][23]
    pollutant = data[i][29]
    if len(time) !=0 and len(longitude) !=0 and len(latitude) !=0 and len(value) !=0 and unit == 'ug/kg'  and pollutant in ['As','Cd','Pb','total_Hg','Zn']:
        k+=1
        ltime.append(data[i][19])
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
"""
We can shrink the data to our location 0-8° longitude and 51-60° latitude and our time frame of 2015-2016.
"""
sortdata=[]
for i in range(len(ltime)):
    tempo = []
    if ltime[i][0:4] == '2015' or ltime[i][0:4] == '2016':
        #print('time OK')
        tempo.append(ltime[i])
    if 0<float(llongitude[i])<8:
        #print('long OK')
        tempo.append(llongitude[i])
    if 51<float(llatitude[i])<60:
        #print('lat OK')
        tempo.append(llatitude[i])
    tempo.append(lpollutant[i])
    tempo.append(lvalue[i])
    tempo.append(lunit[i])
    tempo.append(ldanger[i])
    if len(tempo) == 7:
        sortdata.append(tempo)
#print(len(sortdata))

"""
sortdata is a list of list containing all the datapoints for the selected pollutants, the chosen location and time frame and the danger index of the given concentration.
Exportation of the resulting dataset:

fulldata=[['time','longitude','latitude','pollutant','value','unit','risk']]
for i in range(len(sortdata)):
    fulldata.append(sortdata[i])
print(fulldata)

for i in range(len(fulldata)):
    with open('%s/Sorted_pollutant_data_2015-2016_North_Sea.csv' %path, 'a') as output:
        output.write(';'.join(fulldata[i]) + '\n')
"""

"""
Note from discussion about the script of Thomas:
There are less time points than total datapoints because several measurements the same day of different components at different location.
For the following steps, we can use the 'groupby' and the 'mean' functions from the pandas package. 
The groupby function can make the unique set of time, latitude, longitude, polutant, etc.
So we get an average per location and day of the pollutant value. This gives a 300 datapoints final dataset
"""
