
# Exploratory Data Analysis for AQI dataset

This dataset contains the responses of a gas multisensor device deployed on the field in an Italian city. Hourly responses averages are recorded along with gas concentrations references from a certified analyzer. This dataset was taken from UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/index.php

## Content
The dataset contains 9357 instances of hourly averaged responses from an array of 5 metal oxide chemical sensors embedded in an Air Quality Chemical Multisensor Device. The device was located on the field in a significantly polluted area, at road level,within an Italian city. Data were recorded from March 2004 to February 2005 (one year) representing the longest freely available recordings of on field deployed air quality chemical sensor devices responses. Ground Truth hourly averaged concentrations for CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx) and Nitrogen Dioxide (NO2) and were provided by a co-located reference certified analyzer. Evidences of cross-sensitivities as well as both concept and sensor drifts are present as described in De Vito et al., Sens. And Act. B, Vol. 129,2,2008 (citation required) eventually affecting sensors concentration estimation capabilities. Missing values are tagged with -200 value.

We should use this for creating our Descentralized AQI Classifier solution.

## Loading the dataset


```python
train_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6__hHU1bGI7oczcrZifx8gFp23DXMQLVu6o_7AgPhh0fwCyH8XhWR0IbZgoT26SAmnQZH9rYsU-xc/pub?gid=1720806244&single=true&output=csv"
data = pd.read_csv(train_csv)
```

First , we should investigate the whole dataset, the kinds of data, null values and so on. Data info is a good function for that.


```python
data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9357 entries, 0 to 9356
    Data columns (total 15 columns):
     #   Column         Non-Null Count  Dtype 
    ---  ------         --------------  ----- 
     0   Date           9357 non-null   object
     1   Time           9357 non-null   object
     2   CO(GT)         9357 non-null   object
     3   PT08.S1(CO)    9357 non-null   int64 
     4   NMHC(GT)       9357 non-null   int64 
     5   C6H6(GT)       9357 non-null   object
     6   PT08.S2(NMHC)  9357 non-null   int64 
     7   NOx(GT)        9357 non-null   int64 
     8   PT08.S3(NOx)   9357 non-null   int64 
     9   NO2(GT)        9357 non-null   int64 
     10  PT08.S4(NO2)   9357 non-null   int64 
     11  PT08.S5(O3)    9357 non-null   int64 
     12  T              9357 non-null   object
     13  RH             9357 non-null   object
     14  AH             9357 non-null   object
    dtypes: int64(8), object(7)
    memory usage: 1.1+ MB


We have to turn the columns from object to float, to be easier to do the calculations.


```python
# Converter colunas numéricas para float
numerical_columns = [
    'CO(GT)', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)',
    'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)',
    'T', 'RH', 'AH'
]

for column in numerical_columns:
    data[column] = pd.to_numeric(data[column].astype(str).str.replace(',', '.'), errors='coerce')

# Verificar as primeiras linhas do DataFrame para garantir que as conversões foram bem-sucedidas
data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9357 entries, 0 to 9356
    Data columns (total 15 columns):
     #   Column         Non-Null Count  Dtype  
    ---  ------         --------------  -----  
     0   Date           9357 non-null   object 
     1   Time           9357 non-null   object 
     2   CO(GT)         9357 non-null   float64
     3   PT08.S1(CO)    9357 non-null   int64  
     4   NMHC(GT)       9357 non-null   int64  
     5   C6H6(GT)       9357 non-null   float64
     6   PT08.S2(NMHC)  9357 non-null   int64  
     7   NOx(GT)        9357 non-null   int64  
     8   PT08.S3(NOx)   9357 non-null   int64  
     9   NO2(GT)        9357 non-null   int64  
     10  PT08.S4(NO2)   9357 non-null   int64  
     11  PT08.S5(O3)    9357 non-null   int64  
     12  T              9357 non-null   float64
     13  RH             9357 non-null   float64
     14  AH             9357 non-null   float64
    dtypes: float64(5), int64(8), object(2)
    memory usage: 1.1+ MB



