# Forecast Analysis for Week 15
# Developed by Camilo Salcedo for HAS Tools

# %%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import ar_functions as arf

# %% Data Retrieval for Stremflow (USGS)

# URL Variables
site = '09506000'
start = '1989-01-01'  # Adjusted according to information availability
end = '2020-12-05'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
    site + "&referred_module=sw&period=&begin_date=" + start + "&end_date=" +\
    end

stream_data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                                     'datetime', 'flow',
                                                     'code'],
                            parse_dates=['datetime'], index_col='datetime')

stream_data.index = stream_data.index.strftime('%Y-%m-%d')
stream_data = stream_data.set_index(pd.to_datetime(stream_data.index))

# %% Forecasts for Week 14

# Common dataframe for both forecasts including only the flow column
daily_flow = stream_data[['flow']]
daily_flow = daily_flow.set_index(pd.to_datetime(stream_data.index))

# Two-week forecast

# Training period for the AR Model
start_train_date = '2017-11-01'
end_train_date = '2017-12-12'

# Forecasting period
start_for_date = '2020-12-06'
end_for_date = '2020-12-19'

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
start_train_date = '2017-08-25'  # '2017-08-25'
end_train_date = '2017-11-17'  # '2017-11-10'

# Forecasting period for first 6 weeks
start_for_date = '2020-08-22'
end_for_date = '2020-10-31'

# Number of shifts
time_shifts = 3

# Common dataframe for both forecasts including only the flow column
daily_flow_16w_1 = stream_data.loc['1989-01-01':start_for_date][['flow']]

# Function Call
flow_daily_seas1, flow_weekly_seas1, model_intercept16_1, \
    model_coefficients16_1 = arf.forecast_flows(daily_flow_16w_1, time_shifts,
                                                start_train_date, end_train_date, start_for_date, end_for_date,
                                                'seasonal')

# %%
# Seasonal Forecast for weeks between Nov. 01 to Dec. 12
# NOTE: I did not use the outputs printed by the model to make the forecasts.\
# Rather, I used the model determined by the function.

# Training period for the AR Model for first 6 weeks
start_train_date = '2017-10-01'
end_train_date = '2017-12-15'

# Forecasting period for first 6 weeks
start_for_date = '2020-11-01'
end_for_date = '2020-12-12'

# Number of shifts
time_shifts = 3

# Common dataframe for both forecasts including only the flow column
daily_flow_16w_2 = flow_daily_seas1.loc['1989-01-01':start_for_date][['flow']]

# Function Call
flow_daily_seas2, flow_weekly_seas2, model_intercept16_2, model_coefficients16_2 = \
    arf.forecast_flows(daily_flow_16w_2, time_shifts, start_train_date,
                       end_train_date, start_for_date, end_for_date, 'seasonal')

# %% Plotting Weekly Performance

# Plot the Weekly Forecasts against the observed values
week_obs = stream_data.loc['2020-08-23':'2020-12-05'][['flow']].\
    resample("W-SUN", closed='left', label='left').mean()
weekly_for = [60, 192.61, 218.38, 56.39, 66.34, 94.16, 70,
              75.57, 88.98, 129.29, 139.39, 165.12, 158.23, 176.37, 167.58]

fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(week_obs['flow'], color='darkblue', linewidth=2, ls=':',
        marker='o', label='Observed')
ax.plot(week_obs.index, weekly_for, color='cyan', linewidth=2,
        marker='*', label='1 Week Forecast')
ax.set_ylabel('Average Daily Flow [cfs]', fontweight='bold')
ax.set_xlabel('Date', fontweight='bold')
ax.set_ylim([25, 175])
ax.set_title('Comparison between Weekly Forecast and Observed Flow \n',
             fontweight='bold')
ax.legend()
fig.savefig('weekly.png')

# %% Plotting Seasonal Performance

# Plot the Seasonal Forecasts against the observed values
week_obs = stream_data.loc['2020-08-23':'2020-12-05'][['flow']].\
    resample("W-SUN",  closed='left', label='left').mean()
seasonal_for = flow_weekly_seas1.append(flow_weekly_seas2)

fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(week_obs['flow'], color='darkblue', linewidth=2, ls=':',
        marker='o', label='Observed')
ax.plot(seasonal_for.loc['2020-08-23':'2020-12-05']['flow'], color='green', linewidth=2,
        marker='*', label='Forecasted')
ax.set_ylabel('Average Daily Flow [cfs]', fontweight='bold')
ax.set_xlabel('Date', fontweight='bold')
ax.set_ylim([25, 175])
ax.set_title('Comparison between Seasonal Forecast and Observed Flow \n',
             fontweight='bold')
ax.legend()
fig.savefig('seasonal.png')

# %%
