# -*- coding: utf-8 -*-
"""Maize Train.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ba96LW9BSe-TmaTRcOHM2lsfJmiA4RY4
"""

import pandas as pd

# Load data
data = pd.read_csv('/content/Food_Prices_Kenya.csv')

# Inspect data
print(data.head())
print(data.info())

# Fill any remaining missing values for numerical columns with mean or median
numeric_columns = data.select_dtypes(include=['number']).columns
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Inspect data after cleaning
print(data.head())
print(data.info())

# Check data types
print(data.dtypes)

# Convert columns as needed
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Extract month and year from the Date column
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year

# Drop original Date column if not needed
data.drop(columns=['Date'], inplace=True)

print(data.head())

# Extract month and year from the Date column (if 'Date' column still exists)
if 'Date' in data.columns:
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year

    # Drop original Date column if not needed
    data.drop(columns=['Date'], inplace=True)

print(data.head())

from sklearn.model_selection import train_test_split

# Select features and target variable
features = ['Month', 'Year', 'Regions', 'Annual Rainfall', 'Annual Temperature']
X = data[features]
y = data['Price']

# Convert categorical variables to dummy variables
X = pd.get_dummies(X, columns=['Regions'], drop_first=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Define the ANN model
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the model
history = model.fit(X_train, y_train, validation_split=0.2, epochs=50, batch_size=32)

# Evaluate the model
loss, mae = model.evaluate(X_test, y_test)
print(f"MAE: {mae}")

# Predict and evaluate the model
y_pred = model.predict(X_test)
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print(f"R-squared: {r2_score(y_test, y_pred)}")