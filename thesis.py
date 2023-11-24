import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import math

df = pd.read_csv('test.csv')
df1 = df.copy()
df1.drop(columns=['Matchday', 'Venue', 'For', 'Unnamed: 4',
         'Opponent', 'Unnamed: 6', 'Result', 'Pos.'], inplace=True)

# df1 = df1.dropna(subset=['Date'], inplace=True)

# df1.head()

df1['Date'] = pd.to_datetime(df1['Date'])
first_year = df1.copy()

first_year['Date'] = df1['Date'].dt.year
first_year['month'] = df1['Date'].dt.month

years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

df2 = {}

for year in years:
    data = first_year[first_year['Date'] == year]
    #first_year.drop(columns=['Date'], inplace=True)
    print(data.month.values)
    values = []
    for x in data.month.values:
        if (x in values):
            continue
        else:
            values.append(x)

    values = sorted(values)

    for i in values:
        print('start of ' + str(year) + 'month' + str(i))
        result = data[data['month'] == i]
        print('goals')
        print(result.goal.sum())
        print('assists')
        print(result.assassits.sum())
        print('yellow')
        print(result.yello.count())
        print('second yellow')
        print(result['second yellow'].count())
        yellowCount = result.yello.count()
        if result['second yellow'].count() > 0:
            yellowCount += result['second yellow'].count()
        print('red')
        print(result.red.count())
        redCount = result.red.count()
        if result['second yellow'].count() > 0:
            redCount += result['second yellow'].count()
        print('m')
        print(result.month.count())
        print('t')
        print(result.time.count())
        try:
            plyr = result.time.astype(int).sum() / result.month.count()
        except:
            plyr = result.time.count() / result.month.count()
        print('percent')
        print(plyr)
        print(result.time)
        numerator = []
        for key, value in result.time.items():
            if type(value) == str:
                y = int(value[0:len(value)-1])
                y = float(y)
                numerator.append(y)

        play = (sum(numerator)/(result.month.count() * 90))
        print(play)
        print('end of ' + str(year) + 'month' + str(i))
        # df2.update({str(i) + '/' + str(year): {'goals': result.goal.sum(), 'assist': result.assassits.sum(), 'yellow': yellowCount, 
        #                                        'red': redCount, 'plyr': play}})
        df2.update({str(i) + '/' + str(year): {'date': str(i) + '/' + str(year), 'goals': result.goal.sum(), 'assist': result.assassits.sum(), 'yellow': yellowCount, 
                                               'red': redCount, 'plyr': play}})
    
print(df2)
df2 = pd.DataFrame(df2)
# df2 = pd.melt(df2)
# print(df2)
df2.T.to_csv('data.csv', index=False, encoding='utf-8')
#df2


# =ARRAYFORMULA(SEQUENCE(12 (how many cells),1 (number of Columns),100 (the number that will be written),1 (the difference betwwen the sequence)))