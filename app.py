import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

df = pd.read_csv('test1.csv')
df1 = df.copy()
df1.drop(columns=['Matchday', 'Venue', 'For', 'Unnamed: 4',
         'Opponent', 'Unnamed: 6', 'Result', 'Pos.'], inplace=True)

df1['Date'] = pd.to_datetime(df1['Date'])
first_year = df1.copy()

first_year['Date'] = df1['Date'].dt.year
first_year['month'] = df1['Date'].dt.month

first_year = first_year[first_year['Date'] == 2015]
first_year.drop(columns=['Date'], inplace=True)
print(first_year.month.values)
result = first_year[first_year['month'] == 1]
print('goals')
print(result.goal.sum())
print('assists')
print(result.assassits.sum())
print('yellow')
print(result.yello.count())
print('second yellow')
print(result['second yellow'].count())
print('red')
print(result.red.sum())
print('m')
print(result.month.count())
print('t')
print(result.time.count())
plyr = result.time.count() / result.month.count()
print('percent')
print(plyr)
