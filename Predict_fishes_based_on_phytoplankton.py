"""
Created by Evgeny Ivanov for Emodnet Hackatlon 2019
"""

import os
from owslib.wcs import WebCoverageService
from osgeo import gdal
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import AxesGrid
import cmocean as cm
from netCDF4 import Dataset

import requests
import xml.dom.minidom
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

mintemp=0; maxtemp=130; division=1
clevs = np.arange(mintemp,maxtemp,division)
cmap = cm.cm.deep

def bcz_bound():
	"""
	returns coordinates of BCZ
	as arrays of latitudes and longitudes
	"""
	yz=np.array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361])
	xz=np.array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
	return xz,yz

def grid_instance(llcrnrlon=0.0, urcrnrlon=5.0, llcrnrlat=49.0, urcrnrlat=54.0, lat_ts=51.5, r='i', discr=0.5, caxx='horizontal'):
	"""
	plot the grid instance in the Mercator projection
	arguments: llcrnrlon - the western point (defualt 0.0); urcrnrlon - the eastern point (defualt 5.0);
	llcrnrlat - the southern point (defualt 49.0); urcrnrlat - the northern point (defualt 54.0);
	lat_ts - the central latitude (defualt 51.5); r - resolution (default - 'i');
	discr - discretisation in drawn parallels and meridians (default - 0.5);
	"""
	#fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
	m1 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution=r, ax=ax)
	#m1.drawparallels(np.arange(llcrnrlat,urcrnrlat,discr),labels=[1,0,0,1],fontsize=10)
	#m1.drawmeridians(np.arange(llcrnrlon,urcrnrlon,discr),labels=[1,1,1,0],fontsize=10)
	m1.drawcoastlines()
	#m1.drawmapboundary(fill_color='aqua') # uncomment if quiver + contourf
	m1.drawcountries()
	#m1.fillcontinents(color='#ddaa66',lake_color='#9999FF') # uncomment if quiver + contourf
	if caxx=='horizontal':
		cax = make_axes_locatable(ax).append_axes("bottom", size=0.4, pad=0.15)
	elif caxx=='vertical':
		cax = make_axes_locatable(ax).append_axes("right", size=0.4, pad=0.15)
	else:
		pass
	return fig, ax, cax, m1

#url = "https://ows.emodnet-humanactivities.eu/wcs?" 
url = "https://ows.emodnet-bathymetry.eu/wcs?"
#url = "http://ows.catalog.emodnet-physics.eu/geonetwork/srv/eng/csw?"
wcs = WebCoverageService(url, version='1.0.0', timeout = 320)
print(wcs.identification.type)

clipfile =  r'temp.tif'
requestbbox = (0,55,5,60)
layer = 'emodnet:mean'
#layer = 'emodnet:2017_st_00_avg'
# get the data
#bathyml = 'emodnet:2017_st_00_avg'
bathyml = 'emodnet:mean'
sed = wcs[layer] # this is necesaary to get essential metadata from the advertised layer
print(sed.keywords)

cx,cy = map(int,sed.grid.highlimits)
bbox = sed.boundingboxes[0]['bbox']
lx,ly,hx,hy = map(float,bbox)
resx,resy = (hx-lx)/cx,(hy-ly)/cy
width = cx/1000
height = cy/1000

gc = wcs.getCoverage(identifier=bathyml, bbox = requestbbox, coverage=sed, format='GeoTIFF', crs=sed.boundingboxes[0]['nativeSrs'],resx=resx,resy=resy)

# write to a file
fn = clipfile
f = open(fn,'wb')
f.write(gc.read())
f.close()

ds = gdal.Open(clipfile)

# get the dimentions of column and row
nc   = ds.RasterXSize
nr   = ds.RasterYSize

# read elevation data
bathy = ds.ReadAsArray()

# only get positive depth values
bathy[bathy < 0] = 0

