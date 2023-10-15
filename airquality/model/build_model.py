# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import pandas as pd
import m2cgen as m2c 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import re


#
# DEFINES TRAINING DATA AND ALGORITHM FOR BUILDING THE MODEL
#

# - model algorithm
model = LinearRegression()

# - dataset for training the model
train_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6__hHU1bGI7oczcrZifx8gFp23DXMQLVu6o_7AgPhh0fwCyH8XhWR0IbZgoT26SAmnQZH9rYsU-xc/pub?gid=1720806244&single=true&output=csv"

#
# READS AND PREPARES DATA
#

# - reads data into a pandas dataframe
train_df = pd.read_csv(train_csv)
train_df = train_df.replace(-200, pd.NA).dropna()

numerical_columns = [
    'CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 'PT08.S2(NMHC)',
    'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)',
    'T', 'RH', 'AH'
]

for column in numerical_columns:
    train_df[column] = pd.to_numeric(train_df[column].astype(str).str.replace(',', '.'), errors='coerce')


# Converter colunas de data e hora para datetime
train_df['Datetime'] = pd.to_datetime(train_df['Date'] + ' ' + train_df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')

# Agora você pode descartar as colunas originais de data e hora, se desejar
train_df = train_df.drop(columns=['Date', 'Time'])

X = train_df.drop(['Datetime', 'CO(GT)', 'NMHC(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)'], axis=1)
y = train_df[['CO(GT)','NOx(GT)', 'NO2(GT)']]

# Dividir dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model.fit(X_train, y_train)

#
# EXPORTS MODEL
#

# - uses m2cgen to convert model to pure python code with zero dependencies
#   obs: generated Python code will define a method called `score(input)`, which computes
#        a numerical score based on an input list where each entry corresponds to one of
#        the model's input features/columns. If the dependent variable is a class with
#        more than 2 categories, then the output of the method will be a list of scores
#        for each category.
model_to_python = m2c.export_to_python(model)
# Removendo importação do numpy
# Remoção das importações e as conversões
# Remove a importação do numpy
model_to_python = model_to_python.replace("import numpy as np", "")
model_to_python = model_to_python.replace("np.asarray(", "")
model_to_python = model_to_python[:-1]

# - writes model to file `model.py` in the parent directory (m2cgen/backend)
with open("model.py", "w") as text_file:
    print(f"{model_to_python}", file=text_file)

print("Model exported successfully")

