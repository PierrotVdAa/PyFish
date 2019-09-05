import pandas as p
list_of_unneeded_p01 = 'ADEPZZ01'#,'SAMPID01']

df = p.read_csv('North_biota_unrestricted_transposed_flitered_super.csv')
df = df[df.P01_conceptid != 'ADEPZZ01']
df = df[df.P01_conceptid != 'SAMPID01']
df = df[df['Longitude [degrees_east]'] > 0 ]#&
df = df[df['Longitude [degrees_east]'] < 8]
df = df[df['Latitude [degrees_north]'] > 51 ]#&
df = df[df['Latitude [degrees_north]'] < 60]

print(df.columns.values)

shrink = df.groupby(['Station','time_ISO8601','P01_conceptid']).mean()

print(shrink)
