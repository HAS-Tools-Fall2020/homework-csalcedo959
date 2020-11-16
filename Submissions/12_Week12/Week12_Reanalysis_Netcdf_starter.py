# Forecast Analysis for Week 12
# Developed by Camilo Salcedo for HAS Tools

# %%
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset
import numpy as np
from matplotlib.dates import DateFormatter
import ar_functions as arf

# %% Information Gathering from CDF

# Net CDF file for historical precipitation rate (in Kg/m^2/s)
data_path_prec = os.path.join('./data', 'PrecipitationRate.nc')

# Net CDF file for historical Temperature (in K degrees)
data_path_temp = os.path.join('./data', 'temp_tropo.nc')

# Net CDF file for historical pressure (in Pascals)
data_path_press = os.path.join('./data', 'Pressure.nc')

# Read the data as an x-array
data_preci = xr.open_dataset(data_path_prec)
data_temp = xr.open_dataset(data_path_temp)
data_press = xr.open_dataset(data_path_press)

# Take a look of the datasets

data_preci
data_temp
data_press

# %%
# Get the latitude and longitude of each dataset to extract it

# Precipitation
lat_prec = data_preci.prate.lat.values[0]
lon_prec = data_preci.prate.lon.values[0]

# Temperature
lat_temp = data_temp.air.lat.values[0]
lon_temp = data_temp.air.lon.values[0]

# Pressure
lat_press = data_press.pres.lat.values[0]
lon_press = data_press.pres.lon.values[0]

# Extraction of values for each coordinate
loc_prec = data_preci.prate.sel(lat=lat_prec, lon=lon_prec)
loc_temp = data_temp.air.sel(lat=lat_temp, lon=lon_temp)
loc_press = data_press.pres.sel(lat=lat_press, lon=lon_press)

# Conversion of the datasets into dataframes

precip_df = loc_prec.to_dataframe()
temp_df = loc_temp.to_dataframe()
press_df = loc_press.to_dataframe()

# %% Data Retrieval for Stremflow (USGS)

# URL Variables
site = '09506000'
start = '2009-01-01'  # Adjusted according to information availability
end = '2020-11-15'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + site + \
      "&referred_module=sw&period=&begin_date=" + start + "&end_date=" + end

stream_data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                                     'datetime', 'flow', 'code'],
                            parse_dates=['datetime'], index_col='datetime')

stream_data.index = stream_data.index.strftime('%Y-%m-%d')
stream_data = stream_data.set_index(pd.to_datetime(stream_data.index))

# %%
# Plot the new dataframes
# Precipitation rate
fig, aa = plt.subplots()
aa.plot(precip_df['prate']['2017':'2020'],
        color='darkblue', linewidth=0.6, alpha=0.9, label='Precip. Rate')
aa.set_xlabel('Date', fontweight='bold')
aa.set_ylabel('Precipitation Rate [Kg/m^2/s]', fontweight='bold')
aa.set_title(
    'Daily Average Precipitation Rate Between 2017 and 2020 \n', fontweight='bold')
date_form = DateFormatter("%Y")
aa.legend(loc='lower left',
          bbox_to_anchor=(.5, -0.3), ncol=5)
a2 = aa.twinx()
a2.plot(stream_data.loc['2017':'2020'].index.values, stream_data['flow']['2017':'2020'],
        color='green', alpha=0.7, linewidth=0.2, label='Streamflow')
a2.xaxis.set_major_formatter(date_form)
a2.set_ylim([0, 300])
a2.set_ylabel('Average Daily Flow [cfs]', fontweight='bold')
a2.legend(loc='lower center',
          bbox_to_anchor=(.3, -0.3), ncol=5)
fig.savefig('precip_rate.png')

# Temperature at the Tropopause
fig, bb = plt.subplots()
bb.plot(temp_df['air']['2017':'2020'],
        color='darkorange', linewidth=0.6, alpha=0.9, label='Air Temperature')
bb.set_xlabel('Date', fontweight='bold')
bb.set_ylabel('Air Temperature [K°]', fontweight='bold')
bb.set_title(
    'Daily Air Temperature Between 2017 and 2020 \n', fontweight='bold')
date_form = DateFormatter("%Y")
bb.legend(loc='lower left',
          bbox_to_anchor=(.5, -0.3), ncol=5)
b2 = bb.twinx()
b2.plot(stream_data.loc['2017':'2020'].index.values, stream_data['flow']['2017':'2020'],
        color='green', alpha=0.7, linewidth=0.2, label='Streamflow')
