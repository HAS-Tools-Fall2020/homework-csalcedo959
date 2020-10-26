# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import json 
import urllib.request as req
import urllib
from sklearn.linear_model import LinearRegression
from matplotlib.dates import DateFormatter

# %% Functions
""" Estimate the parameters of an Auto Regressive Model (AR)

Parameters:
----------
df: Dataframe containing the flow information.
initial_date: Initial date for the training period in format 'YYYY-MM-DD'.
final_date: Final date for the training period in format 'YYYY-MM-DD'.
time_shifts: Number of time shifts to consider in the AR model.

Returns:
---------
model_intercept: The intercept of the AR Model
model_coefficients: The coefficients of the AR Model (size=[time_shifts,1])
r_sq: Determination Coefficient R2 of the AR Model
"""


def AR_model_estimate(df, initial_train_date, final_train_date, time_shifts):

    # Define the type of model to use
    model_LR = LinearRegression()

    # Start the shift listing with the string 'Flow'
    shift_list = ['flow']

    # Create additional columns to the dataframe to include desired time \
    # shifts
    for i in range(1, time_shifts+1):
        num_shift = 'flow_tm'+str(i)
        df[num_shift] = df['flow'].shift(i)
        shift_list.append(num_shift)

    # Create a dataframe of training data including all columns of df
    train_data = df[initial_train_date:final_train_date][shift_list]

    # Create the dependent array for the AR model
    y_data = train_data['flow']

    # Create the set of independent variables for the AR Model.
    x_data = train_data[shift_list[1:len(shift_list)]]

    # Fit the corresponding AR Model
    model_LR.fit(x_data, y_data)

    # Save the results of the AR Model
    r_sq = np.round(model_LR.score(x_data, y_data), 4)
    model_intercept = np.round(model_LR.intercept_, 2)
    model_coefficients = np.round(model_LR.coef_, 2)

    # Print the results to the user
    print('AR Model with ', time_shifts, ' shifts')
    print('coefficient of determination:', r_sq)
    print('intercept:', model_intercept)
    print('slope:', model_coefficients)

    return model_intercept, model_coefficients, r_sq


""" Forecast the flows for a given number of periods based on flow timeseries

Parameters:
-----------
flow_daily: Dataframe containing the daily flow information. The index of \
        the df should be the date and this df should only include 'flow'.
time_shifts: Number of time shifts to consider in the AR Model
start_train_date: Initial date for the training period in format 'YYYY-MM-DD'.
end_train_date: Final date for the training period in format 'YYYY-MM-DD'.
start_for_date: Initial date for the forecast in format 'YYYY-MM-DD'.
end_for_date: Final date for the forecast in format 'YYYY-MM-DD'.
seasonal: Binary condition telling the scale of time of the forecast.

Returns:
-----------
flow_daily: Dataframe with the forecasts in a daily basis
flow_weekly: Dataframe with the forecasts in a weekly basis
model_intercept: Intercept from the AR Model
model_coefficients: List of coefficients from the AR Model
"""


