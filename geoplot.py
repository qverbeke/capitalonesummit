from geoplotlib.utils import read_csv, DataAccessObject, BoundingBox
import geoplotlib as gpl
import numpy as np
import pandas as pd
#def display_map
results = pd.read_csv("airbnb-sep-2017/listings.csv")
results[["lat","lon"]]=results[["lat","lon"]].apply(pd.to_numeric, errors='coerce')
results_filter= (results["lat"] != np.nan)&(results["lon"] != np.nan)&(results["lat"]>30)&(results["lon"]>-130)&(results["lat"]<50)&(results["lon"]<-110)
results_filtered=results[results_filter]
data=DataAccessObject.from_dataframe(results_filtered[["lat","lon"]])
gpl.hist(data, colorscale='sqrt', binsize=4)
gpl.kde(data, bw=3, cut_below=1e-2)
gpl.set_bbox(BoundingBox(37.5,-122.65,38,-122.25))
gpl.show()
