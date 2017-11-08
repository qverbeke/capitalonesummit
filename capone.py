import pandas as pd
import numpy as np
import geoplotlib as gpl
from geoplotlib.utils import read_csv, DataAccessObject, BoundingBox


"""
def show_geoplot
Description: generates and displays a map of the density of airbnb locations
Inputs: results: the Pandas Series object containing valid latitudes and longitudes
		mbc: the maximum bounds of the latitude and longitude of the data set
"""
def show_geoplot(results, mbc):
	data=DataAccessObject.from_dataframe(results[["lat","lon"]])
	gpl.hist(data, colorscale='sqrt', binsize=4)
	gpl.kde(data, bw=5, cut_below=1e-3)
	gpl.set_bbox(BoundingBox(mbc[0],mbc[1],mbc[2],mbc[3]))
	gpl.show()
def estimate_price(lat, lon, results, mbc):
	step=((mbc[0]-mbc[2])+(mbc[1]-mbc[3]))/2 #the average of the latitude and longitude span, will be used in the price estimation formula
	five_percent=get_coords_within_radius(results, step/20, lat, lon)


def get_coords_within_radius(results, radius, lat, lon):
	price_list=[]
	for i in results[["lat","lon","price"]]:
		if ((i["lat"]-lat)**2+(i["lon"]-lon)**2<radius):
			 temp=i["price"]

	if len(price_list) is not 0:
		pass
	else:
		return -1
results = pd.read_csv("airbnb-sep-2017/listings.csv")
results[["lat","lon"]]=results[["lat","lon"]].apply(pd.to_numeric, errors='coerce')
results_filter= (results["lat"] != np.nan)&(results["lon"] != np.nan)&(results["lat"]>30)&(results["lon"]>-130)&(results["lat"]<50)&(results["lon"]<-110)
results_filtered=results[results_filter]
max_bound_coords=(results_filtered["lat"].max(), results_filtered["lon"].max(),results_filtered["lat"].min(),results_filtered["lon"].min())
show_geoplot(results_filtered, max_bound_coords)
#estimate_price(37.8, -122.4,results_filtered, max_bound_coords)