def forecast_flows(flow_daily, time_shifts, start_train_date, end_train_date,
                   start_for_date, end_for_date, seasonal):

    # Get the location (index) for the day before the start forecasting \
    # date in the original dataframe (data)

    temp_data = flow_daily
    temp_data=temp_data.reset_index()
    temp_data['datetime'] = flow_daily.index#.strftime('%Y-%m-%d')

    if seasonal == 'week':
        date_before_start = (pd.to_datetime(start_for_date) +
                             dt.timedelta(days=-1)).date()
        index_lag1 = temp_data.loc[temp_data.datetime == str(date_before_start)].index[0]
    elif seasonal == 'seasonal':
        flow_daily = flow_daily.resample("W-SUN", closed='left', label='left')\
                .mean()
        index_lag1 = flow_daily.shape[0]-1
        print(index_lag1)
    else:
        print('Please choose a valid time horizon for forecast')

    # Create a list of dates (daily) for the forecast period
    if seasonal == 'week':
        forecast_period = pd.date_range(start=start_for_date,
                                        end=end_for_date, freq='D')
    elif seasonal == 'seasonal':
        forecast_period = pd.date_range(start=start_for_date,
                                        end=end_for_date, freq='W')

    # Estimate the parameters for the best-fit AR Model
    model_intercept, model_coefficients, r_sq = AR_model_estimate(
        flow_daily, start_train_date, end_train_date, time_shifts)

    # Calculate the Forecasts for the indicated time range based on the \
    # selected timeshifts.
    # "lag_i" is used to extract the flow value based on the order of the \
    # AR Model using the index located for the day before the start of \
    # forecast.
    lag_i = index_lag1+1

    # Using a nested conditional, the forecasts are calculated between \
    # the desired range of dates, and then appended to the dataframe

    if time_shifts == 1:
        for i in range(0, forecast_period.shape[0]):
            forecast_val = model_intercept + model_coefficients[0] * \
                            flow_daily.iloc[lag_i - 1]['flow']
            lag_i += 1  # Update the counter
            flow_daily.loc[forecast_period[i], ['flow']] = forecast_val
    elif time_shifts == 2:
        for i in range(0, forecast_period.shape[0]):
            forecast_val = model_intercept + model_coefficients[0] * \
                                flow_daily.iloc[lag_i - 1]['flow'] + \
                                model_coefficients[1] * \
                                flow_daily.iloc[lag_i - 2]['flow']
            lag_i += 1  # Update the counter
            flow_daily.loc[forecast_period[i], ['flow']] = forecast_val
    elif time_shifts == 3:
        for i in range(0, forecast_period.shape[0]):
            forecast_val = model_intercept + model_coefficients[0] * \
                                flow_daily.iloc[lag_i - 1]['flow'] + \
                                model_coefficients[1] * \
                                flow_daily.iloc[lag_i - 2]['flow'] + \
                                model_coefficients[2] * \
                                flow_daily.iloc[lag_i - 3]['flow']
            lag_i += 1  # Update the counter
            flow_daily.loc[forecast_period[i], ['flow']] = forecast_val
    elif time_shifts == 4:
        for i in range(0, forecast_period.shape[0]):
            forecast_val = model_intercept + model_coefficients[0] * \
                                flow_daily.iloc[lag_i - 1]['flow'] + \
                                model_coefficients[1] * \
                                flow_daily.iloc[lag_i - 2]['flow'] + \
                                model_coefficients[2] * \
                                flow_daily.iloc[lag_i - 3]['flow'] + \
                                model_coefficients[3] * \
                                flow_daily.iloc[lag_i - 4]['flow']
            lag_i += 1  # Update the counter
            flow_daily.loc[forecast_period[i], ['flow']] = forecast_val
    else:
        print('Please modify the code to include more time shifts')

    # Resampling the forecast in a weekly basis, starting on Sundays and \
    # setting the labels and closed interval at the left
    if seasonal == 'week':
        flow_weekly = flow_daily.loc[start_for_date:end_for_date][['flow']].\
            resample("W-SUN", closed='left', label='left').mean()
    elif seasonal == 'seasonal':
        flow_weekly = flow_daily.loc[start_for_date:end_for_date][['flow']]

    # Print the forecasts for the competition
    for i in range(flow_weekly.shape[0]):
        print('\n Week #', str(i+1), '-', flow_weekly.iloc[i].name, '(cfs): ',
              np.round(flow_weekly.iloc[i]['flow'], 2))

    return flow_daily, flow_weekly, model_intercept, model_coefficients

# %% 

# Data retrieval of streamflows from USGS

# URL Variables
site = '09506000'
start = '2009-03-02' # Adjusted according to information availability
end = '2020-10-24'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + site + \
      "&referred_module=sw&period=&begin_date=" + start + "&end_date=" + end

stream_data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                               'datetime', 'flow', 'code'],
                      parse_dates=['datetime'], index_col='datetime')

