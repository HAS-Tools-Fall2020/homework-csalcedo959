# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Starter Code
# Count the number of values with flow > 600 and month ==7
flow_count = np.sum((flow_data[:,3] > 600) & (flow_data[:,1]==7))

# this gives a list of T/F where the criteria are met
(flow_data[:,3] > 600) & (flow_data[:,1]==7)

# this give the flow values where that criteria is met
flow_pick = flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7), 3]

# this give the year values where that criteria is met
year_pic = flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7), 0]

# this give the all rows  where that criteria is met
all_pic = flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7), ]

# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', flow_mean, "when this is true")

# Make a histogram of data
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)
# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])



# %%
## Homework # 4:

## Make a box-whiskers plot to compare the means among anual flows in Verde river
fig, ax=plt.subplots()
plt.boxplot((flow_data[flow_data[:,0]==1989,3],flow_data[flow_data[:,0]==1990,3],flow_data[flow_data[:,0]==1991,3],\
        flow_data[flow_data[:,0]==1992,3],flow_data[flow_data[:,0]==1993,3],flow_data[flow_data[:,0]==1994,3],\
                flow_data[flow_data[:,0]==1995,3],flow_data[flow_data[:,0]==1996,3],flow_data[flow_data[:,0]==1997,3],\
                        flow_data[flow_data[:,0]==1998,3],flow_data[flow_data[:,0]==1999,3],flow_data[flow_data[:,0]==2000,3],\
                                flow_data[flow_data[:,0]==2001,3],flow_data[flow_data[:,0]==2002,3],flow_data[flow_data[:,0]==2003,3],\
                                        flow_data[flow_data[:,0]==2004,3],flow_data[flow_data[:,0]==2005,3],flow_data[flow_data[:,0]==2006,3],\
                                                flow_data[flow_data[:,0]==2007,3],flow_data[flow_data[:,0]==2008,3],flow_data[flow_data[:,0]==2009,3],\
                                                        flow_data[flow_data[:,0]==2010,3],flow_data[flow_data[:,0]==2011,3],flow_data[flow_data[:,0]==2012,3],\
                                                                flow_data[flow_data[:,0]==2013,3],flow_data[flow_data[:,0]==2014,3],flow_data[flow_data[:,0]==2015,3],\
                                                                        flow_data[flow_data[:,0]==2016,3],flow_data[flow_data[:,0]==2017,3],flow_data[flow_data[:,0]==2018,3],\
                                                                                flow_data[flow_data[:,0]==2019,3],flow_data[flow_data[:,0]==2020,3]), showfliers=False,showmeans=True)
ax.set_title('Daily flowrate per year')
ax.set_ylabel('Daily Flow (cfs)')
ax.set_xticklabels(['1989','1990','1991','1992','1993','1994','1995','1996','1997','1998',\
        '1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',\
                '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020'], rotation=90)

#Plot the anual average for daily flows 
means_flow=np.zeros((32,2))
for i in range(0,32):
 means_flow[i,0]=1989+i
 means_flow[i,1]=np.mean(flow_data[flow_data[:,0]==1989+i,3])

print(means_flow)

fig, ay=plt.subplots()
plt.bar(means_flow[:,0],means_flow[:,1])
ay.set_title('Anual Mean Daily Flowrate')
ay.set_ylabel('Mean Daily Flow (cfs)')

#Comparison between year 2009 and 2020
fig, az=plt.subplots()
az.plot(flow_data[flow_data[:,0]==2009,3],label='2009')
az.plot(flow_data[flow_data[:,0]==2020,3],label='2020')
az.legend(loc='best')

# %% 
#Forecasts Week 4

#Looks for the start and end of the periods of interest: June 01 - Sept. 19
for j in range(0,flow_data.shape[0]):
        if flow_data[j,0]==2009 and flow_data[j,1]==6 and flow_data[j,2]==1:
                strt09=j
                print(strt09)
        elif flow_data[j,0]==2009 and flow_data[j,1]==9 and flow_data[j,2]==19:
                end09=j
                print(end09)
        elif flow_data[j,0]==2020 and flow_data[j,1]==6 and flow_data[j,2]==1:
                strt20=j
                print(strt20)
        elif flow_data[j,0]==2020 and flow_data[j,1]==9 and flow_data[j,2]==19:
                end20=j
                print(end20)

#Creates arrays with the previous information
array09=flow_data[strt09:end09]
array20=flow_data[strt20:end20]

#Calculates a proportional factor between 2020 and 2009
prop_factor = np.divide(array20,array09)
mprop = np.mean(prop_factor[:,3])

fig, ap=plt.subplots()
ap.plot(prop_factor[:,3])
ap.set_title('Proportional factors between 2020/2009')
ap.set_ylabel('Multiplier')
ap.set_xlabel('Days between June 1 - Sept 19')

# Forecast Week 1 & 2
av_factor =np.mean(prop_factor[91:110,3])
print('Mean multiplier between Sept 1- 19:',av_factor)

#ArrayNewForecast
arrayW1=flow_data[end09+1:end09+8]
arrayW2=flow_data[end09+8:end09+15]

forWeek1=np.multiply(arrayW1,av_factor)
forWeek2=np.multiply(arrayW2,av_factor)

print('Week 1 and Week 2 Forecasts')
print('Forecast Week 1',np.mean(forWeek1[:,3]))
print('Forecast Week 2',np.mean(forWeek2[:,3]))

