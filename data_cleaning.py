import pandas as pd
import numpy as np


#read csv
df=pd.read_csv('daatasets/dfs.csv')
# print(df)
# print(df.info())



#1
print(df.isnull().sum())    #show the number of missing data in each column
df=df.dropna()   #remove rows with missing data
#To fill in missing values  df.fillna(df.mean(),inplace=True)



#2    Check and correct illogical or incorrect values
print(df.describe())  
logical_range={'Porosity':(0,1),
               'Permeability':(0,10000),
               'Depth':(0,10000),
               'Temperature':(0,300),
               'Pressure':(0,10000),
               'Injection':(-1000,1000),
               'Saturation_Gaz':(0,1),
               'Year':(1900,2100),
               'month':(1,12),
               'Day':(1,31)}
for column,(min_val,max_val) in logical_range.items():
    if column in df.columns:
        outliers=df[(df[column]<min_val)|(df[column]>max_val)][column]
        if not outliers.empty:
            print(f"column{column} has invalid elements")
            print(outliers)
#correct invalid elements
for colum,(min_val,max_val) in logical_range.items():
    if colum in df.columns:
        df.loc[(df[colum]<min_val)|(df[colum]>max_val),colum]=np.nan
        df[colum].fillna(df[colum].mean(),inplace=True)
print(df.describe())


#3
print(df.head())
for col in ['year','month','day']:
    df[col]=df[col].round().astype('Int64')
    df['year']=df['year'].apply(lambda x :x if 1900<=x<=2100 else np.nan)
    df['month']=df['month'].apply(lambda x:x if 1 <= x <=12 else np.nan)
    df['day']=df['day'].apply(lambda x:x if 1 <= x <=31 else np.nan)
    df['year'].fillna(2000)
    df['month'].fillna(1)
    df['day'].fillna(1)
df['date']=pd.to_datetime(df[['year','month','day']].astype(str).agg('-'.join,axis=1),errors='coerce')
df=df.drop(columns=['year','month','day','month_cos','day_cos'])
numeric_columns=['Porosity','Permeability','Depth','Temperature','Pressure','Injection','Saturation_Gaz']
for y in numeric_columns:
    if y in df.columns:
        df[y]=pd.to_numeric(df[y],errors='coerce')
        df[y]=df[y].round(3)
       
        

#4
df=df.drop_duplicates()   #remove duplicates
df.to_csv('new_dfs.csv',index=False)

