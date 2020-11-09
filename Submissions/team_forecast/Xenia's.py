# %%
# Some the necessary tools
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import datetime
import json
import urllib.request as req
import urllib
import fiona
import contextily as ctx
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from yellowbrick.regressor import ResidualsPlot
from yellowbrick.features import Rank2D

# %%
# NOTE examples of how to put regression equations on the plots:
plt.text(65, 230, 'y={:.2f}+{:.2f}*x'.format(male_fit[1], male_fit[0]), color='darkblue', size=12)
plt.text(70, 130, 'y={:.2f}+{:.2f}*x'.format(female_fit[1], female_fit[0]), color='deeppink', size=12)
line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'

# %%
# Function for Mesowest Temperature & Precipitation data


def prec_temp_data(end_date):

    """ Obtaining Precipitation and Air Temperature from the Mesowest website.


    Parameters
    ----------
    end_date : updated date, to obtain the latest values.

    Returns
    ------
    data_Meso : dataframe with precipitation and temperature per hour
    data_Meso_D : dataframe with the means of precipitation and temperature \
                  per day
    data_Meso_W : dataframe with the means of precipitation and temperature \
                  per week

    """

    # This is the base url that will be the start our final url
    base_url = "http://api.mesowest.net/v2/stations/timeseries"

    # Specific arguments for the data that we want
    args = {
            'start': '199701010000',
            'end': end_date,
            'obtimezone': 'UTC',
            'vars': 'air_temp,precip_accum',
            'stids': 'QVDA3',
            'units': 'temp|C,precip|mm',
            'token': 'demotoken'}

    # Takes your arguments and paste them together into a string for the api
    apiString = urllib.parse.urlencode(args)

    # add the API string to the base_url
    fullUrl = base_url + '?' + apiString
    print('The Mesowest data is obtained from: ', fullUrl)

    # Request the data
    response = req.urlopen(fullUrl)

    # What we need to do now is read this data. The complete format of this:
    responseDict = json.loads(response.read())

    # Create a dictionary. Keys shows the main elements of it.
    responseDict.keys()

    # Get the data we want:
    dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
    airT = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']
    precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_set_1']

    # Creating the pandas dataframe
    data_Meso = pd.DataFrame({'Temperature': airT, 'Precipitation': precip},
                             index=pd.to_datetime(dateTime))
    data_Meso_D = data_Meso.resample('D').mean().round(2)
    data_Meso_W = data_Meso.resample('W-SUN').mean().round(2)

    return data_Meso, data_Meso_D, data_Meso_W


# %%
end_date = '202011070000'
# Calling the function to get Precipitation and Temperature data from Mesowest
data_Meso, data_Meso_D, data_Meso_W = prec_temp_data(end_date)
# Printing my dataframe to know it
data_Meso_D

# %%
# New Plots with Temperature & Precipitation

fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='Streamflow', color='black', linewidth=1)
ax.plot(data_Meso_W['Precipitation'], 'r:', label='Precipitation',
        color='aqua', linestyle='-', alpha=1, linewidth=2)
ax.plot(data_Meso_W['Temperature'], 'r:', label='Temperature', color='red',
        linestyle='-', alpha=1, linewidth=1)
ax.set(title="2018-2021 data", xlabel="Date", ylabel="Weekly Avg values",
       yscale='log', xlim=[datetime.date(2018, 8, 24),
                           datetime.date(2021, 1, 15)])
ax.legend()
fig.set_size_inches(7, 5)
fig.savefig("2018-2021_Data.png")

# %%
# NOTE Review this: Calling x_data & y_data from function to plot them
x_data = AR_model_estimate(daily_flow, start_train_date,
                           end_train_date, time_shifts)
y_data = AR_model_estimate(daily_flow, start_train_date,
                           end_train_date, time_shifts)

# %%
# NOTE review x_data & y_data. Scatter plot of t vs t-1 flow with normal axes
fig, ax = plt.subplots()
ax.scatter(x_data, y_data, marker='.',
           color='purple', label='observations')
ax.set(title="Autoregression Model", xlabel='flow t-1', ylabel='flow t',
       xlim=[0, 175], ylim=[0, 175])
ax.plot(np.sort(x_data), np.sort(y_data), label='AR model',
        color='aqua', linewidth=3)
ax.legend()

# Xenia: Saving my plots
fig.set_size_inches(7, 5)
fig.savefig("Autoregression_Model.png")

# %%
# %%
# Residuals Plot (Trying new things)

# The residuals plot shows how the model is injecting error, the bold \
# horizontal line at residuals = 0 is no error, and any point above or below \
# that line, indicates the magnitude of error.
# (https://www.scikit-yb.org/en/latest/quickstart.html#installation)

# %%
# Adding timezone = UTC to the flow data, to join the Mesowest data after
daily_flow.index = daily_flow.index.tz_localize(tz="UTC")

# Merge the USGS data (flow) with the Mesowest data (precip. and temp.)
union = daily_flow['flow'].join(data_Meso_D[['Precipitation'], ['Temperature']])

# Rank2D Pearson Correlation
visualizer = Rank2D(algorithm="pearson")
visualizer.fit_transform(union)
visualizer.show()

# %%
# NOTE still working on this too. Correlation Matrix
corr_matrix = np.corrcoef(union).round(decimals=5)
fig, ax = plt.subplots()
im = ax.imshow(corr_matrix)
im.set_clim(-1, 1)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1, 2), ticklabels=('Precipitation', 'flow', 'Temperature'))
ax.yaxis.set(ticks=(0, 1, 2), ticklabels=('Precipitation', 'flow', 'Temperature'))
ax.set_ylim(2.5, -2.5)
for i in range(3):
    for j in range(3):
        ax.text(j, i, corr_matrix[i, j], ha='center', va='center',
                color='r')
cbar = ax.figure.colorbar(im, ax=ax, format='% .2f')
plt.show()

# Xenia: Saving my plots
plt.show()
fig.set_size_inches(7, 5)
plt.savefig("3._Correlation_Plot.png")
fig.savefig("3._Correlation_Plot.png")

# %%