# get Longitude and Latitude info
geotransform = ds.GetGeoTransform()
xOrigin      = geotransform[0]
yOrigin      = geotransform[3]
pixelWidth   = geotransform[1]
pixelHeight  = geotransform[5]

# enerate Longitude and Latitude array
lons = xOrigin + np.arange(0, nc)*pixelWidth
lats = yOrigin + np.arange(0, nr)*pixelHeight

fig, ax, cax, m1 = grid_instance(llcrnrlon=0, urcrnrlon=5, llcrnrlat=51, urcrnrlat=55, lat_ts=51, r='l', discr=0.25, caxx='vertical')
xz,yz = bcz_bound()
x, y = m1(xz, yz)
m1.plot(x,y,color='black',linewidth=1.0)
lons,lats = np.meshgrid(lons,lats)
x1, y1 = m1(lons, lats)

norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp)
bounds=np.arange(mintemp,maxtemp+division,division)
cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')
cbar.ax.invert_yaxis() 

#bathy[bathy<3]=np.nan
bathy[bathy>maxtemp]=maxtemp
CS1 = m1.contourf(x1,y1,bathy,clevs,cmap=cmap)


"""
plane2 = np.array(Image.open('/home/evgeny/Hackatlon/fish4.png'))
im2 = OffsetImage(plane2, zoom=0.1)
x2, y2 = m1(2.9, 51.5)
ab2 = AnnotationBbox(im2, (x2,y2), xycoords='data', frameon=False)
m1._check_ax().add_artist(ab2)

plane3 = np.array(Image.open('/home/evgeny/Hackatlon/ship.png'))
im3 = OffsetImage(plane3, zoom=0.1)
x3, y3 = m1(2.6, 51.2)
ab3 = AnnotationBbox(im3, (x3,y3), xycoords='data', frameon=False)
m1._check_ax().add_artist(ab3)"""
# Get the axes object from the basemap and add the AnnotationBbox artist

"""m1.plot(list([x3,x2]),list([y3,y2]), marker=None,color='m',linewidth=3)"""

"""rr = Dataset('/home/evgeny/Hackatlon/MetO-NWS-WAV-hi_1567684700871.nc', 'r', format='NETCDF4') # Huon (112,81) Hvom (111,82)
h=rr.variables['VHM0'][0]
h[h>1.3] = 0
h[h>0] = -1
h[h==0] = 1

lon2 = rr.variables['longitude'][:]
lat2 = rr.variables['latitude'][:]
lon2,lat2 = np.meshgrid(lon2,lat2)
ln2,lt2 = m1(lon2, lat2)
m1.contourf(ln2,lt2,h,clevs,cmap=mpl.cm.Reds,vmin=0.99,vmax=1.0,alpha=0.95)
rr.close()
"""
rr = Dataset('/home/evgeny/Hackatlon/MetO-NWS-BIO-dm-PHYT_1567692273372.nc', 'r', format='NETCDF4') # Huon (112,81) Hvom (111,82)
v=np.mean(rr.variables['PhytoC'][0],axis=0)

lon3 = rr.variables['lon'][:]
lat3 = rr.variables['lat'][:]
lon3,lat3 = np.meshgrid(lon3,lat3)
ln3,lt3 = m1(lon3, lat3)
#m1.contourf(ln3,lt3,v,clevs,cmap=mpl.cm.rainbow) #,alpha=0.5)




for i in range(2,len(v)-2):
	for j in range(2,len(v.T)-2):
		if v[i,j] == np.max(v[i-1:i+2,j-1:j+2]) and type(v[i,j])==np.float64 and v[i,j]>1:
			print(i,j,v[i,j])
			plane1 = np.array(Image.open('/home/evgeny/Hackatlon/fish3.png'))
			im1 = OffsetImage(plane1, zoom=0.15*v[i,j]*1/50)
			x0, y0 = m1(lon3[i,j], lat3[i,j])
			ab1 = AnnotationBbox(im1, (x0,y0), xycoords='data', frameon=False)
			m1._check_ax().add_artist(ab1)
plt.show()
