import polars as pl
from functime.forecasting import linear_model

# Create a dummy time series
data = {
    "entity": ["A"] * 10 + ["B"] * 10,
    "time": list(range(10)) * 2,
    "value": [i * 0.5 for i in range(10)] + [i * 1.2 for i in range(10)],
}
y = pl.DataFrame(data)

# Initialize and fit a simple linear model forecaster
forecaster = linear_model(freq="1", lags=2)
forecaster.fit(y=y)

# Predict the next 2 steps
y_pred = forecaster.predict(fh=2)

print("Local installation test successful!")
print("Predicted values:")
print(y_pred)