```python
data.describe()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CO(GT)</th>
      <th>PT08.S1(CO)</th>
      <th>NMHC(GT)</th>
      <th>C6H6(GT)</th>
      <th>PT08.S2(NMHC)</th>
      <th>NOx(GT)</th>
      <th>PT08.S3(NOx)</th>
      <th>NO2(GT)</th>
      <th>PT08.S4(NO2)</th>
      <th>PT08.S5(O3)</th>
      <th>T</th>
      <th>RH</th>
      <th>AH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
      <td>9357.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-34.207524</td>
      <td>1048.990061</td>
      <td>-159.090093</td>
      <td>1.865683</td>
      <td>894.595276</td>
      <td>168.616971</td>
      <td>794.990168</td>
      <td>58.148873</td>
      <td>1391.479641</td>
      <td>975.072032</td>
      <td>9.778305</td>
      <td>39.485380</td>
      <td>-6.837604</td>
    </tr>
    <tr>
      <th>std</th>
      <td>77.657170</td>
      <td>329.832710</td>
      <td>139.789093</td>
      <td>41.380206</td>
      <td>342.333252</td>
      <td>257.433866</td>
      <td>321.993552</td>
      <td>126.940455</td>
      <td>467.210125</td>
      <td>456.938184</td>
      <td>43.203623</td>
      <td>51.216145</td>
      <td>38.976670</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
      <td>-200.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.600000</td>
      <td>921.000000</td>
      <td>-200.000000</td>
      <td>4.000000</td>
      <td>711.000000</td>
      <td>50.000000</td>
      <td>637.000000</td>
      <td>53.000000</td>
      <td>1185.000000</td>
      <td>700.000000</td>
      <td>10.900000</td>
      <td>34.100000</td>
      <td>0.692300</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.500000</td>
      <td>1053.000000</td>
      <td>-200.000000</td>
      <td>7.900000</td>
      <td>895.000000</td>
      <td>141.000000</td>
      <td>794.000000</td>
      <td>96.000000</td>
      <td>1446.000000</td>
      <td>942.000000</td>
      <td>17.200000</td>
      <td>48.600000</td>
      <td>0.976800</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2.600000</td>
      <td>1221.000000</td>
      <td>-200.000000</td>
      <td>13.600000</td>
      <td>1105.000000</td>
      <td>284.000000</td>
      <td>960.000000</td>
      <td>133.000000</td>
      <td>1662.000000</td>
      <td>1255.000000</td>
      <td>24.100000</td>
      <td>61.900000</td>
      <td>1.296200</td>
    </tr>
    <tr>
      <th>max</th>
      <td>11.900000</td>
      <td>2040.000000</td>
      <td>1189.000000</td>
      <td>63.700000</td>
      <td>2214.000000</td>
      <td>1479.000000</td>
      <td>2683.000000</td>
      <td>340.000000</td>
      <td>2775.000000</td>
      <td>2523.000000</td>
      <td>44.600000</td>
      <td>88.700000</td>
      <td>2.231000</td>
    </tr>
  </tbody>
</table>
</div>



We see above that we have a lot of -200 values. -200 is a standard notation for invalid value. So we have to solve this.


```python
data.replace(-200, np.nan, inplace=True)
data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9357 entries, 0 to 9356
    Data columns (total 15 columns):
     #   Column         Non-Null Count  Dtype  
    ---  ------         --------------  -----  
     0   Date           9357 non-null   object 
     1   Time           9357 non-null   object 
     2   CO(GT)         7674 non-null   float64
     3   PT08.S1(CO)    8991 non-null   float64
     4   NMHC(GT)       914 non-null    float64
     5   C6H6(GT)       8991 non-null   float64
     6   PT08.S2(NMHC)  8991 non-null   float64
     7   NOx(GT)        7718 non-null   float64
     8   PT08.S3(NOx)   8991 non-null   float64
     9   NO2(GT)        7715 non-null   float64
     10  PT08.S4(NO2)   8991 non-null   float64
     11  PT08.S5(O3)    8991 non-null   float64
     12  T              8991 non-null   float64
     13  RH             8991 non-null   float64
     14  AH             8991 non-null   float64
    dtypes: float64(13), object(2)
    memory usage: 1.1+ MB


Seeing above, We can remove from the study the non numerical data and NMHC(GT) , which have more than 90% of missing values.


