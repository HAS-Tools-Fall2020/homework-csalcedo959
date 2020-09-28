# Example solution for HW 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

#filepath = '/../homework-csalcedo959/data/streamflow_week5.txt'

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%
# Sorry no more helpers past here this week, you are on your own now :) 
# Hints - you will need the functions: describe, info, groupby, sort, head and tail.

#FORECASTS

#Analyze the historical means of June, July and August to determine the more similar years to 2020

reportsMonth = pd.DataFrame(columns=['Year','Month', 'Mean','Stdv'])

for i in range(1989,2021):
        year_temp=data.loc[(data.year==i)]
        for j in range(7,10):
        #Gets the list of elements for each month
         month_temp=year_temp.loc[(year_temp.month==j)]
         mean_val=month_temp.mean()['flow']
         std_val=month_temp.std()['flow']
         reportsMonth=reportsMonth.append({'Year':i, 'Month':j,'Mean':mean_val, 'Stdv':std_val},ignore_index=True)
          
print('\n The lowest and highest flow values, with its corresponding year, are shown below:')
print(reportsMonth)

mJuly=reportsMonth.loc[(reportsMonth.Month)==7]
mAug=reportsMonth.loc[(reportsMonth.Month)==8]
mSept=reportsMonth.loc[(reportsMonth.Month)==9]
#July
fig,ax = plt.subplots()
plt.bar(mJuly['Year'], mJuly['Mean'])
ax.set_title('Annually Mean for July Daily Flows at Verde River')
ax.set_ylabel('Mean Daily Flow (cfs)')
ax.set_xlabel('Year')
plt.show()
#August
fig,ax = plt.subplots()
plt.bar(mAug['Year'], mAug['Mean'])
ax.set_title('Annually Mean for August Daily Flows at Verde River')
ax.set_ylabel('Mean Daily Flow (cfs)')
ax.set_xlabel('Year')
plt.show()
#September
fig,ax = plt.subplots()
plt.bar(mSept['Year'], mSept['Mean'])
ax.set_title('Annually Mean for September Daily Flows at Verde River')
ax.set_ylabel('Mean Daily Flow (cfs)')
ax.set_xlabel('Year')
plt.show()

# %%
#Forecasts Week 5

#To develop the short term forecasting, it was noticed that Sept 2010 and Sept 2019 had a similar flow in terms of their mean.

#Calculate a proportional factor between 2019/2010

flow092019 = data.loc[(data.year==2019)&(data.month==9)&(data.day<=26),['flow']].to_numpy()
flow092010 = data.loc[(data.year==2010)&(data.month==9)&(data.day<=26),['flow']].to_numpy()

prop_fact=flow092019/flow092010

#Get time series for 2020
flow092020=data.loc[(data.year==2020)&(data.month==9)&(data.day<=26),['flow']].to_numpy()

#Get difference between 2020 and 2019
fact_2020=flow092020/flow092019
final_fact=fact_2020/prop_fact

fact=np.min(final_fact)

data['forecast2020']=data['flow']*(1-fact) #(1-(fact-1)) 

#First week
w1=data.loc[(data.year==2019)&(data.month==9)&(data.day>=27)&(data.day<=30),['forecast2020']].mean()['forecast2020']
w1oct=data.loc[(data.year==2019)&(data.month==10)&(data.day<=3),['forecast2020']].mean()['forecast2020']
print('\n The forecast for week 1 is:', np.round((w1+w1oct)/2,decimals=2))

#Second Week
w2=data.loc[(data.year==2019)&(data.month==10)&(data.day>=4)&(data.day<=10),['forecast2020']].mean()['forecast2020']
print('\n The forecast for week 2 is:', np.round(w2,decimals=2))

#Seasonal Forecast

#August: Comparison between 2019 and 2002
#Calculate a proportional factor between 2019/2010

flow082019 = data.loc[(data.year==2019)&(data.month==8)&(data.day<=21),['flow']].to_numpy()
flow082002 = data.loc[(data.year==2002)&(data.month==8)&(data.day<=21),['flow']].to_numpy()

