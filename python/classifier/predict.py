import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("/content/finals20.csv")
df = df[["vader", "secscore", "assoc", "perc"]]
print(df.head())

predictors = ['vader', 'assoc']
target = ['perc']
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_train = scaler.fit_transform(df)

print(df.columns.values)
print(type(scaled_train))
scaled_train_df = pd.DataFrame(scaled_train, columns=df.columns.values)
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dense(1))
model.compile(loss='mean_squared_error', optimizer='adamax')
X = scaled_train_df.drop(target, axis=1).values
Y = scaled_train_df[['perc']].values
# Train the model
model.fit(
    X[1:],
    Y[1:],
    epochs=200,
    shuffle=True,
    verbose=2
)