```python
data = data.drop(columns=['Date', 'Time', 'NMHC(GT)'])
data.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CO(GT)</th>
      <th>PT08.S1(CO)</th>
      <th>C6H6(GT)</th>
      <th>PT08.S2(NMHC)</th>
      <th>NOx(GT)</th>
      <th>PT08.S3(NOx)</th>
      <th>NO2(GT)</th>
      <th>PT08.S4(NO2)</th>
      <th>PT08.S5(O3)</th>
      <th>T</th>
      <th>RH</th>
      <th>AH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>7674.000000</td>
      <td>8991.000000</td>
      <td>8991.000000</td>
      <td>8991.000000</td>
      <td>7718.000000</td>
      <td>8991.000000</td>
      <td>7715.000000</td>
      <td>8991.000000</td>
      <td>8991.000000</td>
      <td>8991.000000</td>
      <td>8991.000000</td>
      <td>8991.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.152750</td>
      <td>1099.833166</td>
      <td>10.083105</td>
      <td>939.153376</td>
      <td>246.896735</td>
      <td>835.493605</td>
      <td>113.091251</td>
      <td>1456.264598</td>
      <td>1022.906128</td>
      <td>18.317829</td>
      <td>49.234201</td>
      <td>1.025530</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.453252</td>
      <td>217.080037</td>
      <td>7.449820</td>
      <td>266.831429</td>
      <td>212.979168</td>
      <td>256.817320</td>
      <td>48.370108</td>
      <td>346.206794</td>
      <td>398.484288</td>
      <td>8.832116</td>
      <td>17.316892</td>
      <td>0.403813</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.100000</td>
      <td>647.000000</td>
      <td>0.100000</td>
      <td>383.000000</td>
      <td>2.000000</td>
      <td>322.000000</td>
      <td>2.000000</td>
      <td>551.000000</td>
      <td>221.000000</td>
      <td>-1.900000</td>
      <td>9.200000</td>
      <td>0.184700</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.100000</td>
      <td>937.000000</td>
      <td>4.400000</td>
      <td>734.500000</td>
      <td>98.000000</td>
      <td>658.000000</td>
      <td>78.000000</td>
      <td>1227.000000</td>
      <td>731.500000</td>
      <td>11.800000</td>
      <td>35.800000</td>
      <td>0.736800</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.800000</td>
      <td>1063.000000</td>
      <td>8.200000</td>
      <td>909.000000</td>
      <td>180.000000</td>
      <td>806.000000</td>
      <td>109.000000</td>
      <td>1463.000000</td>
      <td>963.000000</td>
      <td>17.800000</td>
      <td>49.600000</td>
      <td>0.995400</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2.900000</td>
      <td>1231.000000</td>
      <td>14.000000</td>
      <td>1116.000000</td>
      <td>326.000000</td>
      <td>969.500000</td>
      <td>142.000000</td>
      <td>1674.000000</td>
      <td>1273.500000</td>
      <td>24.400000</td>
      <td>62.500000</td>
      <td>1.313700</td>
    </tr>
    <tr>
      <th>max</th>
      <td>11.900000</td>
      <td>2040.000000</td>
      <td>63.700000</td>
      <td>2214.000000</td>
      <td>1479.000000</td>
      <td>2683.000000</td>
      <td>340.000000</td>
      <td>2775.000000</td>
      <td>2523.000000</td>
      <td>44.600000</td>
      <td>88.700000</td>
      <td>2.231000</td>
    </tr>
  </tbody>
</table>
</div>



We still have the NaN values to remove, but it is easier now that we converted from -200.


```python
data = data.dropna()
data.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CO(GT)</th>
      <th>PT08.S1(CO)</th>
      <th>C6H6(GT)</th>
      <th>PT08.S2(NMHC)</th>
      <th>NOx(GT)</th>
      <th>PT08.S3(NOx)</th>
      <th>NO2(GT)</th>
      <th>PT08.S4(NO2)</th>
      <th>PT08.S5(O3)</th>
      <th>T</th>
      <th>RH</th>
      <th>AH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
      <td>6941.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.182467</td>
      <td>1119.913269</td>
      <td>10.554488</td>
      <td>958.543005</td>
      <td>250.671949</td>
      <td>816.893387</td>
      <td>113.874082</td>
      <td>1452.648898</td>
      <td>1057.756519</td>
      <td>17.755323</td>
      <td>48.881905</td>
      <td>0.985573</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.441158</td>
      <td>218.733754</td>
      <td>7.465226</td>
      <td>264.055002</td>
      <td>208.611371</td>
      <td>251.897200</td>
      <td>47.475017</td>
      <td>353.301576</td>
      <td>406.509957</td>
      <td>8.844909</td>
      <td>17.433193</td>
      <td>0.401097</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.100000</td>
      <td>647.000000</td>
      <td>0.200000</td>
      <td>390.000000</td>
      <td>2.000000</td>
      <td>322.000000</td>
      <td>2.000000</td>
      <td>551.000000</td>
      <td>221.000000</td>
      <td>-1.900000</td>
      <td>9.200000</td>
      <td>0.184700</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.100000</td>
      <td>956.000000</td>
      <td>4.900000</td>
      <td>760.000000</td>
      <td>103.000000</td>
      <td>642.000000</td>
      <td>79.000000</td>
      <td>1207.000000</td>
      <td>760.000000</td>
      <td>11.200000</td>
      <td>35.300000</td>
      <td>0.694100</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.900000</td>
      <td>1085.000000</td>
      <td>8.800000</td>
      <td>931.000000</td>
      <td>186.000000</td>
      <td>786.000000</td>
      <td>110.000000</td>
      <td>1457.000000</td>
      <td>1006.000000</td>
      <td>16.800000</td>
      <td>49.200000</td>
      <td>0.953900</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2.900000</td>
      <td>1254.000000</td>
      <td>14.600000</td>
      <td>1135.000000</td>
      <td>335.000000</td>
      <td>947.000000</td>
      <td>142.000000</td>
      <td>1683.000000</td>
      <td>1322.000000</td>
      <td>23.700000</td>
      <td>62.200000</td>
      <td>1.251600</td>
    </tr>
    <tr>
      <th>max</th>
      <td>11.900000</td>
      <td>2040.000000</td>
      <td>63.700000</td>
      <td>2214.000000</td>
      <td>1479.000000</td>
      <td>2683.000000</td>
      <td>333.000000</td>
      <td>2775.000000</td>
      <td>2523.000000</td>
      <td>44.600000</td>
      <td>88.700000</td>
      <td>2.180600</td>
    </tr>
  </tbody>
