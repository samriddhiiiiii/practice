import os
from datetime import datetime

class Config:
    """Application configuration settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'namma-traffic-ai-secret-key-2024'
    DEBUG = True
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///traffic_data.db'
    
    # AI Model settings
    MODEL_UPDATE_INTERVAL = 300  # 5 minutes
    PREDICTION_WINDOW = 1800  # 30 minutes ahead
    
    # Bangalore specific settings
    BANGALORE_COORDINATES = {
        'lat': 12.9716,
        'lng': 77.5946
    }
    
    # Major traffic points in Bangalore
    MAJOR_TRAFFIC_POINTS = {
        'silk_board': {
            'name': 'Silk Board Junction',
            'lat': 12.9178,
            'lng': 77.6229,
            'priority': 'high',
            'avg_vehicles_per_hour': 3500
        },
        'electronic_city': {
            'name': 'Electronic City Toll',
            'lat': 12.8399,
            'lng': 77.6773,
            'priority': 'high',
            'avg_vehicles_per_hour': 4200
        },
        'hebbal': {
            'name': 'Hebbal Flyover',
            'lat': 13.0358,
            'lng': 77.5970,
            'priority': 'high',
            'avg_vehicles_per_hour': 3800
        },
        'marathahalli': {
            'name': 'Marathahalli Bridge',
            'lat': 12.9591,
            'lng': 77.6974,
            'priority': 'medium',
            'avg_vehicles_per_hour': 3200
        },
        'whitefield': {
            'name': 'Whitefield Main Road',
            'lat': 12.9698,
            'lng': 77.7499,
            'priority': 'medium',
            'avg_vehicles_per_hour': 2800
        },
        'koramangala': {
            'name': 'Koramangala Junction',
            'lat': 12.9279,
            'lng': 77.6271,
            'priority': 'medium',
            'avg_vehicles_per_hour': 2900
        },
        'jayanagar': {
            'name': 'Jayanagar 4th Block',
            'lat': 12.9237,
            'lng': 77.5937,
            'priority': 'low',
            'avg_vehicles_per_hour': 2400
        },
        'richmond_circle': {
            'name': 'Richmond Circle',
            'lat': 12.9581,
            'lng': 77.6015,
            'priority': 'medium',
            'avg_vehicles_per_hour': 2600
        },
        'majestic': {
            'name': 'Majestic Bus Stand Area',
            'lat': 12.9767,
            'lng': 77.5710,
            'priority': 'high',
            'avg_vehicles_per_hour': 4000
        }
    }
    
    # Traffic signal timing settings
    DEFAULT_SIGNAL_TIMINGS = {
        'red': 60,    # seconds
        'yellow': 5,  # seconds
        'green': 45   # seconds
    }
    
    # Performance targets
    TARGET_COMMUTE_REDUCTION = 0.10  # 10% reduction
    
    # Update intervals
    DATA_REFRESH_INTERVAL = 30  # seconds
    AI_MODEL_RETRAIN_INTERVAL = 3600  # 1 hour