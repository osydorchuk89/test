"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants

Test task
"""

# TODO Import the necessary libraries
import pandas as pd
import numpy as np

# TODO Import the dataset 

path = r'./data/weather_dataset.data'
data = pd.read_csv(path, sep=';')
data.head()

# TODO  Assign it to a variable called data and replace the first 3 columns by a proper datetime index
# TODO Check if everything is okay with the data. Create functions to delete/fix rows with strange cases and apply them
# TODO Write a function in order to fix date (this relate only to the year info) and apply it
dates = '19' + data.Yr.astype(str) + '-' + data.Mo.astype(str) + '-' + data.Dy.astype(str)
data['date'] = dates
data.head()

# TODO Set the right dates as the index. Pay attention at the data type, it should be datetime64[ns]
data['date'] = pd.to_datetime(dates)
data.drop(columns=['Yr', 'Mo', 'Dy'], inplace=True)

# TODO Compute how many values are missing for each location over the entire record
locations = [col for col in data.columns if col.startswith('loc')]
for loc in locations:
    nans = data[loc].isna().sum()
    print(f'There are {nans} missing values in the column {loc}')

# TODO Compute how many non-missing values there are in total
all_values = sum(data.count())
print(f'There are {all_values} non-missing values in total')

# TODO Calculate the mean windspeeds of the windspeeds over all the locations and all the times
# replacing erroneous entries with NaNs and then filling them with column means
bad_strings = ['None', 'NONE', '-123*None', 'nodata', '1.0k']

for loc in locations:
    data[loc] = data[loc].apply(lambda x: str(x).replace(',', '.'))
    data[loc] = data[loc].replace(bad_strings, np.nan).astype(float)
    data[loc] = data[loc].fillna(data[loc].mean())

# replacing all negative numbers with zero
for loc in locations:
    data[loc].clip(lower=0, inplace=True)

# replacing outliers in location 9 with median
data.loc9 = np.where(data.loc9 > 25.88, data.loc9.median(), data.loc9)

data[locations].mean()

# TODO Create a DataFrame called loc_stats and calculate the min, max and mean windspeeds and standard deviations of the windspeeds at each location over all the days
loc_stats = pd.DataFrame({
    'min': data[locations].min(),
    'max': data[locations].max(),
    'mean': data[locations].mean(),
    'std': data[locations].std(),
})

# TODO Find the average windspeed in January for each location
data[data.date.dt.month == 1].mean()

# TODO Downsample the record to a yearly frequency for each location
annual_data = data.set_index('date').resample('Y').mean()
annual_data.head()

# TODO Downsample the record to a monthly frequency for each location
monthly_data = data.set_index('date').resample('M').mean()
monthly_data.head()

# TODO Downsample the record to a weekly frequency for each location
weekly_data = data.set_index('date').resample('W').mean()
weekly_data.head()

# TODO Calculate the min, max and mean windspeeds and standard deviations of the windspeeds across all locations for each week (assume that the first week starts on January 2 1961) for the first 21 weeks
agg_weekly_data = data.set_index('date').resample('W').agg(['min', 'max', 'mean', 'std']).head(21)