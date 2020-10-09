# Forecast Week 4
## *Name:* Camilo Salcedo
## *Date:* September 21st 2020
___
### Grade
3/3 - nice job, I like your reasoning for the forecast.
___

# Forecast description

Using a plot showing the mean daily flows at each year between 1989 and 2020, I tried to confirm my previous assumption that year 2020 is having a similar behavior to 2009. Despite the average daily flow is different, the behavior for summer season is very similar, which was demonstrated by a comparison plot developed comparing only 2009 and 2020. Hence, I decided to limit the time horizon between June 06 to September 19 (for short forecast), to determine the proportional change between flow values 2020/2009. After, the time horizon was shortened because the trend of the multiplier tend to increase since September 1, then the new period of time considered was between September 01 to 19, with a mean proportional value of 0.53. For the seasonal forecast, the same procedure was performed, but the base time window for getting the proportional value was between July 21 to August 21. The corresponding plots can be obtained by running the code.

# Assignment Questions
## 1. Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.
At first, my attempt was to include a Box & Whiskers plot in order to analyze the dispersion of the data. Hence, by plotting this, it can be observed that in years such as 1993, 2005 and 2010, the dispersion among values was very significant, while in years such as 1990, 1996, 2006 and 2018 the values were not so disperse. This trend can be associated with climatic effects. Despite the importance of this plot, I decided to analyze the mean values at every year in an attempt to understand if the comparison between means was a good approach to perform the forecasts. In conclusion, it was observed that analyzing the mean behavior along a year is a very big time window, and it would be better to analyze it in smaller time horizons. As an example, despite 2020 and 2009 have different mean daily flows and their behavior at the first semester of the year was very different also, after june, the trend tend to be similar, which can be a good approach to make the forecast.

## 2. Describe the variable flow_data?
Flow_data is an array that contains all the measurements of daily flow at Verde River, including: Year, Month, Day and Daily Flow.
### What is it:
It is an array.
### What type of values is it composed of:
The type of elements are: : numpy.ndarray
### What is are its dimensions, and total size?
The dimensions of the array are (11585,4). The total size is 46,340.

## 3.How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)??
The total number of times the daily flow in September was greater than my forecast for Week 1 (56.39 cfs) was 912 , which represents a 96.10115911485775 %.

## 4. How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)
If only the years before 2000 were considered, the total number of times the daily flow in September was greater than my forecast for Week 1 (56.39 cfs) was 330 , which represents a 100.0 %. In the other hand, if only the years after 2010 were considered, the total number of times the daily flow in September was greater than my forecast for Week 1 (56.39 cfs) was 330 , which represents a 100.0 %. The reason is that according to my analysis, 2020 is a dry year.

## 5. How does the daily flow generally change from the first half of September to the second?
Flow tends to decrease in late September, going from 178.0727083333333 cfs to 168.88400852878465 cfs.
