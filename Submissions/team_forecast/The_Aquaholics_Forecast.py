# Team Forecast: The Aquaholics
# Members: Diana, Danielle, Xenia and Camilo
# November 2020

# %%
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import json
import urllib.request as req
import urllib
import teamfns as tf
from sklearn.linear_model import LinearRegression
from matplotlib.dates import DateFormatter
import seaborn as sn

# %% Data retrieval of streamflows from USGS

# URL Variables
site = '09506000'
start = '2009-03-02'  # Adjusted according to information availability
end = '2020-11-06'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" +\
       site + "&referred_module=sw&period=&begin_date=" + start + "&end_date="\
       + end

stream_data = pd.read_table(url, skiprows=30,
                            names=['agency_cd', 'site_no',
                                   'datetime', 'flow', 'code'],
                            parse_dates=['datetime'], index_col='datetime')

stream_data.index = stream_data.index.strftime('%Y-%m-%d')
stream_data = stream_data.set_index(pd.to_datetime(stream_data.index))


# %%
# Forecasts for Week 10

# Common dataframe for both forecasts including only the flow column
daily_flow = stream_data[['flow']]
daily_flow = daily_flow.set_index(pd.to_datetime(stream_data.index))
weekly_flow_plot = stream_data[['flow']].resample('W-SUN').mean().round(2)

# Two-week forecast

# Training period for the AR Model
start_train_date = '2009-10-01'
end_train_date = '2009-11-30'

# Forecasting period
start_for_date = '2020-11-01'
end_for_date = '2020-11-14'

# Used parameters for the model
# Number of shifts
time_shifts = 3

# Function Call
flow_daily_2w, flow_weekly_2w, model_intercept, model_coefficients = \
    tf.forecast_flows(daily_flow, time_shifts, start_train_date,
                      end_train_date, start_for_date, end_for_date, 'week')

# %%
# Seasonal Forecast for weeks between Aug. 22 to Oct. 31

# Training period for the AR Model for first 6 weeks
start_train_date = '2019-08-25'
end_train_date = '2019-11-10'

# Forecasting period for first 6 weeks
start_for_date = '2020-08-22'
end_for_date = '2020-10-31'

# Number of shifts
time_shifts = 3

# Common dataframe for both forecasts including only the flow column
daily_flow_16w = stream_data.loc['1989-01-01':start_for_date][['flow']]

# Function Call
flow_daily_seas, flow_weekly_seas, model_intercept16, model_coefficients16 = \
    tf.forecast_flows(daily_flow_16w, time_shifts, start_train_date,
                      end_train_date, start_for_date, end_for_date, 'seasonal')

# %%
# Seasonal Forecast for weeks between Nov. 01 to Dec. 12
# NOTE: I did not use the outputs printed by the model to make the forecasts.\
# Rather, I used the model determined by the function.

# Training period for the AR Model for first 6 weeks
start_train_date = '2009-10-01'
end_train_date = '2009-11-30'

# Forecasting period for first 6 weeks
start_for_date = '2020-11-01'
end_for_date = '2020-12-12'

# Number of shifts
time_shifts = 3

# Common dataframe for both forecasts including only the flow column
daily_flow_16w = flow_daily_seas.loc['1989-01-01':start_for_date][['flow']]

# Function Call
flow_daily_seas, flow_weekly_seas, model_intercept16, model_coefficients16 = \
    tf.forecast_flows(daily_flow_16w, time_shifts, start_train_date,
                      end_train_date, start_for_date, end_for_date, 'seasonal')

# %%
# Making PLOTS with Mesowest and USGS Data
end_date = '202011070000'

# Calling the function to get Precipitation and Temperature data from Mesowest
data_Meso, data_Meso_D, data_Meso_W = tf.prec_temp_data(end_date)

# Printing my dataframe to know it
data_Meso_D

# %%
# Plots with Temperature & Precipitation
fig, ax = plt.subplots()
ax.plot(weekly_flow_plot['flow'], label='Streamflow', color='black',
        linewidth=0.5)
ax.plot(data_Meso_W['Precipitation'], 'r:', label='Precipitation',
        color='aqua', linestyle='-', alpha=1, linewidth=0.7)
ax.plot(data_Meso_W['Temperature'], 'r:', label='Temperature',
        color='mediumorchid', linestyle='-', alpha=1, linewidth=0.5)
ax.set(title="Data", xlabel="Date", ylabel="Weekly Avg values",
       yscale='log')

ax.legend()
fig.set_size_inches(7, 5)
fig.savefig("Data.png")

# %%
# Adding timezone = UTC to the flow data, to join the Mesowest data after
daily_flow.index = daily_flow.index.tz_localize(tz="UTC")
weekly_flow_plot.index = weekly_flow_plot.index.tz_localize(tz="UTC")

# Concatenate a single dataframe with all the time series
union = pd.concat([weekly_flow_plot[['flow']], data_Meso_W[['Temperature']],
                   data_Meso_W[['Precipitation']]], axis=1)

# %%
# Correlation Plot
corrMatrix = union.corr()
sn.heatmap(corrMatrix, annot=True, vmin=-1, vmax=1, center=0, cmap='PRGn')
plt.title("Correlation_Matrix")
plt.show()
fig.set_size_inches(7, 5)
plt.savefig("Correlation_MAtrix.png")

# %%
