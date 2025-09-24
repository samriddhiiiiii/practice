import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class TrafficPredictor:
    """AI-based traffic prediction using machine learning"""
    
    def __init__(self):
        self.models = {}
        self.feature_columns = [
            'hour', 'minute', 'day_of_week', 'is_weekend',
            'vehicle_count', 'average_speed', 'congestion_level',
            'weather_factor', 'event_factor'
        ]
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize ML models for each traffic point"""
        from config.config import Config
        
        for point_id in Config.MAJOR_TRAFFIC_POINTS.keys():
            # Use Random Forest for better performance with limited data
            self.models[point_id] = {
                'timing_model': RandomForestRegressor(n_estimators=50, random_state=42),
                'congestion_model': RandomForestRegressor(n_estimators=30, random_state=42),
                'trained': False
            }
    
    def generate_training_data(self, point_id, days=30):
        """Generate synthetic training data for initial model training"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        # Generate hourly data for the specified period
        for i in range(days * 24):
            current_time = start_date + timedelta(hours=i)
            
            # Create realistic traffic patterns
            hour = current_time.hour
            day_of_week = current_time.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            
            # Peak hours: 8-10 AM and 6-8 PM on weekdays
            if not is_weekend and ((8 <= hour <= 10) or (18 <= hour <= 20)):
                base_vehicle_count = random.randint(200, 400)
                congestion_multiplier = random.uniform(2.0, 3.5)
            elif not is_weekend and (7 <= hour <= 9) or (17 <= hour <= 19):
                base_vehicle_count = random.randint(150, 300)
                congestion_multiplier = random.uniform(1.5, 2.5)
            elif is_weekend and (10 <= hour <= 22):
                base_vehicle_count = random.randint(100, 200)
                congestion_multiplier = random.uniform(1.0, 2.0)
            else:
                base_vehicle_count = random.randint(50, 150)
                congestion_multiplier = random.uniform(0.5, 1.5)
            
            # Add some randomness
            vehicle_count = int(base_vehicle_count * random.uniform(0.8, 1.2))
            average_speed = max(10, 50 - (congestion_multiplier * 10) + random.uniform(-5, 5))
            congestion_level = min(100, congestion_multiplier * 25 + random.uniform(-10, 10))
            
            # Weather and event factors
            weather_factor = random.uniform(0.8, 1.2)  # 1.0 = normal weather
            event_factor = random.uniform(0.9, 1.1)   # 1.0 = no special events
            
            # Optimal signal timings (what we want to predict)
            green_duration = self._calculate_optimal_green_time(
                vehicle_count, congestion_level, hour, is_weekend
            )
            red_duration = self._calculate_optimal_red_time(
                vehicle_count, congestion_level, hour, is_weekend
            )
            
            data.append({
                'hour': hour,
                'minute': current_time.minute,
                'day_of_week': day_of_week,
                'is_weekend': is_weekend,
                'vehicle_count': vehicle_count,
                'average_speed': average_speed,
                'congestion_level': congestion_level,
                'weather_factor': weather_factor,
                'event_factor': event_factor,
                'optimal_green_duration': green_duration,
                'optimal_red_duration': red_duration,
                'predicted_congestion': congestion_level * 1.1  # Slight increase for future prediction
            })
        
        return pd.DataFrame(data)
    
    def _calculate_optimal_green_time(self, vehicle_count, congestion_level, hour, is_weekend):
        """Calculate optimal green light duration based on traffic conditions"""
        base_green = 45  # Default green time
        
        # Adjust based on vehicle count
        if vehicle_count > 300:
            base_green += 20
        elif vehicle_count > 200:
            base_green += 10
        elif vehicle_count < 100:
            base_green -= 10
        
        # Adjust based on congestion
        if congestion_level > 70:
            base_green += 15
        elif congestion_level > 50:
            base_green += 10
        
        # Peak hour adjustments
        if not is_weekend and ((8 <= hour <= 10) or (18 <= hour <= 20)):
            base_green += 10
        
        return max(30, min(90, base_green))  # Keep between 30-90 seconds
    
    def _calculate_optimal_red_time(self, vehicle_count, congestion_level, hour, is_weekend):
        """Calculate optimal red light duration based on cross-traffic"""
        base_red = 60  # Default red time
        
        # Adjust based on conditions (inverse relationship with main road traffic)
        if vehicle_count > 300:
            base_red -= 10  # Less red time for heavy main road traffic
        elif vehicle_count < 100:
            base_red += 10  # More red time for light main road traffic
        
        # Night time adjustments
        if hour < 6 or hour > 22:
            base_red -= 15
        
        return max(20, min(80, base_red))  # Keep between 20-80 seconds
    
    def train_models(self, point_id):
        """Train the ML models for a specific traffic point"""
        try:
            # Generate training data
            training_data = self.generate_training_data(point_id)
            
            # Prepare features and targets
            X = training_data[self.feature_columns]
            y_timing = training_data[['optimal_green_duration', 'optimal_red_duration']]
            y_congestion = training_data['predicted_congestion']
            
            # Train timing prediction model
            self.models[point_id]['timing_model'].fit(X, y_timing)
            
            # Train congestion prediction model
            self.models[point_id]['congestion_model'].fit(X, y_congestion)
            
            self.models[point_id]['trained'] = True
            
            print(f"Models trained successfully for {point_id}")
            
        except Exception as e:
            print(f"Error training models for {point_id}: {e}")
    
    def predict_optimal_timing(self, point_id, current_traffic_data):
        """Predict optimal traffic signal timing"""
        try:
            if not self.models[point_id]['trained']:
                self.train_models(point_id)
            
            # Prepare current features
            now = datetime.now()
            features = self._prepare_features(now, current_traffic_data)
            
            if features is None:
                # Return default values if features can't be prepared
                return {
                    'green_duration': 45,
                    'red_duration': 60,
                    'confidence': 0.5
                }
            
            # Make prediction
            timing_prediction = self.models[point_id]['timing_model'].predict([features])[0]
            congestion_prediction = self.models[point_id]['congestion_model'].predict([features])[0]
            
            # Apply some business logic to ensure reasonable values
            green_duration = max(30, min(90, int(timing_prediction[0])))
            red_duration = max(20, min(80, int(timing_prediction[1])))
            
            # Calculate confidence based on model variance
            confidence = min(0.95, max(0.6, 1.0 - (abs(congestion_prediction - features[6]) / 100)))
            
            return {
                'green_duration': green_duration,
                'red_duration': red_duration,
                'predicted_congestion': congestion_prediction,
                'confidence': confidence
            }
            
        except Exception as e:
            print(f"Error predicting optimal timing for {point_id}: {e}")
            return {
                'green_duration': 45,
                'red_duration': 60,
                'confidence': 0.5
            }
    
    def _prepare_features(self, timestamp, traffic_data):
        """Prepare feature vector from current data"""
        try:
            hour = timestamp.hour
            minute = timestamp.minute
            day_of_week = timestamp.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            
            # Extract traffic data or use defaults
            vehicle_count = traffic_data.get('vehicle_count', 150)
            average_speed = traffic_data.get('average_speed', 35)
            congestion_level = traffic_data.get('congestion_level', 40)
            weather_factor = traffic_data.get('weather_factor', 1.0)
            event_factor = traffic_data.get('event_factor', 1.0)
            
            return [
                hour, minute, day_of_week, is_weekend,
                vehicle_count, average_speed, congestion_level,
                weather_factor, event_factor
            ]
            
        except Exception as e:
            print(f"Error preparing features: {e}")
            return None
    
    def save_models(self, filepath):
        """Save trained models to disk"""
        try:
            joblib.dump(self.models, filepath)
            print(f"Models saved to {filepath}")
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def load_models(self, filepath):
        """Load trained models from disk"""
        try:
            if os.path.exists(filepath):
                self.models = joblib.load(filepath)
                print(f"Models loaded from {filepath}")
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def get_model_performance(self):
        """Get performance metrics for all models"""
        performance = {}
        for point_id, model_data in self.models.items():
            if model_data['trained']:
                # Generate test data
                test_data = self.generate_training_data(point_id, days=7)
                X_test = test_data[self.feature_columns]
                y_test = test_data[['optimal_green_duration', 'optimal_red_duration']]
                
                # Calculate accuracy
                predictions = model_data['timing_model'].predict(X_test)
                mse = np.mean((predictions - y_test) ** 2)
                accuracy = max(0, 1 - (mse / 1000))  # Normalize MSE to accuracy
                
                performance[point_id] = {
                    'accuracy': accuracy,
                    'mse': mse,
                    'trained': True
                }
            else:
                performance[point_id] = {
                    'accuracy': 0,
                    'mse': float('inf'),
                    'trained': False
                }
        
        return performance