stream_data.index = stream_data.index.strftime('%Y-%m-%d')
stream_data=stream_data.set_index(pd.to_datetime(stream_data.index))


# %%
# Daily Temperature from Mesonet

# First Create the URL for the rest API
# Insert your token here
mytoken = '98bcecc0f3a4475d990a1596ab12e780'

# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want.. 
args = {
    'start': '199701010000',
    'end': '202010250000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'units': 'temp|F',
    'stids': 'KSEZ',
    'token': mytoken}

# Takes your arguments and paste them together
# into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
# this just gives us the API response... not very useful yet
response = req.urlopen(fullUrl)

# What we need to do now is read this data
# The complete format of this 
responseDict = json.loads(response.read())

# This creates a dictionary for you 
# The complete format of this dictonary is descibed here: 
# https://developers.synopticdata.com/mesonet/v2/getting-started/
#Keys shows you the main elements of your dictionary
responseDict.keys()
# You can inspect sub elements by looking up any of the keys in the dictionary
responseDict['UNITS']
#Each key in the dictionary can link to differnt data structures
#For example 'UNITS is another dictionary'
type(responseDict['UNITS'])
responseDict['UNITS'].keys()
responseDict['UNITS']['position']

#where as STATION is a list 
type(responseDict['STATION'])
# If we grab the first element of the list that is a dictionary
type(responseDict['STATION'][0])
# And these are its keys
responseDict['STATION'][0].keys()

# Long story short we can get to the data we want like this: 
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
airTemp = responseDict['STATION'][0]['OBSERVATIONS']['air_temp_set_1']