#Seasonal Forecasts
#Looks for the start and end of the periods of interest: Jul. 21 - Aug. 21
for j in range(0,flow_data.shape[0]):
        if flow_data[j,0]==2009 and flow_data[j,1]==7 and flow_data[j,2]==21:
                strtN09=j
                print(strtN09)
        elif flow_data[j,0]==2009 and flow_data[j,1]==8 and flow_data[j,2]==21:
                endN09=j
                print(endN09)
        elif flow_data[j,0]==2020 and flow_data[j,1]==7 and flow_data[j,2]==21:
                strtN20=j
                print(strtN20)
        elif flow_data[j,0]==2020 and flow_data[j,1]==8 and flow_data[j,2]==21:
                endN20=j
                print(endN20)

#Creates arrays with the previous information
arrayN09=flow_data[strtN09:endN09]
arrayN20=flow_data[strtN20:endN20]

#arr009=flow_data[(flow_data[:,0]==2009)&(flow_data[:1]==7)&(flow_data[:,2]==21):(flow_data[:,0]==2009)&(flow_data[:1]==8)&(flow_data[:,2]==21)]

#Calculates a proportional factor between 2020 and 2009
prop_factor = np.divide(arrayN20,arrayN09)
mprop = np.mean(prop_factor[:,3])

#ArrayNewForecast
arrayW1=flow_data[endN09+1:endN09+8]
arrayW2=flow_data[endN09+8:endN09+15]
arrayW3=flow_data[endN09+15:endN09+22]
arrayW4=flow_data[endN09+22:endN09+29]
arrayW5=flow_data[endN09+29:endN09+36]
arrayW6=flow_data[endN09+36:endN09+42]
arrayW7=flow_data[endN09+42:endN09+49]
arrayW8=flow_data[endN09+49:endN09+56]
arrayW9=flow_data[endN09+56:endN09+63]
arrayW10=flow_data[endN09+63:endN09+70]
arrayW11=flow_data[endN09+70:endN09+77]
arrayW12=flow_data[endN09+77:endN09+84]
arrayW13=flow_data[endN09+84:endN09+91]
arrayW14=flow_data[endN09+91:endN09+98]
arrayW15=flow_data[endN09+98:endN09+105]
arrayW16=flow_data[endN09+105:endN09+112]

forWeek1=np.multiply(arrayW1,av_factor)
forWeek2=np.multiply(arrayW2,av_factor)

print('Seasonal Forecast')
print('Forecast Week 1',np.mean(np.multiply(arrayW1[:,3],mprop)))
print('Forecast Week 2',np.mean(np.multiply(arrayW2[:,3],mprop)))
print('Forecast Week 3',np.mean(np.multiply(arrayW3[:,3],mprop)))
print('Forecast Week 4',np.mean(np.multiply(arrayW4[:,3],mprop)))
print('Forecast Week 5',np.mean(np.multiply(arrayW5[:,3],mprop)))
print('Forecast Week 6',np.mean(np.multiply(arrayW6[:,3],mprop)))
print('Forecast Week 7',np.mean(np.multiply(arrayW7[:,3],mprop)))
print('Forecast Week 8',np.mean(np.multiply(arrayW8[:,3],mprop)))
print('Forecast Week 9',np.mean(np.multiply(arrayW9[:,3],mprop)))
print('Forecast Week 10',np.mean(np.multiply(arrayW10[:,3],mprop)))
print('Forecast Week 11',np.mean(np.multiply(arrayW11[:,3],mprop)))
print('Forecast Week 12',np.mean(np.multiply(arrayW12[:,3],mprop)))
print('Forecast Week 13',np.mean(np.multiply(arrayW13[:,3],mprop)))
print('Forecast Week 14',np.mean(np.multiply(arrayW14[:,3],mprop)))
print('Forecast Week 15',np.mean(np.multiply(arrayW15[:,3],mprop)))
print('Forecast Week 16',np.mean(np.multiply(arrayW16[:,3],mprop)))

#Question #3
flow_count = np.sum((flow_data[:,3] > 56.39) & (flow_data[:,1]==9))
sept_entries=np.sum(flow_data[:,1]==9)
print('The total number of times the daily flow in september was greater than my forecast for Week 1 (56.39 cfs) was',flow_count,', which represents a', (flow_count/sept_entries)*100,'%.')

#Question #4
#Before 2000
flow_count_2000 = np.sum((flow_data[:,3] > 56.39) & (flow_data[:,0]<2000) & (flow_data[:,1]==9))
sept_entries_2000=np.sum((flow_data[:,1]==9) & (flow_data[:,0]<2000))
print('If only the years before 2000 were considered, the total number of times the daily flow in september was greater than my forecast for Week 1 (56.39 cfs) was',flow_count_2000,', which represents a', (flow_count_2000/sept_entries_2000)*100,'%.')

#After 2010
flow_count_2010 = np.sum((flow_data[:,3] > 56.39) & (flow_data[:,0]>2010) & (flow_data[:,1]==9))
sept_entries_2010=np.sum(flow_data[:,1]==9 & (flow_data[:,0]>2010))
print('If only the years after 2010 were considered, the total number of times the daily flow in september was greater than my forecast for Week 1 (56.39 cfs) was',flow_count_2000,', which represents a', (flow_count_2000/sept_entries_2000)*100,'%.')

#Question # 5
early_sept=np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2]<=15),3])
late_sept=np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2]>15),3])

if early_sept > late_sept:
        print("Flow tends to decrease in late september, going from",early_sept,'to',late_sept)
else:
        print("Flow tends to increase in late september, going from",early_sept,'to',late_sept)



# %%