</table>
</div>



## Variable distributions

Visual distributions can help us to visualize the value distribution through the variables in the dataset before creating the model. So, lets get started we histograms of all the numerical values.


```python
for column in data:
    plt.figure(figsize=(8, 4))
    sns.histplot(data[column], kde=True, bins=50)
    plt.title(f'Distribuição de {column}')
    plt.xlabel(column)
    plt.ylabel('Frequência')
    plt.show()
```





    
![png](README_files/README_16_1.png)
    






    
![png](README_files/README_16_3.png)
    





    
![png](README_files/README_16_5.png)
    





    
![png](README_files/README_16_7.png)
    






    
![png](README_files/README_16_9.png)
    






    
![png](README_files/README_16_11.png)
    






    
![png](README_files/README_16_13.png)
    






    
![png](README_files/README_16_15.png)
    





    
![png](README_files/README_16_17.png)
    





    
![png](README_files/README_16_19.png)
    





    
![png](README_files/README_16_21.png)
    





    
![png](README_files/README_16_23.png)
    


Boxplots are a powerfull way to visualize if we have outliers in our study and what to do with them.


```python
for column in data:
    plt.figure(figsize=(8, 4))
    sns.boxplot(data[column])
    plt.title(f'Boxplot de {column}')
    plt.xlabel(column)
    plt.show()
```


    
![png](README_files/README_18_0.png)
    



    
![png](README_files/README_18_1.png)
    



    
![png](README_files/README_18_2.png)
    



    
![png](README_files/README_18_3.png)
    



    
![png](README_files/README_18_4.png)
    



    
![png](README_files/README_18_5.png)
    



    
![png](README_files/README_18_6.png)
    



    
![png](README_files/README_18_7.png)
    



    
![png](README_files/README_18_8.png)
    



    
![png](README_files/README_18_9.png)
    



    
![png](README_files/README_18_10.png)
    



    
![png](README_files/README_18_11.png)
    


We can choose to leave the outliers in, or remove than based on how far they are from the quartiles. Lets remove them and plot an before and after comparison:


