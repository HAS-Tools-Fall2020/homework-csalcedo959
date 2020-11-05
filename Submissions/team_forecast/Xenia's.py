# %%
# Some the necessary tools
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import fiona
import contextily as ctx
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from yellowbrick.datasets import load_concrete
from yellowbrick.regressor import ResidualsPlot

# %%
# Residuals Plot (Trying new things)

# The residuals plot shows how the model is injecting error, the bold \
# horizontal line at residuals = 0 is no error, and any point above or below \
# that line, indicates the magnitude of error.
# (https://www.scikit-yb.org/en/latest/quickstart.html#installation)

# Load a regression dataset
X, y = load_concrete()

# %%
# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

visualizer = ResidualsPlot(LinearRegression())
visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()                 # Finalize and render the figure

# Xenia: Saving my plots
plt.show()
fig.set_size_inches(7, 5)
plt.savefig("6._Residuals_Plot.png")
fig.savefig("6._Residuals_Plot.png")


# %%
# Gauges II USGS stream gauge dataset:
# Link used: https://water.usgs.gov/GIS/dsdl/gagesII_9322_point_shapefile.zip
# Reading it using geopandas
file = os.path.join('../data/gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# The variable "file" will automatically join the address of your shapefile.
print('The current work directory is:')
print(os.getcwd())
print()
print('The data is storaged at:')
print(file)
print()

# This shows if the path exists or not, to check if there is any problem
# finding the data. "True" means it's ok. "False" means there is a problem.
print('Is everything ok with the path to start working now?')
os.path.exists(file)

# %%
# Now lets make a map!
fig, ax = plt.subplots(figsize=(5, 5))
gages.plot(ax=ax)
plt.show()

# Zoom  in and just look at AZ
gages.columns
gages.STATE.unique()
gages_AZ = gages[gages['STATE'] == 'AZ']
gages_AZ.shape

# More advanced plot of AZ gages - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='OrRd',
              ax=ax)
ax.set_title("Arizona stream gauge drainge area\n (sq km)")
plt.show()

# %%
# Adding more datasets
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/\

# HUC means: Hydrologic Unit Code
# Reading in a geodataframe
# Watershed boundaries for the lower Colorado. Polygon layer.
file = os.path.join('../data/WBD_15_HU2_GDB', 'WBD_15_HU2_GDB.gdb')
os.path.exists(file)
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")

# Looking at the dataset
HUC6.head()

# plot the new layer we got:
fig, ax = plt.subplots(figsize=(5, 5))
HUC6.plot(ax=ax)
ax.set_title("HUC Boundaries")
plt.show()

# Showing the Coordinate Reference System
HUC6.crs

# %%
# Add some points
# UofA:  32.22877495, -110.97688412
# Verde River Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-110.97688412, 32.22877495],
                       [-111.7891667, 34.44833333]])

# make these into spatial features
point_geom = [Point(xy) for xy in point_list]
point_geom

# mape a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC6.crs)

# plot these on the first dataset
# Then we can plot just one layer at a time
fig, ax = plt.subplots(figsize=(5, 5))
HUC6.plot(ax=ax)
point_df.plot(ax=ax, color='red', marker='x', markersize=50)
ax.set_title("HUC Boundaries")
plt.show()

# %%
# Xenia
# From:https://www.epa.gov/eco-research/ecoregion-download-files-state-region-9

# Ecoregions of Arizona. Polygon layer.
file = os.path.join('../data/az_eco_l3', 'az_eco_l3.shp')
os.path.exists(file)
fiona.listlayers(file)
eco_AZ = gpd.read_file(file, layer="az_eco_l3")

# Looking at the dataset
eco_AZ.head()

# More advanced - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
eco_AZ.plot(column='NA_L2NAME', categorical=True, legend=True, cmap='YlGn',
            ax=ax)
ax.set_title("Ecoregions of Arizona")
plt.show()

# %%
# Xenia
# From: https://data.fs.usda.gov/geodata/edw/datasets.php?xmlKeyword=arizona

# Temperatures of Arizona. Point layer.
file = os.path.join('../data/S_USA.NorWeST_TemperaturePoints.gdb',
                    'S_USA.NorWeST_TemperaturePoints.gdb')
os.path.exists(file)
fiona.listlayers(file)
temp_AZ = gpd.read_file(file, layer="NorWeST_TemperaturePoints")

# Looking at the dataset
temp_AZ.head()

# More advanced - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
temp_AZ.plot(categorical=True, legend=True, cmap='RdYlBu', ax=ax)
ax.set_title("Temperatures of Arizona")
plt.show()

# %%
# Xenia
# From: http://repository.azgs.az.gov/category/thematic-keywords/geodatabase

# Wildfires of Arizona. Point layer.
file = os.path.join('../data/azwildfires_di44_v1.gdb_',
                    'AZWildfires_DI44_v1.gdb')
os.path.exists(file)
fiona.listlayers(file)
fires_AZ = gpd.read_file(file, layer="RainGages_AZFires")

# Looking at the dataset
fires_AZ.head()

# More advanced - color by attribute
fig, ax = plt.subplots(figsize=(5, 5))
fires_AZ.plot(categorical=True, legend=True, cmap='OrRd', ax=ax)
ax.set_title("Wildfires of Arizona")
plt.show()

# %%
# Changing all the layers to the same CRS as "Gages" layer.
points_project = point_df.to_crs(gages_AZ.crs)
eco_AZ_project = eco_AZ.to_crs(gages_AZ.crs)
temp_AZ_project = temp_AZ.to_crs(gages_AZ.crs)
fires_AZ_project = fires_AZ.to_crs(gages_AZ.crs)
HUC6_project = HUC6.to_crs(gages_AZ.crs)

# NOTE: .to_crs() will only work if your original spatial object has a CRS \
# assigned to it AND if that CRS is the correct CRS!

# %%
# Putting everything on the same plot:

# Now plot
# Adding each layer to the map
fig, ax = plt.subplots(figsize=(10, 5))
eco_AZ_project.plot(column='NA_L2NAME', categorical=True, legend=True,
                    label='Ecoregions', cmap='YlGn', ax=ax)
gages_AZ.plot(categorical=False, legend=True,
              label='Stream Gages', markersize=15, cmap='ocean', ax=ax)
temp_AZ_project.plot(categorical=False, legend=True, markersize=15, marker='>',
                     cmap='RdYlBu', ax=ax, label='Temperature')
fires_AZ_project.plot(categorical=False, legend=True, marker='^',
                      markersize=80, cmap='Reds', ax=ax, label='Wildfires')
points_project.plot(ax=ax, legend=True, label='Points of interest',
                    color='red', marker='x', markersize=80, linewidth=2)
HUC6_project.boundary.plot(ax=ax, color=None, edgecolor='black', linewidth=0.5)

# Making zoom to the bounds of the prefered layer. In this case Eco-regions.
xlim = ([eco_AZ_project.total_bounds[0],  eco_AZ_project.total_bounds[2]])
ylim = ([eco_AZ_project.total_bounds[1],  eco_AZ_project.total_bounds[3]])
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set(title='Flow Gages, Ecoregions, Temperature \n Arizona State',
       xlabel='Longitude', ylabel='Latitude')

# Show the legend
ax.legend()

# Show the plot
plt.show()

# %%