b2.xaxis.set_major_formatter(date_form)
b2.set_ylim([0, 300])
b2.set_ylabel('Average Daily Flow [cfs]', fontweight='bold')
b2.legend(loc='lower center',
          bbox_to_anchor=(.3, -0.3), ncol=5)
fig.savefig('temperature.png')

# Pressure
fig, cc = plt.subplots()
cc.plot(press_df['pres']['2017':'2020'],
        color='deepskyblue', linewidth=0.6, alpha=0.9, label='Pressure')
cc.set_xlabel('Date', fontweight='bold')
cc.set_ylabel('Pressure [Pa]', fontweight='bold')
cc.set_title(
    'Daily Pressure Between 2017 and 2020 \n', fontweight='bold')
date_form = DateFormatter("%Y")
cc.legend(loc='lower left',
          bbox_to_anchor=(.5, -0.3), ncol=5)
c2 = cc.twinx()
c2.plot(stream_data.loc['2017':'2020'].index.values, stream_data['flow']['2017':'2020'],
        color='green', alpha=0.7, linewidth=0.2, label='Streamflow')
c2.xaxis.set_major_formatter(date_form)
c2.set_ylim([0, 300])
c2.set_ylabel('Average Daily Flow [cfs]', fontweight='bold')
c2.legend(loc='lower center',
          bbox_to_anchor=(.3, -0.3), ncol=5)
fig.savefig('pressure.png')


# %%
# Perform a correlation analysis to determine which time series is more \
# similar to streamflow

# Correlation analysis between Streamflow and Precipitation Rate
corr_precip_rate = stream_data['flow']['2009-01-01':
                                       '2020-11-01'].corr(precip_df['prate']['2009-01-01':
                                                                             '2020-11-01'])
print('Correlation with Precipitation Rate:', corr_precip_rate)

# Plot the correlation
fig, ax = plt.subplots()
ax.scatter(stream_data['flow']['2009-01-01':'2020-11-01'], precip_df['prate']['2009-01-01':
                                                                              '2020-11-01'],
           color='blue', marker='*')
ax.set_xlim([0, 5000])
ax.set_title(
    'Correlation between Streamflow \n and Precipitation Rate at Verde River')
ax.set_xlabel('Daily streamflow [cfs]')
ax.set_ylabel('Precipitation Rate [Kg/m^2/s]')

# Correlation analysis between Streamflow and Temperature
corr_temp = stream_data['flow']['2009-01-01':
                                '2020-11-01'].corr(temp_df['air']['2009-01-01':
                                                                  '2020-11-01'])
print('Correlation with Temperature:', corr_temp)

# Plot the correlation
fig, ay = plt.subplots()
ay.scatter(stream_data['flow']['2009-01-01':'2020-11-01'], temp_df['air']['2009-01-01':
                                                                          '2020-11-01'],
           color='red', marker='o')
ay.set_xlim([0, 5000])
ay.set_title(
    'Correlation between Streamflow \n and Temperature at Verde River')
ay.set_xlabel('Daily streamflow [cfs]')
ay.set_ylabel('Temperature [K°]')

# Correlation analysis between Streamflow and Pressure
corr_press = stream_data['flow']['2009-01-01':'2020-11-01'].corr(
    press_df['pres']['2009-01-01':'2020-11-01'])
print('Correlation with Pressure:', corr_press)

# Plot the correlation
fig, az = plt.subplots()
az.scatter(stream_data['flow']['2009-01-01':'2020-11-01'], press_df['pres']['2009-01-01':
                                                                            '2020-11-01'],
           color='yellow', marker='o')
az.set_xlim([0, 5000])
az.set_title(
    'Correlation between Streamflow \n and Pressure at Verde River')
az.set_xlabel('Daily streamflow [cfs]')
az.set_ylabel('Pressure [Pa]')

# %% Forecasts for Week 12

# Common dataframe for both forecasts including only the flow column
daily_flow = stream_data[['flow']]
daily_flow = daily_flow.set_index(pd.to_datetime(stream_data.index))

# Two-week forecast

# Training period for the AR Model
start_train_date = '2019-08-25'
end_train_date = '2019-11-17'

# Forecasting period
start_for_date = '2020-11-15'
end_for_date = '2020-11-28'

# Used parameters for the model
# Number of shifts
time_shifts = 3

# Function Call
flow_daily_2w, flow_weekly_2w, model_intercept, model_coefficients = \
    arf.forecast_flows(daily_flow, time_shifts, start_train_date,
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
