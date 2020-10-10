# Forecasting code for Week 7

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
#note you may need to do pip install for sklearn

#%% Functions

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
        shift_list=['flow']

        # Create additional columns to the dataframe to include desired time shifts
        for i in range(1,time_shifts+1):
                num_shift = 'flow_tm'+str(i)
                df[num_shift]=df['flow'].shift(i)
                shift_list.append(num_shift)

        # Create a dataframe of training data including all columns of df
        train_data = df[initial_train_date:final_train_date][shift_list]

        # Create the dependent array for the AR model
        y_data=train_data['flow']

        # Create the set of independent variables for the AR Model.
        x_data=train_data[shift_list[1:len(shift_list)]]

        # Fit the corresponding AR Model
        model_LR.fit(x_data,y_data)

        # Save the results of the AR Model
        r_sq = np.round(model_LR.score(x_data, y_data),4)
        model_intercept=np.round(model_LR.intercept_, 2)
        model_coefficients=np.round(model_LR.coef_,2)

        # Print the results to the user
        print('AR Model with ',time_shifts,' shifts')
        print('coefficient of determination:', r_sq)
        print('intercept:', model_intercept)
        print('slope:',model_coefficients )

        return model_intercept, model_coefficients, r_sq

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week7.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# %%
# Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()

# %%
# Forecasts for Week 7

# Define the time shifts parameter
time_shifts=3

# Estimate the parameters for the best-fit AR Model
model_intercept,model_coefficients, r_sq=AR_model_estimate(flow_weekly,\
         '2019-08-25','2019-11-17',time_shifts)

# Select the measured flow during a test period of time
test=flow_weekly.loc['2019-08-25':'2020-10-31']['flow']

# Create an array of zeros to save the flow data from Aug. 25/2019 to date
forecasts=np.zeros(test.shape[0]+2)

# Save flow values between Aug. 21/2020 to date
forecasts[0:test.shape[0]]=test.values

# Calculate the Forecasts for Week 1 and Week 2

if time_shifts == 1:
        for i in range(test.shape[0],test.shape[0]+2):
                forecasts[i]=model_intercept + \
                        model_coefficients[0]* forecasts[i-1]
elif time_shifts == 2:
        for i in range(test.shape[0],test.shape[0]+2):
                forecasts[i]=model_intercept + \
                         model_coefficients[0]* forecasts[i-1] \
                        + model_coefficients[1]* forecasts[i-2]
elif time_shifts == 3:
        for i in range(test.shape[0],test.shape[0]+2):
                forecasts[i]=model_intercept + \
                         model_coefficients[0]* forecasts[i-1] \
                          + model_coefficients[1]* forecasts[i-2]+\
                                model_coefficients[2]*forecasts[i-3]
elif time_shifts == 4:
        for i in range(test.shape[0],test.shape[0]+2):
                forecasts[i]=model_intercept + \
                                model_coefficients[0]* forecasts[i-1] \
                                + model_coefficients[1]* forecasts[i-2]+\
                                model_coefficients[2]*forecasts[i-3]+\
                                model_coefficients[3]*forecasts[i-4]
else:
        print('Please modify the code to include more time shifts')

# Print the forecasts for the competition
print('Dear Classmate, please submit these values to my CSV (The ones generated by AR Model):')
print('Week # 1 (cfs): ',np.round(forecasts[forecasts.shape[0]-2],2))
print('Week # 2 (cfs): ',np.round(forecasts[forecasts.shape[0]-1],2))

# %%
# Plot the results
# Time series of flow values with the x axis range limited
fig, ax = plt.subplots()

# Define x-axis for both arrays
x1=np.linspace(1,forecasts.shape[0]-3,forecasts.shape[0]-3)
x2=np.linspace(forecasts.shape[0]-2,forecasts.shape[0]-1,2)

# Plot both time series (Historical and Forecasted)
ax.plot(x1,forecasts[0:forecasts.shape[0]-3], label='Historical Data')
ax.plot(x2,forecasts[forecasts.shape[0]-2:forecasts.shape[0]], 'r:', label='Forecasted')
ax.set(title="Forecasted Flow", xlabel="Week", ylabel="Weekly Avg Flow [cfs]",
        yscale='log') # xlim=[datetime.date(2019, 8, 25), datetime.date(2020, 10, 31)])
ax.legend()

plt.show()


# %%