```python
import matplotlib.pyplot as plt
import seaborn as sns

def remove_outliers(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    return df[(df[column_name] >= lower_limit) & (df[column_name] <= upper_limit)]

data_cleaned = data.copy()

for column in data:
    plt.figure(figsize=(8, 4))
    sns.boxplot(data_cleaned[column])
    plt.title(f'Boxplot de {column} (Before removing outliers)')
    plt.xlabel(column)
    plt.show()
    
    data_cleaned = remove_outliers(data_cleaned, column)
    
    plt.figure(figsize=(8, 4))
    sns.boxplot(data_cleaned[column])
    plt.title(f'Boxplot de {column} (After removing outliers)')
    plt.xlabel(column)
    plt.show()

```


    
![png](README_files/README_20_0.png)
    



    
![png](README_files/README_20_1.png)
    



    
![png](README_files/README_20_2.png)
    



    
![png](README_files/README_20_3.png)
    



    
![png](README_files/README_20_4.png)
    



    
![png](README_files/README_20_5.png)
    



    
![png](README_files/README_20_6.png)
    



    
![png](README_files/README_20_7.png)
    



    
![png](README_files/README_20_8.png)
    



    
![png](README_files/README_20_9.png)
    



    
![png](README_files/README_20_10.png)
    



    
![png](README_files/README_20_11.png)
    



    
![png](README_files/README_20_12.png)
    



    
![png](README_files/README_20_13.png)
    



    
![png](README_files/README_20_14.png)
    



    
![png](README_files/README_20_15.png)
    



    
![png](README_files/README_20_16.png)
    



    
![png](README_files/README_20_17.png)
    



    
![png](README_files/README_20_18.png)
    



    
![png](README_files/README_20_19.png)
    



    
![png](README_files/README_20_20.png)
    



    
![png](README_files/README_20_21.png)
    



    
![png](README_files/README_20_22.png)
    



    
![png](README_files/README_20_23.png)
    



```python

```

We can see below that we have a cleaner dataset


```python
data_cleaned.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CO(GT)</th>
      <th>PT08.S1(CO)</th>
      <th>C6H6(GT)</th>
      <th>PT08.S2(NMHC)</th>
      <th>NOx(GT)</th>
      <th>PT08.S3(NOx)</th>
      <th>NO2(GT)</th>
      <th>PT08.S4(NO2)</th>
      <th>PT08.S5(O3)</th>
      <th>T</th>
      <th>RH</th>
      <th>AH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
      <td>6084.00000</td>
      <td>6084.000000</td>
      <td>6084.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1.929635</td>
      <td>1088.931953</td>
      <td>9.359895</td>
      <td>924.304569</td>
      <td>208.434418</td>
      <td>824.830375</td>
      <td>108.022847</td>
      <td>1430.520874</td>
      <td>997.731262</td>
      <td>18.36453</td>
      <td>47.919001</td>
      <td>1.000566</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.062334</td>
      <td>179.633917</td>
      <td>5.697361</td>
      <td>218.738612</td>
      <td>140.166830</td>
      <td>197.013242</td>
      <td>39.858664</td>
      <td>329.220010</td>
      <td>327.732870</td>
      <td>8.94417</td>
      <td>17.461237</td>
      <td>0.404146</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.100000</td>
      <td>667.000000</td>
      <td>0.500000</td>
      <td>440.000000</td>
      <td>2.000000</td>
      <td>360.000000</td>
      <td>2.000000</td>
      <td>601.000000</td>
      <td>288.000000</td>
      <td>-1.90000</td>
      <td>9.200000</td>
      <td>0.184700</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1.100000</td>
      <td>953.000000</td>
      <td>4.800000</td>
      <td>755.000000</td>
      <td>101.000000</td>
      <td>681.000000</td>
      <td>79.000000</td>
      <td>1192.000000</td>
      <td>751.000000</td>
      <td>11.90000</td>
      <td>34.200000</td>
      <td>0.711675</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1.700000</td>
      <td>1066.000000</td>
      <td>8.200000</td>
      <td>909.000000</td>
      <td>173.000000</td>
      <td>802.000000</td>
      <td>106.000000</td>
      <td>1446.000000</td>
      <td>972.000000</td>
      <td>17.80000</td>
      <td>47.800000</td>
      <td>0.972750</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2.600000</td>
      <td>1206.000000</td>
      <td>13.000000</td>
      <td>1083.000000</td>
      <td>285.000000</td>
      <td>948.000000</td>
      <td>133.250000</td>
      <td>1663.000000</td>
      <td>1227.000000</td>
      <td>24.50000</td>
      <td>61.300000</td>
      <td>1.274250</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5.600000</td>
      <td>1657.000000</td>
      <td>27.700000</td>
      <td>1497.000000</td>
      <td>629.000000</td>
      <td>1389.000000</td>
      <td>219.000000</td>
      <td>2367.000000</td>
      <td>1945.000000</td>
      <td>43.40000</td>
      <td>88.700000</td>
      <td>2.119500</td>
    </tr>
  </tbody>
</table>
</div>



Heatmaps are useful to discorver relationships between variables. So lets plot one.


```python
correlation_matrix = data_cleaned[data_cleaned.columns].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Matrix")
plt.show()
```


    
![png](README_files/README_25_0.png)
    


## Training the model

With the cleaning steps ready, we can start thinking on how we can train this dataset to generate a model for our solution.  The reference variables will be the groundtruths for CO, NOx and NO2, and we remove all the Grountruths from the training set.


```python
X = data_cleaned.drop(['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)'], axis=1)
y = data_cleaned[['CO(GT)','NOx(GT)', 'NO2(GT)']]  # Variáveis GT como referência

