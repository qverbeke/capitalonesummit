import pandas as pd
import numpy as np
import geoplotlib as gpl
from geoplotlib.utils import read_csv, DataAccessObject, BoundingBox
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

"""
def show_geoplot
Description: generates and displays a map of the density of airbnb locations
Inputs: results: the Pandas Series object containing valid latitudes and longitudes
	mbc: the maximum bounds of the latitude and longitude of the data set
Outputs: a display of the input data in a heat map
"""
def show_geoplot(results, mbc):
	data=DataAccessObject.from_dataframe(results[["lat","lon"]])
	gpl.hist(data, colorscale='sqrt', binsize=4)
	gpl.kde(data, bw=5, cut_below=1e-3)
	gpl.set_bbox(BoundingBox(mbc[0],mbc[1],mbc[2],mbc[3]))
	gpl.show()

"""
def estimate_price
Description: gets the suggested price by latitude and longitude by taking an initial radius and weighting it the most, then
	taking incrementally larger radii and giving them less and less weight as the radius increases.
	Radius is based on the total size of san francisco bookings, as indicated by the outer bounds of the points
Inputs: lat: the latitude query. lon: the longitude query. 
	results: the Pandas Series object containing valid latitudes, longitudes, and prices
	mbc: the maximum bounding coordinates of the latitude and longitude of the data set
Outputs: the estimate for an airbnb booking at the given location
"""
def estimate_price(lat, lon, results, mbc):
	radius=((mbc[0]-mbc[2])+(mbc[1]-mbc[3]))/128 
	avg_price=0
	count=0
	for i in range(len(results["lon"])):
		try:
			results["price"][i]
		except:
			continue
		price =results["price"][i][1:]
		try:
			temp=price.index(",")
			price=float(price[:temp]+price[temp+1:])
		except ValueError:
			price=float(price)		
		if ((results["lat"][i]-lat)**2+(results["lon"][i]-lon)**2<radius):
			avg_price+=price
			count+=1
		elif ((results["lat"][i]-lat)**2+(results["lon"][i]-lon)**2<radius*2):
			avg_price+=price*0.5
			count+=0.5
		elif ((results["lat"][i]-lat)**2+(results["lon"][i]-lon)**2<radius*4):
			avg_price+=price*0.25
			count+=0.25
		elif ((results["lat"][i]-lat)**2+(results["lon"][i]-lon)**2<radius*8):
			avg_price+=price*0.125
			count+=0.125
	if count!=0:			
		return avg_price/count
	else:
		return "Invalid coordinates"
