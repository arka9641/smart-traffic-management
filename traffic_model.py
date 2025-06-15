import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load

class TrafficPredictor:
    def __init__(self):
        self.model = RandomForestRegressor()
        
    def train(self, historical_data):
        # Preprocess data
        X = historical_data[['hour', 'day_of_week', 'vehicle_count']]
        y = historical_data['avg_speed']
        self.model.fit(X, y)
        dump(self.model, 'traffic_model.joblib')
    
    def predict_congestion(self, current_conditions):
        model = load('traffic_model.joblib')
        return model.predict([current_conditions])