X.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PT08.S1(CO)</th>
      <th>PT08.S2(NMHC)</th>
      <th>PT08.S3(NOx)</th>
      <th>PT08.S4(NO2)</th>
      <th>PT08.S5(O3)</th>
      <th>T</th>
      <th>RH</th>
      <th>AH</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1360.0</td>
      <td>1046.0</td>
      <td>1056.0</td>
      <td>1692.0</td>
      <td>1268.0</td>
      <td>13.6</td>
      <td>48.9</td>
      <td>0.7578</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1292.0</td>
      <td>955.0</td>
      <td>1174.0</td>
      <td>1559.0</td>
      <td>972.0</td>
      <td>13.3</td>
      <td>47.7</td>
      <td>0.7255</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1402.0</td>
      <td>939.0</td>
      <td>1140.0</td>
      <td>1555.0</td>
      <td>1074.0</td>
      <td>11.9</td>
      <td>54.0</td>
      <td>0.7502</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1376.0</td>
      <td>948.0</td>
      <td>1092.0</td>
      <td>1584.0</td>
      <td>1203.0</td>
      <td>11.0</td>
      <td>60.0</td>
      <td>0.7867</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1272.0</td>
      <td>836.0</td>
      <td>1205.0</td>
      <td>1490.0</td>
      <td>1110.0</td>
      <td>11.2</td>
      <td>59.6</td>
      <td>0.7888</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

The goal is to predict continuous values (pollutant concentrations), which is intrinsically a regression problem. Linear Regression is one of the most fundamental techniques for regression problems. Also, Linear Regression is simple, easy to implement and interpret. You can easily understand the relationship between the independent and dependent variables by looking at the model coefficients.So, lets go with LR for this sample.


```python
# Treinar modelo
model = LinearRegression()
model.fit(X_train, y_train)
```
Based on pollutant predictions, we can calculate an air quality index (AQI) and categorize this AQI into different levels. Just for the sake of simplicity, we will just calculate the mean of all values predicted by our model.


```python
#We define a simple AQI function
def calculate_aqi(concentrations):
    aqi = concentrations.mean(axis=1)
    return aqi

#We define here a simple categorize function based on the international range

def categorize_aqi(aqi):
    if aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Moderate'
    elif aqi <= 150:
        return 'Bad for sensible groups'
    elif aqi <= 200:
        return 'Bad'
    elif aqi <= 300:
        return 'Very bad'
    else:
        return 'Dangerous'
```

No we can use the model to predict the test values. And we can still calculate metrics such as MSE.


```python
# Prever concentrações de poluentes
predicted_concentrations = model.predict(X_test)

# Calcular AQI a partir de previsões de poluentes
predicted_aqi = calculate_aqi(pd.DataFrame(predicted_concentrations, columns=['CO(GT)','NOx(GT)', 'NO2(GT)']))

# Avaliar o modelo (opcional)
mse = mean_squared_error(y_test, predicted_concentrations)
print(f'Mean Squared Error: {mse}')
```

    Mean Squared Error: 1167.3460143391228