"""
def create_price_by_neighbourhood_roomtype
Description: This function takes a result set and creates multiple graphs representing data about the price
	as it is related to both neighbourhood and the type of room being offered
Input: results: the entire result set from the listings csv file
Output: three graphs
	first: neighbourhood vs price for airbnbs
	second: top ten neighbourhoods by price divided into the price of each room type
	third: lowest ten neighbourhoods by price divided into the price of each room type
"""
def create_price_by_neighbourhood_roomtype(results):
	neighbourhoods_list=[]
	neighbourhoods_count=[]
	for i in results["neighbourhood"]:
		try:
			neighbourhoods_count[neighbourhoods_list.index(i)]+=1
		except ValueError:
			neighbourhoods_list.append(i)
			neighbourhoods_count.append(1)
	i=0
	while i < len(neighbourhoods_list):
		if neighbourhoods_count[i]<30:
			neighbourhoods_count.pop(i)
			neighbourhoods_list.pop(i)
		else:
			i+=1
	temp=neighbourhoods_list.index(np.nan)
	neighbourhoods_list.pop(temp)
	neighbourhoods_count.pop(temp)
	price_list=[]
	for i in neighbourhoods_list:
		results_filter=(results["neighbourhood"]==i)
		results_filtered=results[results_filter]
		avg_price=0.0
		count=0
		for i in results_filtered["price"]:
			try:
				try:
					i=i[1:]
					temp=i.index(",")
					i=i[:temp]+i[temp+1]
				except ValueError:
					pass
				i=float(i)
				avg_price+=i
				count+=1
			except TypeError:
				continue
		price_list.append(avg_price/count)

	for i in range(1,len(price_list)):
		j=i-1
		while j>=0 and price_list[j+1]<price_list[j]:
			price_list[j],price_list[j+1]=price_list[j+1],price_list[j]
			neighbourhoods_list[j],neighbourhoods_list[j+1]=neighbourhoods_list[j+1],neighbourhoods_list[j]
			j-=1
	display_neighbourhoods_by_price(neighbourhoods_list, price_list)
		
	room_types=("Private room", "Entire home/apt", "Shared room")
	prices=[[],[],[]]	
	for i in range(30):
		filter_room_type=(results["neighbourhood"]==neighbourhoods_list[len(neighbourhoods_list)-i//3-1])&(results["room_type"]==room_types[i%3])
		room_types_filtered=results[filter_room_type]
		avg_price=0.0
		count=0
		for j in room_types_filtered["price"]:
			try:
				try:
					j=j[1:]
					temp=j.index(",")
					j=j[:temp]+j[temp+1]
				except ValueError:
					pass
				j=float(j)
				avg_price+=j
				count+=1
			except TypeError:
				continue
		if count !=0:
			prices[i%3].append(avg_price/count)
		else:
			prices[i%3].append(1)
	display_neighbourhoods_by_room_price(prices, neighbourhoods_list[len(neighbourhoods_list)-11:])
	
	prices=[[],[],[]]

	for i in range(30):
		filter_room_type=(results["neighbourhood"]==neighbourhoods_list[i//3])&(results["room_type"]==room_types[i%3])
		room_types_filtered=results[filter_room_type]
		avg_price=0.0
		count=0
		for j in room_types_filtered["price"]:
			try:
				try:
					j=j[1:]
					temp=j.index(",")
					j=j[:temp]+j[temp+1]
				except ValueError:
					pass
				j=float(j)
				avg_price+=j
				count+=1
			except TypeError:
				continue
		if count !=0:
			prices[i%3].append(avg_price/count)
		else:
			prices[i%3].append(1)	
	display_neighbourhoods_by_room_price(prices, neighbourhoods_list[:10])
"""
def display_neighbourhoods_by_price
Description: create a matplotlib graphical display of all neighbourhoods sorted in order of decreasing average price
Inputs: neighbourhoods_list: a list of all the neighbourhoods in san francisco
	price_list: a list of all prices corresponding to neighbourhoods 
Outputs: A bar chart representing the average prices of airbnbs in different neighbourhoods
"""
def display_neighbourhoods_by_price(neighbourhoods_list, price_list):
	font = {'size':8}
	mpl.rc('font', **font)
	y_pos = np.arange(len(neighbourhoods_list))
	plt.barh(y_pos, price_list, align='center', alpha=0.5)
	plt.yticks(y_pos, neighbourhoods_list)
	font = {'size':16}
	mpl.rc('font', **font)
	plt.xlabel('Price')
	plt.title('Price vs Neighbourhood')
	plt.show()	
"""
def display_neighbourhoods_by_price
Description: create a matplotlib graphical display of ten neighbourhoods. Each neighbourhood has data about the
	prices of the three different possible room types
Inputs: neighbourhoods_list: a list of all the neighbourhoods in san francisco
	prices: a 2D list of room types corresponding to prices which correspond to neighbourhoods 
Outputs: A bar chart representing the average prices of airbnbs in different neighbourhoods. Each
	neighbourhood has data about each of the three room types
"""
def display_neighbourhoods_by_room_price(prices, neighbourhoods):
	n_groups = 10
	private = prices[0]
	home = prices[1]
	shared=prices[2]
	font = {'size':10}
	mpl.rc('font', **font) 
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.3
	rects1 = plt.barh(index, shared, bar_width,
					 alpha=0.5,
					 color='b',
					 label='Shared Room')
	 
	rects2 = plt.barh(index + bar_width, private, bar_width,
					 alpha=0.5,
					 color='c',
					 label='Private Room')
	rects3 = plt.barh(index + 2*bar_width, home, bar_width,
					 alpha=0.6,
					 color='g',
					 label='Entire home/apt')
	plt.xlabel('Price')
	plt.ylabel('Neighbourhood')
	plt.title('Average Price by Room Type and Neighbourhood')
	plt.yticks(index + 2*bar_width, neighbourhoods)
	plt.legend()
	plt.show()
"""
def main()
Description: the main function. Runs a test of all written functions.
	To run one specific function, simply read the function description and give valid input,
	or comment out all functions that you do not wish to run.
	Ex. If you wish to run estimate_price, simply pass a latitude, longitude, result set, and 
	maximum bounding coordinates to the function
"""
def main():
	results = pd.read_csv("airbnb-sep-2017/listings.csv")
	results[["lat","lon"]]=results[["lat","lon"]].apply(pd.to_numeric, errors='coerce')
	results_filter= (results["lat"] != np.nan)&(results["lon"] != np.nan)&(results["lat"]>30)&(results["lon"]>-130)&(results["lat"]<50)&(results["lon"]<-110)
	results_filtered=results[results_filter]
	
	
	
	max_bound_coords=(results_filtered["lat"].max(), results_filtered["lon"].max(),results_filtered["lat"].min(),results_filtered["lon"].min())
	show_geoplot(results_filtered, max_bound_coords)
	create_price_by_neighbourhood_roomtype(pd.read_csv("airbnb-sep-2017/listings.csv"))
	print("Input a valid set of coordinates for San Francisco.\n"
		+"Valid latitude coordinates are between "+str(max_bound_coords[2])+" and "+str(max_bound_coords[0]))
	lat=float(input("Latitude: "))
	print("Valid longitude coordinates are between "+str(max_bound_coords[3])+" and "+str(max_bound_coords[1]))
	lon=float(input("Longitude: "))
	print("The approximate price of an airbnb at these coordinates is: $"+str(estimate_price(lat, lon, results_filtered, max_bound_coords)))

if __name__=="__main__":
	main()
