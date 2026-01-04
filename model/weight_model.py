import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def predict_weight(df, target_days=7):
    """
    Predicts weight after 'target_days' based on calorie and weight history.
    """
    if len(df) < 3:  # Need at least 3 data points for a trend
        return None, "Need more data (at least 3 days) to predict."

    # Feature Engineering: Days since start and Net Calories
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
    df['net_calories'] = df['intake'] - df['burned']
    
    # Clean data (remove rows with missing weight)
    df = df.dropna(subset=['weight'])
    
    # Model Training
    # X = Days and Cumulative Net Calories, y = Weight
    X = df[['days_since_start', 'net_calories']]
    y = df['weight']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for future date
    future_day = df['days_since_start'].max() + target_days
    # Estimate net calories based on average of last 3 days
    avg_net_calories = df['net_calories'].tail(3).mean()
    
    prediction = model.predict([[future_day, avg_net_calories]])
    return round(prediction[0], 2), None