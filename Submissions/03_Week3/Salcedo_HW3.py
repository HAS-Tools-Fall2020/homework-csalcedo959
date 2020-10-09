# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week3.txt'
filepath = os.path.join('../data', filename)

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

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Here is some starter code to illustrate some things you might like to do
# Modify this however you would like to do your homework. 
# From here on out you should use only the lists created in the last block:
# flow, date, yaer, month and day

# Calculating some basic properites
print(min(flow))
print(max(flow))
print(np.mean(flow))
print(np.std(flow))

# Making and empty list that I will use to store
# index values I'm interested in
ilist = []

# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify
for i in range(len(flow)):
        if flow [i] > 600 and month[i] == 7:
                ilist.append(i)

# see how many times the criteria was met by checking the length
# of the index list that was generated
print(len(ilist))

# Alternatively I could have  written the for loop I used 
# above to  create ilist like this
ilist2 = [i for i in range(len(flow)) if flow[i] > 600 and month[i]==7]
print(len(ilist2))

# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified 
# in the ilist
subset = [flow[j] for j in ilist]
# %%
# Developed code for Assignment #3

#Creation of lists including the flow between Jan 01 and Sep 12 for each year between 1989 and 2020
#for i in range(1989,2020):
#        yr=str(i)
#        tx="list"
#        nameList = tx+yr
#        nameList=[j for j in range(len(flow)) if year[j]==i and month[j]<9]
#        print(len(nameList))

list2009=[i for i in range(len(flow)) if year[i]==2009 and month[i]<8]
list2020=[i for i in range(len(flow)) if year[i]==2020 and month[i]<8]
#Get a correction factor
correction=np.mean(list2020)/np.mean(list2009)
print(correction)

#Calculate average for 2009 and correct them using the correction factor. 
forecast=[]
for j in range(len(flow)):
        if year[j]==2009 and month[j]==8 and day[j]==22:
                ind=j
                print(ind)

sumWeekAver=0
i=0
week=1
for k in range(ind,ind+112):
        sumWeekAver=sumWeekAver+flow[k]
        i=i+1
        if i==7:
                CorrAver=(sumWeekAver/7)*correction
                forecast.append(CorrAver)
                print(week,CorrAver)
                sumWeekAver=0
                week=week+1
                i=0

print(forecast)

#Question # 1
print(len(flow))
print(len(year))
print(len(month))
print(len(day))

#Question # 2
#Look for september 2009 and forecast the values
for j in range(len(flow)):
        if year[j]==2009 and month[j]==9 and day[j]==1:
                ind=j
                print(ind)

#Perform the forecasting
forSept=[]
for j in range(ind,ind+30): 
        dailyFor=flow[j]*correction
        forSept.append(dailyFor)
print("# of Forecasts in september:", len(forSept))

#Determines how many times the daily flow was greater than my forecast
septFlow=[i for i in range(len(flow)) if month[i]==9] #Total number of entries registered for september
yr = 1 #Index for taking into account the year
greaterInd=0
for i in range(len(septFlow)):
        if i< 30:
                if septFlow[i]>forSept[i]:
                        greaterInd=greaterInd+1
        else:
                if i%30 == True:
                        yr=yr+1
                
                if septFlow[i-yr*30]>forSept[i-yr*30]:
                        greaterId=greaterInd+1      
                     
prop = greaterInd/len(septFlow)*100
print("# of values in september:", len(septFlow))
print("# of values greater than the forecast", greaterInd)
print("Ratio", prop)

#Question # 3
#Determines how many times the daily flow was greater than my forecast
septFlow=[i for i in range(len(flow)) if month[i]==9 and year[i]<2000 or month[i]==9 and year[i]>2010] #Total number of entries registered for september
yr = 1 #Index for taking into account the year
greaterInd=0
for i in range(len(septFlow)):
        if i< 30:
                if septFlow[i]>forSept[i]:
                        greaterInd=greaterInd+1
        else:
                if i%30 == True:
                        yr=yr+1
                
                if septFlow[i-yr*30]>forSept[i-yr*30]:
                        greaterId=greaterInd+1      
                     
prop = greaterInd/len(septFlow)*100
print("# of values in september:", len(septFlow))
print("# of values greater than the forecast", greaterInd)
print("Ratio", prop)


#Question # 4
septEarly=[i for i in range(len(flow)) if month[i]==9 and day[i]<=15]
septLate=[i for i in range(len(flow)) if month[i]==9 and day[i]>15]

if np.mean(septEarly) > np.mean(septLate):
        print("Flow tends to decrease in late september")
else:
        print("Flow tends to increase in late september")

# %%