prop_fact=flow082019/flow082002

#Get time series for 2020
flow082020=data.loc[(data.year==2020)&(data.month==8)&(data.day<=21),['flow']].to_numpy()

#Get difference between 2020 and 2019
fact_2020=flow082020/flow082019
final_fact=fact_2020/prop_fact

fact=np.max(final_fact)

data['forecast2020long']=data['flow']*(fact-1) #(1-(fact-1)) 
#Determines the index for the first forecasting date
startf=data.loc[(data.year==2019)&(data.month==8)&(data.day==22)].index[0]
endf=data.loc[(data.year==2019)&(data.month==8)&(data.day==29)].index[0]
for i in range(0,14):
        week=data.iloc[startf+i*7:endf+i*7,9:10]
        print('\: Week:' , i+1, 'Forecast(lps): ',np.round(week.mean()[0], decimals=2))

#Determines the index for the first forecasting date
startf=data.loc[(data.year==2016)&(data.month==11)&(data.day==22)].index[0]
endf=data.loc[(data.year==2016)&(data.month==11)&(data.day==28)].index[0]
for i in range(1,3):
        week=data.iloc[startf+i*7:endf+i*7,9:10]
        print('\: Week:' , i+14, 'Forecast(lps): ',np.round(week.mean()[0], decimals=2))


# %% 
# Answer to Questions

# 1. Provide a summary of the data frames properties.

#Description of column "Year"
print('The column "Year" is composed as follows:',data['year'].describe())
#Description of column "Month"
print('\n The column "Month" is composed as follows:',data['month'].describe())
#Description of column "Day"
print('\n The column "Day" is composed as follows:',data['day'].describe())

#2. Provide a summary of the flow column including the min, mean, max, standard deviation and quartiles.

print('\n The summary of the column "Flow" is below:', data[['flow']].describe())

#3. Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)

#Creates the grouping information
monthly_flow=data.groupby(['month'])[['flow']].describe()
print('\n The summary of flow data grouped in a monthly basis is shown below:', monthly_flow)
#%%
#4. Provide a table with the 5 highest and 5 lowest flow values for the period of record. Include the date, month and flow values in your summary.

#Create a dataframe for sorted values
sorted_data=data.sort_values(by='flow', ascending=False)
#Print the top 5-highest flows and the data in which they occured
print('\n The top 5-highest flows are shown below:')
print(sorted_data[['year','month','day','flow']].head())
#Print the top 5-lowest flows and the data in which they occured
print('\n The top 5-lowest flows are shown below:')
print(sorted_data[['year','month','day','flow']].tail())

#%% 

#5. Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in.
#Create a dataframe to store the results
reports = pd.DataFrame(columns=['Month', 'Max','Year(max)','Min','Year(min)'])

for i in range(1,13):
        #Gets the list of elements for each month
        month_temp=data.loc[(data.month==i)]   
        sv=month_temp.sort_values(by='flow', ascending=False)   
        maxVal=sv.iloc[0:1,3:4].to_numpy()
        maxYear=sv.iloc[0:1,5:6].to_numpy()
        minVal=sv.iloc[sv.shape[0]-1:sv.shape[0],3:4].to_numpy()
        minYear=sv.iloc[sv.shape[0]-1:sv.shape[0],5:6].to_numpy()

        reports=reports.append({'Month':i,'Max':maxVal, 'Year(max)':maxYear,\
               'Min':minVal,'Year(min)':minYear},ignore_index=True)

              
print('\n The lowest and highest flow values, with its corresponding year, are shown below:')
print(reports)
    
# %%

#6. Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other value and report the date and the new window you used

flows10=data.loc[(data.flow>=55.41*0.90) & (data.flow<=55.41*1.10), ['year', 'month', 'day','flow']]
print('\n The flows that are within 10% of my forecast for Week 1 are:')
print(flows10)
# %%
