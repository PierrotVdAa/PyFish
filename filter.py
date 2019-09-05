import pandas as p
import numpy as np
list_of_unneeded_p01 = 'ADEPZZ01'#,'SAMPID01']

df = p.read_csv('North_biota_unrestricted_transposed_flitered_super2.csv', encoding='latin-1')
df = df[df.P01_conceptid != 'ADEPZZ01']
df = df[df.P01_conceptid != 'SAMPID01']
df['time_ISO8601'] = df['time_ISO8601'].str.slice(0,10,1)
df = df[df['Longitude [degrees_east]'] > 0 ]#&
df = df[df['Longitude [degrees_east]'] < 8]
df = df[df['Latitude [degrees_north]'] > 51 ]#&
df = df[df['Latitude [degrees_north]'] < 60]

print(df.columns.values)

#shrink = df.groupby(['Station','time_ISO8601','P01_preflabel']).mean()
df['Latitude [degrees_north]'] = df['Latitude [degrees_north]'] - df['Latitude [degrees_north]'] % 0.01 #.round(3)
df['Longitude [degrees_east]'] = df['Longitude [degrees_east]'] - df['Longitude [degrees_east]'] % 0.01 #.round(3)

print(df.columns.values)
shrink = df.groupby(['Latitude [degrees_north]', 'Longitude [degrees_east]', 'time_ISO8601', 'S27_preflabel','Units'], as_index=False).mean()

print(shrink)
#shrink.to_csv('output2.csv')

global_dataframe = p.read_csv('datapoints.csv')

print(global_dataframe.columns.values)

#global_dataframe.date = p.to_datetime(global_dataframe.date)

global_dataframe['Element'] = np.NAN
global_dataframe['Units'] = np.NAN
global_dataframe['Element_value'] = np.NAN

count = 0
for index, row in global_dataframe.iterrows():
    for ind, df_row in df.iterrows():
        if row.lat_bin/100 == df_row['Latitude [degrees_north]'] and row.lon_bin/100 == df_row['Longitude [degrees_east]'] and row.date == df_row['time_ISO8601']:
            count = count + 1
            row.Element = df_row['S27_preflabel']
            row.Element_value = df_row['Value']
            row.Units = df_row['Units']
        #else:
         #   print(f"{row.lat_bin/100} == {df_row['Latitude [degrees_north]']} and {row.lon_bin/100} == {df_row['Longitude [degrees_east]']}")

global_dataframe.to_csv('bigData.csv')