# Now we can combine this into a pandas dataframe
data_temp = pd.DataFrame({'Temperature': airTemp}, index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
daily_temp = data_temp.resample('D').max()
daily_temp =daily_temp.reset_index()
daily_temp =daily_temp.set_index([stream_data.index])

# %%
# Daily Relative Humidity from Mesonet

# First Create the URL for the rest API
# Insert your token here
mytoken = '98bcecc0f3a4475d990a1596ab12e780'

# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want.
args = {
    'start': '199701010000',
    'end': '202010250000',
    'obtimezone': 'UTC',
    'vars': 'relative_humidity',
    'stids': 'KSEZ',
    'token': mytoken}

# Takes your arguments and paste them together
# into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
# this just gives us the API response... not very useful yet
response = req.urlopen(fullUrl)

# What we need to do now is read this data
# The complete format of this 
responseDict = json.loads(response.read())

# This creates a dictionary for you 
# The complete format of this dictonary is descibed here: 
# https://developers.synopticdata.com/mesonet/v2/getting-started/
#Keys shows you the main elements of your dictionary
responseDict.keys()
# You can inspect sub elements by looking up any of the keys in the dictionary
responseDict['UNITS']
#Each key in the dictionary can link to differnt data structures
#For example 'UNITS is another dictionary'
type(responseDict['UNITS'])
responseDict['UNITS'].keys()
responseDict['UNITS']['position']

#where as STATION is a list 
type(responseDict['STATION'])
# If we grab the first element of the list that is a dictionary
type(responseDict['STATION'][0])
# And these are its keys
responseDict['STATION'][0].keys()

# Long story short we can get to the data we want like this: 
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
relative_humidity = responseDict['STATION'][0]['OBSERVATIONS']['relative_humidity_set_1']

# Now we can combine this into a pandas dataframe
data_r_hum = pd.DataFrame({'Relative Humidity': relative_humidity}, index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
daily_r_hum = data_r_hum.resample('D').max()

daily_r_hum = daily_r_hum.reset_index()
daily_r_hum= daily_r_hum.set_index([stream_data.index])


# %%
# Concatenate a single dataframe with all the time series
daily_data =pd.concat([stream_data[['flow']], daily_temp[['Temperature']], daily_r_hum[['Relative Humidity']]], axis=1)
daily_data=daily_data.set_index(pd.to_datetime(stream_data.index))

# %%
# Analyze the correlation between selected timeseries

# Calculate the correlation between timeseries

corr_temp = daily_data['flow'].corr(daily_data['Temperature'])
print('Correlation with Temperature:', corr_temp)

# Plot the correlation between timeseries
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
ax[0].scatter(stream_data['flow'],daily_temp['Temperature'], color='green', marker='*')
ax[0].set_xlim([0,5000])
ax[0].set_title('Correlation between Streamflow \n and Temperature at Verde River')
ax[0].set_xlabel('Daily streamflow [cfs]')
ax[0].set_ylabel('Temperature (°F)')

corr_rel_hum = daily_data['flow'].corr(daily_data['Relative Humidity'])
print('Correlation with Relative Humidity:', corr_rel_hum)

ax[1].scatter(stream_data['flow'], daily_r_hum['Relative Humidity'],color='orange', marker='o')
ax[1].set_xlim([0,5000])
ax[1].set_title('Correlation between Streamflow \n and Temperature at Verde River')
ax[1].set_xlabel('Daily streamflow [cfs]')
ax[1].set_ylabel('Daily Relative Humidity [%]')
plt.show()
fig.savefig('corr_plots.png')

#%% 
# Plot of the timeseries

fig, ay = plt.subplots()
ay.plot(daily_data['2015-01-01':'2020-10-24'].index, daily_data.loc['2015-01-01':'2020-10-24']['flow'], color='blue', label='Stream flow')
ay.set_title('Streamflow at Verde River - Source: USGS')
ay.set_xlabel('Date')
ay.set_ylabel('Flow [cfs]')
fig.savefig('streamflow.png')

fig, ax = plt.subplots()
ax.plot(daily_data['2015-01-01':'2020-10-24'].index, daily_data.loc['2015-01-01':'2020-10-24']['Temperature'], color='green', label='Temperature')
ax.set_title('Temperature near Verde River - Source: Sedona Airport (Mesonet)')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature [°F]')
fig.savefig('temperature.png')

fig, az = plt.subplots()
az.plot(daily_data['2015-01-01':'2020-10-24'].index, daily_data.loc['2015-01-01':'2020-10-24']['Relative Humidity'], color='red', label='Relative Humidity')
az.set_title('Relative Humidity near Verde River - Source: Sedona Airport (Mesonet)')
az.set_xlabel('Date')
az.set_ylabel('Relative Humidity [%]')
plt.show()
fig.savefig('rel_humidity.png')

# %%
# Forecasts for Week 9

# Common dataframe for both forecasts including only the flow column
daily_flow = stream_data[['flow']]
daily_flow=daily_flow.set_index(pd.to_datetime(stream_data.index))

# Two-week forecast

# Training period for the AR Model
start_train_date = '2019-08-25'
end_train_date = '2019-11-17'

# Forecasting period
start_for_date = '2020-10-25'
end_for_date = '2020-11-07'

# Used parameters for the model
# Number of shifts
time_shifts = 3

# Function Call
flow_daily_2w, flow_weekly_2w, model_intercept, model_coefficients = \
        forecast_flows(daily_flow, time_shifts, start_train_date,
                       end_train_date, start_for_date, end_for_date, 'week')

# Seasonal Forecast

# Training period for the AR Model for first 6 weeks
start_train_date = '2019-08-25'
end_train_date = '2019-11-10'

# Forecasting period for first 6 weeks
start_for_date = '2020-08-22'
end_for_date = '2020-12-12'

# Number of shifts
time_shifts = 3

# Common dataframe for both forecasts including only the flow column
daily_flow_16w = stream_data.loc['1989-01-01':start_for_date][['flow']]

# Function Call
flow_daily_seas, flow_weekly_seas, model_intercept16, model_coefficients16 = \
    forecast_flows(daily_flow_16w, time_shifts, start_train_date,
                   end_train_date, start_for_date, end_for_date, 'seasonal')
# %%
