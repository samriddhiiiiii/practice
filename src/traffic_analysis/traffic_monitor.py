try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

import numpy as np
from datetime import datetime, timedelta
import random
import json

class TrafficMonitor:
    """Computer vision-based traffic monitoring system"""
    
    def __init__(self):
        self.vehicle_cascade = None
        self.background_subtractor = None
        if CV2_AVAILABLE:
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.vehicle_count_history = {}
        self.initialize_vehicle_detection()
    
    def initialize_vehicle_detection(self):
        """Initialize vehicle detection models"""
        # In a real implementation, you would load pre-trained models
        # For simulation, we'll use basic computer vision techniques
        if CV2_AVAILABLE:
            self.vehicle_cascade = cv2.CascadeClassifier()
        
        # Initialize vehicle count history for all traffic points
        from config.config import Config
        for point_id in Config.MAJOR_TRAFFIC_POINTS.keys():
            self.vehicle_count_history[point_id] = []
    
    def analyze_traffic_image(self, image_path_or_array, point_id):
        """Analyze traffic from camera image using computer vision"""
        try:
            # In a real implementation, this would process actual camera feeds
            # For simulation, we'll return realistic traffic analysis data
            
            # Simulate vehicle detection
            vehicle_count = self._simulate_vehicle_detection(point_id)
            
            # Calculate traffic metrics
            congestion_level = self._calculate_congestion_level(vehicle_count, point_id)
            average_speed = self._estimate_average_speed(congestion_level)
            
            # Store in history
            timestamp = datetime.now()
            traffic_data = {
                'timestamp': timestamp,
                'vehicle_count': vehicle_count,
                'congestion_level': congestion_level,
                'average_speed': average_speed,
                'point_id': point_id
            }
            
            self.vehicle_count_history[point_id].append(traffic_data)
            
            # Keep only last 100 records
            if len(self.vehicle_count_history[point_id]) > 100:
                self.vehicle_count_history[point_id].pop(0)
            
            return traffic_data
            
        except Exception as e:
            print(f"Error analyzing traffic image for {point_id}: {e}")
            return self._get_default_traffic_data(point_id)
    
    def _simulate_vehicle_detection(self, point_id):
        """Simulate realistic vehicle detection based on time and location"""
        from config.config import Config
        
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()
        is_weekend = day_of_week >= 5
        
        # Get base vehicle count for this point
        base_count = Config.MAJOR_TRAFFIC_POINTS[point_id].get('avg_vehicles_per_hour', 2000) / 60
        
        # Apply time-based multipliers
        if not is_weekend:
            # Weekday patterns
            if 8 <= hour <= 10:  # Morning peak
                multiplier = random.uniform(2.5, 4.0)
            elif 17 <= hour <= 20:  # Evening peak
                multiplier = random.uniform(3.0, 4.5)
            elif 11 <= hour <= 16:  # Day time
                multiplier = random.uniform(1.2, 2.0)
            elif 21 <= hour <= 23:  # Late evening
                multiplier = random.uniform(0.8, 1.5)
            else:  # Night/early morning
                multiplier = random.uniform(0.3, 0.8)
        else:
            # Weekend patterns
            if 10 <= hour <= 22:  # Active hours
                multiplier = random.uniform(1.0, 2.5)
            else:  # Quiet hours
                multiplier = random.uniform(0.4, 1.0)
        
        # Add some randomness
        vehicle_count = int(base_count * multiplier * random.uniform(0.8, 1.2))
        
        return max(0, vehicle_count)
    
    def _calculate_congestion_level(self, vehicle_count, point_id):
        """Calculate congestion level (0-100) based on vehicle count"""
        from config.config import Config
        
        # Get the typical capacity for this point
        max_capacity = Config.MAJOR_TRAFFIC_POINTS[point_id].get('avg_vehicles_per_hour', 2000) / 60
        
        # Calculate congestion as percentage of capacity
        congestion = (vehicle_count / max_capacity) * 100
        
        # Apply non-linear scaling (congestion increases exponentially)
        if congestion > 80:
            congestion = 80 + (congestion - 80) * 2
        
        return min(100, max(0, congestion))
    
    def _estimate_average_speed(self, congestion_level):
        """Estimate average vehicle speed based on congestion"""
        # Speed decreases with congestion
        if congestion_level < 20:
            return random.uniform(40, 60)  # Free flow
        elif congestion_level < 40:
            return random.uniform(30, 45)  # Light traffic
        elif congestion_level < 60:
            return random.uniform(20, 35)  # Moderate traffic
        elif congestion_level < 80:
            return random.uniform(10, 25)  # Heavy traffic
        else:
            return random.uniform(5, 15)   # Stop-and-go
    
    def _get_default_traffic_data(self, point_id):
        """Return default traffic data when analysis fails"""
        return {
            'timestamp': datetime.now(),
            'vehicle_count': 50,
            'congestion_level': 30,
            'average_speed': 35,
            'point_id': point_id
        }
    
    def detect_traffic_incidents(self, point_id):
        """Detect traffic incidents using pattern analysis"""
        if point_id not in self.vehicle_count_history or len(self.vehicle_count_history[point_id]) < 10:
            return []
        
        incidents = []
        recent_data = self.vehicle_count_history[point_id][-10:]  # Last 10 readings
        
        # Check for sudden congestion increase
        congestion_levels = [data['congestion_level'] for data in recent_data]
        if len(congestion_levels) >= 5:
            recent_avg = sum(congestion_levels[-3:]) / 3
            previous_avg = sum(congestion_levels[-8:-3]) / 5
            
            if recent_avg > previous_avg + 30:  # Sudden 30% increase
                incidents.append({
                    'type': 'sudden_congestion',
                    'severity': 'high' if recent_avg > 80 else 'medium',
                    'timestamp': datetime.now(),
                    'description': f'Sudden congestion increase detected at {point_id}'
                })
        
        # Check for abnormally low speeds
        speeds = [data['average_speed'] for data in recent_data]
        if len(speeds) >= 3:
            avg_speed = sum(speeds[-3:]) / 3
            if avg_speed < 10:
                incidents.append({
                    'type': 'traffic_jam',
                    'severity': 'high',
                    'timestamp': datetime.now(),
                    'description': f'Severe traffic jam detected at {point_id} (avg speed: {avg_speed:.1f} km/h)'
                })
        
        return incidents
    
    def get_traffic_flow_analysis(self, point_id, hours=24):
        """Get traffic flow analysis for the specified time period"""
        if point_id not in self.vehicle_count_history:
            return {}
        
        # Filter data for the specified time period
        cutoff_time = datetime.now() - timedelta(hours=hours)
        relevant_data = [
            data for data in self.vehicle_count_history[point_id]
            if data['timestamp'] >= cutoff_time
        ]
        
        if not relevant_data:
            return {}
        
        # Calculate statistics
        vehicle_counts = [data['vehicle_count'] for data in relevant_data]
        congestion_levels = [data['congestion_level'] for data in relevant_data]
        speeds = [data['average_speed'] for data in relevant_data]
        
        analysis = {
            'period_hours': hours,
            'data_points': len(relevant_data),
            'vehicle_count': {
                'average': sum(vehicle_counts) / len(vehicle_counts),
                'max': max(vehicle_counts),
                'min': min(vehicle_counts)
            },
            'congestion_level': {
                'average': sum(congestion_levels) / len(congestion_levels),
                'max': max(congestion_levels),
                'min': min(congestion_levels)
            },
            'average_speed': {
                'average': sum(speeds) / len(speeds),
                'max': max(speeds),
                'min': min(speeds)
            },
            'peak_hours': self._identify_peak_hours(relevant_data)
        }
        
        return analysis
    
    def _identify_peak_hours(self, traffic_data):
        """Identify peak traffic hours from historical data"""
        hourly_congestion = {}
        
        for data in traffic_data:
            hour = data['timestamp'].hour
            if hour not in hourly_congestion:
                hourly_congestion[hour] = []
            hourly_congestion[hour].append(data['congestion_level'])
        
        # Calculate average congestion by hour
        hourly_averages = {
            hour: sum(levels) / len(levels)
            for hour, levels in hourly_congestion.items()
        }
        
        # Find top 3 peak hours
        sorted_hours = sorted(hourly_averages.items(), key=lambda x: x[1], reverse=True)
        peak_hours = sorted_hours[:3]
        
        return [{'hour': hour, 'avg_congestion': avg} for hour, avg in peak_hours]
    
    def get_analytics_data(self):
        """Get comprehensive analytics data for all traffic points"""
        analytics = {
            'timestamp': datetime.now().isoformat(),
            'traffic_points': {},
            'system_overview': {
                'total_monitoring_points': len(self.vehicle_count_history),
                'active_incidents': 0,
                'average_system_congestion': 0
            }
        }
        
        total_congestion = 0
        total_incidents = 0
        
        for point_id in self.vehicle_count_history.keys():
            # Get flow analysis
            flow_analysis = self.get_traffic_flow_analysis(point_id, hours=1)
            
            # Detect incidents
            incidents = self.detect_traffic_incidents(point_id)
            total_incidents += len(incidents)
            
            # Get current status
            current_data = self.vehicle_count_history[point_id][-1] if self.vehicle_count_history[point_id] else None
            
            analytics['traffic_points'][point_id] = {
                'current_status': current_data,
                'flow_analysis': flow_analysis,
                'incidents': incidents,
                'monitoring_active': True
            }
            
            if current_data:
                total_congestion += current_data['congestion_level']
        
        # Calculate system overview
        if len(self.vehicle_count_history) > 0:
            analytics['system_overview']['average_system_congestion'] = total_congestion / len(self.vehicle_count_history)
        analytics['system_overview']['active_incidents'] = total_incidents
        
        return analytics
    
    def process_video_feed(self, video_source, point_id):
        """Process live video feed for traffic monitoring"""
        # This would be used for real camera feeds
        # For simulation purposes, this returns mock data
        
        # In real implementation:
        # cap = cv2.VideoCapture(video_source)
        # while True:
        #     ret, frame = cap.read()
        #     if not ret:
        #         break
        #     traffic_data = self.analyze_traffic_image(frame, point_id)
        #     yield traffic_data
        
        # Simulation:
        while True:
            traffic_data = self.analyze_traffic_image(None, point_id)
            yield traffic_data