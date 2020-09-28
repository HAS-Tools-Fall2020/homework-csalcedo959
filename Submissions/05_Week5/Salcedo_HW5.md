# Forecast Week 5
## *Name:* Camilo Salcedo
## *Date:* September 28th 2020
___

# Forecast description

Using a plot to show the mean flows for the months of July, August and September at each year within the analysis period, it was determined which years had a similar behavior during those months historically. In this sense, for August, the most similar year was 2002, while for September it was 2010. Meanwhile, the most similar year to 2020 in terms of its mean was 2019. Hence, a proportional factor was estimated between 2019 and 2002 (August) and 2010 (September), and then a second factor was calculated between 2020 and 2019. In this way, the forecast was performed according to the dates established in the contest (Seasonal forecast using information until Aug. 21/2020 and for the short forecast using data until Sept. 26/2020).

# Assignment Questions
## 1. Provide a summary of the data frames properties.
The dataframe is composed by 4 columns: Year, Month, Day and Flow. The types of each column are float64. The summary of each column is described below:

The column "Year" is composed as follows:
|:--------|------------|
|count    |11592.000000|
|mean     | 2004.372671|
|std      |    9.162864|
|min      | 1989.000000|
|25%      | 1996.000000|
|50%      | 2004.000000|
|75%      | 2012.000000|
|max      | 2020.000000|
Name: year, dtype: float64

 The column "Month" is composed as follows:
 count    11592.000000
mean         6.486542
std          3.438779
min          1.000000
25%          4.000000
50%          6.000000
75%          9.000000
max         12.000000
Name: month, dtype: float64

 The column "Day" is composed as follows:
 count    11592.000000
mean        15.724379
std          8.798330
min          1.000000
25%          8.000000
50%         16.000000
75%         23.000000
max         31.000000
Name: day, dtype: float64

 The summary of the column "Flow" is below:      
count  11592.000000
mean     345.630461
std     1410.832968
min       19.000000
25%       93.700000
50%      158.000000
75%      216.000000
max    63400.000000

## 2. Provide a summary of the flow column including the min, mean, max, standard deviation and quartiles.

The summary of the column "Flow" is below:           
count  11592.000000
mean     345.630461
std     1410.832968
min       19.000000
25%       93.700000
50%      158.000000
75%      216.000000
max    63400.000000

## 3.  Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)

The summary of flow data grouped in a monthly basis is shown below:         flow                                                            \
count        mean          std    min      25%     50%      75%   
month                                                                    
1      992.0  706.320565  2749.153983  158.0  202.000  219.50   292.00   
2      904.0  925.252212  3348.821197  136.0  201.000  244.00   631.00   
3      992.0  941.731855  1645.803872   97.0  179.000  387.50  1060.00   
4      960.0  301.240000   548.140912   64.9  112.000  142.00   214.50   
5      992.0  105.442339    50.774743   46.0   77.975   92.95   118.00   
6      960.0   65.998958    28.966451   22.1   49.225   60.50    77.00   
7      992.0   95.571472    83.512343   19.0   53.000   70.90   110.00   
8      992.0  164.354133   274.464099   29.6   76.075  114.00   170.25   
9      956.0  172.688808   286.776478   36.6   88.075  120.00   171.25   
10     961.0  146.168991   111.779072   69.9  107.000  125.00   153.00   
11     930.0  205.105376   235.673534  117.0  156.000  175.00   199.00   
12     961.0  337.097815  1097.280926  155.0  191.000  204.00   228.00   


    max  
month           
1      63400.0  
2      61000.0  
3      30500.0  
4       4690.0  
5        546.0  
6        481.0  
7       1040.0  
8       5360.0  
9       5590.0  
10      1910.0  
11      4600.0  
12     28700.0  


## 4. Provide a table with the 5 highest and 5 lowest flow values for the period of record. Include the date, month and flow values in your summary.

The top 5-highest flows are shown below:
      year  month  day     flow
1468  1993      1    8  63400.0
1511  1993      2   20  61000.0
2236  1995      2   15  45500.0
5886  2005      2   12  35600.0
2255  1995      3    6  30500.0

 The top 5-lowest flows are shown below:
      year  month  day  flow
8584  2012      7    3  23.4
8580  2012      6   29  22.5
8581  2012      6   30  22.1
8583  2012      7    2  20.1
8582  2012      7    1  19.0

## 5. Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in.

The lowest and highest flow values, with its corresponding year, are shown below:
  Month          Max Year(max)        Min Year(min)
0      1  [[63400.0]]  [[1993]]  [[158.0]]  [[2003]]
1      2  [[61000.0]]  [[1993]]  [[136.0]]  [[1991]]
2      3  [[30500.0]]  [[1995]]   [[97.0]]  [[1989]]
3      4   [[4690.0]]  [[1991]]   [[64.9]]  [[2018]]
4      5    [[546.0]]  [[1992]]   [[46.0]]  [[2004]]
5      6    [[481.0]]  [[1992]]   [[22.1]]  [[2012]]
6      7   [[1040.0]]  [[2006]]   [[19.0]]  [[2012]]
7      8   [[5360.0]]  [[1992]]   [[29.6]]  [[2019]]
8      9   [[5590.0]]  [[2004]]   [[36.6]]  [[2020]]
9     10   [[1910.0]]  [[2010]]   [[69.9]]  [[2012]]
10    11   [[4600.0]]  [[2004]]  [[117.0]]  [[2016]]
11    12  [[28700.0]]  [[2004]]  [[155.0]]  [[2012]]

## 6. Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other value and report the date and the new window you used

The flows that are within 10% of my forecast for Week 1 are:
      year  month  day  flow
160    1989      6   10  58.0
161    1989      6   11  53.0
162    1989      6   12  57.0
164    1989      6   14  57.0
165    1989      6   15  60.0
...     ...    ...  ...   ...
11585  2020      9   20  52.6
11586  2020      9   21  55.9
11587  2020      9   22  60.0
11590  2020      9   25  58.1
11591  2020      9   26  55.7

[566 rows x 4 columns]
