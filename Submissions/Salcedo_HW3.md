# Forecast Week 3
## *Name:* Camilo Salcedo
## *Date:* September 14th 2020

# Forecast description

As in the previous forecasts, I decided to use a dry year similar in magnitude to 2020. In this sense, I got the average flow of Verde River between January 01 and August 01 for both 2009 and 2020, and determine a correction factor of 1.542 approximately. Based on this, I decided to update the forecast by multiplying the dry year weekly average by the correction factor. Using more data in this test didn't seem to works well.

#Assignment Questions

##1. Describe the variables flow, year, month, and day. What type of objects are they, what are they composed of, and how long are they?
### Flow:
List of daily measured flow in Verde River between 01-01-1989 and 12-09-2020 in cfs. Float type. Length of 11579 elements.
### Year:
List of the variable "year" of the measurements. An integer between 1989 and 2020. Integer type. Length of 11579 elements.
### Month:
List of the variable "month" of the measurements. An integer between 1 and 12.  Integer type. Length of 11579 elements.
### Day:
List of the variable "day" of the measurements. An integer between 1 and 31.  Integer type. Length of 11579 elements.

##2. How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?
Among all the years analyzed, during September 23 times the daily flow was greater than my prediction. This is equivalent to a 2.44% of the total measurements in September (943).

##3. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)
When the years of analysis is limited to the ones before 2000 and after 2010, the amount of times the daily flow measurements were greater than my forecasts were 23 times. However, the number of measurements taken into account were 613. Therefore, the percentage reduced to 3.75%.

##4. How does the daily flow generally change from the first half of September to the second?
In average, the flow tends to decrease by the second half of September. This was calculated using the comparison of mean flows: Early September registered a mean flow of 5887.53 cfs and Late September registered a mean flow of 5743.61 cfs.