Finally, we can give the model some inputs for testing it:


```python
user_input = {
    'PT08.S1(CO)': 1360,
    'PT08.S2(NMHC)': 1046,
    'PT08.S3(NOx)': 1056,
    'PT08.S4(NO2)': 1692,
    'PT08.S5(O3)': 1268,
    'T': 21.6,
    'RH': 13.6,
    'AH': 0.76
}

good_air_quality_input = {
    'PT08.S1(CO)': 700,  # Supondo baixas concentrações de monóxido de carbono
    'PT08.S2(NMHC)': 400,
    'PT08.S3(NOx)': 1450,
    'PT08.S4(NO2)': 900,
    'PT08.S5(O3)': 500,  # Supondo baixas concentrações de ozônio
    'T': 20.0,          # Temperatura em graus Celsius
    'RH': 50.0,         # Umidade relativa em percentagem
    'AH': 0.8           # Concentração absoluta de umidade
}

# Exemplo de entrada para qualidade do ar ruim
bad_air_quality_input = {
    'PT08.S1(CO)': 1500,
    'PT08.S2(NMHC)': 1100,
    'PT08.S3(NOx)': 850,
    'PT08.S4(NO2)': 1700,
    'PT08.S5(O3)': 1400,
    'T': 30.0,
    'RH': 70.0,
    'AH': 1.3
}

# Exemplo de entrada para qualidade do ar muito ruim
very_bad_air_quality_input = {
    'PT08.S1(CO)': 2000,
    'PT08.S2(NMHC)': 1500,
    'PT08.S3(NOx)': 550,
    'PT08.S4(NO2)': 2200,
    'PT08.S5(O3)': 2200,
    'T': 35.0,
    'RH': 80.0,
    'AH': 1.8
}

# Converte o input do usuário em um DataFrame
user_input_df = pd.DataFrame([user_input])
user_input_gd = pd.DataFrame([good_air_quality_input])
user_input_bd = pd.DataFrame([bad_air_quality_input])
user_input_vb = pd.DataFrame([very_bad_air_quality_input])

# Agora você pode usar o modelo para fazer previsões com esse input
user_predicted_concentrations = model.predict(user_input_df)
user_predicted_aqi = calculate_aqi(pd.DataFrame(user_predicted_concentrations, columns=['CO(GT)','NOx(GT)', 'NO2(GT)']))

# Agora você pode usar o modelo para fazer previsões com esse input
user_predicted_concentrations_good = model.predict(user_input_gd)
user_predicted_aqi_good = calculate_aqi(pd.DataFrame(user_predicted_concentrations_good, columns=['CO(GT)','NOx(GT)', 'NO2(GT)']))

# Agora você pode usar o modelo para fazer previsões com esse input
user_predicted_concentrations_bad = model.predict(user_input_bd)
user_predicted_aqi_bad = calculate_aqi(pd.DataFrame(user_predicted_concentrations_bad, columns=['CO(GT)','NOx(GT)', 'NO2(GT)']))

# Agora você pode usar o modelo para fazer previsões com esse input
user_predicted_concentrations_vb = model.predict(user_input_vb)
user_predicted_aqi_vb = calculate_aqi(pd.DataFrame(user_predicted_concentrations_vb, columns=['CO(GT)','NOx(GT)', 'NO2(GT)']))

print(f'Predicted AQI for user input: {categorize_aqi(user_predicted_aqi.values[0])}')
print(f'Predicted AQI for user input good: {categorize_aqi(user_predicted_aqi_good.values[0])}')
print(f'Predicted AQI for user input bad: {categorize_aqi(user_predicted_aqi_bad.values[0])}')
print(f'Predicted AQI for user input very bad: {categorize_aqi(user_predicted_aqi_vb.values[0])}')

```

    Predicted AQI for user input: Moderate
    Predicted AQI for user input good: Good
    Predicted AQI for user input bad: Bad
    Predicted AQI for user input very bad: Very bad


This model could be more refined and some aspects of the AQI calculation could be defined a more refined equation, but for the sake of this project this if enough for now.


```python

```
