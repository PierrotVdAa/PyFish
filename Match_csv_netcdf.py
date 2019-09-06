"""
Created by Evgeny Ivanov for Emodnet Hackatlon 2019
"""

from netCDF4 import Dataset
import csv
import numpy as np
from datetime import date, datetime, timedelta
lo3 = lambda x: datetime(2014,1,1,0,0,0) + timedelta(seconds=x)
from scipy import spatial

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin();
	return array[idx]

t,lt,ln = [],[],[]
with open('datapoints.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		try:
			tt = row[0].split(',')[0]
			t.append(datetime.strptime(tt, '%Y-%m-%d'))
			lt.append(float(row[0].split(',')[1])/100)
			ln.append(float(row[0].split(',')[2])/100)
			print(t[-1],lt[-1],ln[-1])
			if t[-1].year == 2016:
				break
		except:
			pass	

rr = Dataset('MetO-NWS-BIO-dm-PHYT_1567692273372.nc', 'r', format='NETCDF4') # Huon (112,81) Hvom (111,82)
v=np.mean(rr.variables['PhytoC'][0,0],axis=0)

lon3 = rr.variables['lon'][:]
lat3 = rr.variables['lat'][:]
tt3 = rr.variables['time'][:]
t3 = []
for i in range(len(tt3)):
	t3.append(lo3(int(tt3[i])-12*3600))


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

c = []
f= open("Phyto.txt","w")
for i in range(len(t)):
	for j in range(len(t3)):
		if (t[i]-t3[j]).days == 0:
			# j is our time index
			mm = find_nearest(lat3, lt[i])
			nn = find_nearest(lon3, ln[i])
	
			m = int(np.where(lat3==mm)[0][0])
			n = int(np.where(lon3==nn)[0][0])
			c.append(np.mean(rr.variables['PhytoC'][j,:,m,n],axis=0))
			f.write("%s\n" % (c[-1]))
			print(i,j)
f.close()

f= open("Phyto2.txt","w")
for i in range(len(t)):
	f.write("%s\t%s\t%s\t%s\n" % (t[i],lt[i],ln[i],c[i]))
f.close()
