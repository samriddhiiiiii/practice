import random
import math
from datetime import datetime, timedelta
from config.config import Config

class TrafficSimulator:
    """Simulates realistic traffic data for the Bangalore traffic management system"""
    
    def __init__(self):
        self.baseline_commute_times = {}
        self.current_commute_times = {}
        self.system_start_time = datetime.now()
        self.initialize_baseline_commute_times()
    
    def initialize_baseline_commute_times(self):
        """Initialize baseline commute times for major routes"""
        # Baseline commute times between major points (in minutes)
        self.baseline_commute_times = {
            'silk_board_to_electronic_city': 25,
            'hebbal_to_marathahalli': 45,
            'koramangala_to_whitefield': 55,
            'majestic_to_silk_board': 35,
            'electronic_city_to_koramangala': 40,
            'whitefield_to_hebbal': 50,
            'jayanagar_to_richmond_circle': 20,
            'richmond_circle_to_majestic': 15
        }
        
        # Initialize current times as baseline
        self.current_commute_times = self.baseline_commute_times.copy()
    
    def generate_traffic_data(self):
        """Generate realistic traffic data for all monitoring points"""
        traffic_data = {}
        
        for point_id, point_info in Config.MAJOR_TRAFFIC_POINTS.items():
            traffic_data[point_id] = self._generate_point_data(point_id, point_info)
        
        return traffic_data
    
    def _generate_point_data(self, point_id, point_info):
        """Generate traffic data for a specific point"""
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()
        is_weekend = day_of_week >= 5
        
        # Base vehicle count from config
        base_vehicles_per_minute = point_info['avg_vehicles_per_hour'] / 60
        
        # Apply time-based patterns
        time_multiplier = self._get_time_multiplier(hour, is_weekend)
        
        # Apply day-of-week patterns
        day_multiplier = self._get_day_multiplier(day_of_week)
        
        # Add weather effects
        weather_factor = self._get_weather_factor()
        
        # Add special events (festivals, cricket matches, etc.)
        event_factor = self._get_event_factor(now)
        
        # Calculate final vehicle count
        vehicle_count = int(
            base_vehicles_per_minute * 
            time_multiplier * 
            day_multiplier * 
            weather_factor * 
            event_factor *
            random.uniform(0.85, 1.15)  # Random variation
        )
        
        # Calculate congestion level
        max_capacity = base_vehicles_per_minute * 3  # Peak capacity
        congestion_level = min(100, (vehicle_count / max_capacity) * 100)
        
        # Apply congestion penalty (exponential increase)
        if congestion_level > 70:
            congestion_level = 70 + (congestion_level - 70) * 1.5
        
        # Calculate average speed based on congestion
        average_speed = self._calculate_speed_from_congestion(congestion_level)
        
        # Calculate queue length
        queue_length = max(0, int((congestion_level - 50) * 0.5)) if congestion_level > 50 else 0
        
        # Calculate wait time
        wait_time = max(0, (congestion_level - 30) * 0.8) if congestion_level > 30 else 0
        
        return {
            'vehicle_count': vehicle_count,
            'congestion_level': round(congestion_level, 1),
            'average_speed': round(average_speed, 1),
            'queue_length': queue_length,
            'wait_time': round(wait_time, 1),
            'weather_factor': weather_factor,
            'event_factor': event_factor,
            'timestamp': now.isoformat(),
            'priority': point_info['priority']
        }
    
    def _get_time_multiplier(self, hour, is_weekend):
        """Get traffic multiplier based on time of day"""
        if not is_weekend:
            # Weekday patterns
            if hour in [8, 9]:  # Morning peak
                return random.uniform(3.5, 4.5)
            elif hour in [7, 10]:  # Pre/post morning peak
                return random.uniform(2.5, 3.5)
            elif hour in [17, 18, 19]:  # Evening peak
                return random.uniform(3.8, 5.0)
            elif hour in [16, 20]:  # Pre/post evening peak
                return random.uniform(2.8, 3.8)
            elif 11 <= hour <= 15:  # Daytime
                return random.uniform(1.5, 2.2)
            elif 21 <= hour <= 23:  # Late evening
                return random.uniform(1.0, 1.8)
            else:  # Night/early morning
                return random.uniform(0.3, 0.7)
        else:
            # Weekend patterns
            if 10 <= hour <= 22:  # Active hours
                return random.uniform(1.2, 2.8)
            elif hour in [23, 0, 1]:  # Late night social hours
                return random.uniform(0.8, 1.5)
            else:  # Quiet hours
                return random.uniform(0.2, 0.6)
    
    def _get_day_multiplier(self, day_of_week):
        """Get traffic multiplier based on day of week"""
        # Monday = 0, Sunday = 6
        multipliers = {
            0: 1.1,   # Monday (back to work)
            1: 1.0,   # Tuesday
            2: 1.0,   # Wednesday
            3: 1.0,   # Thursday
            4: 1.2,   # Friday (early weekend travel)
            5: 0.9,   # Saturday
            6: 0.8    # Sunday
        }
        return multipliers.get(day_of_week, 1.0)
    
    def _get_weather_factor(self):
        """Get traffic multiplier based on weather conditions"""
        # Simulate different weather conditions
        weather_conditions = {
            'clear': {'probability': 0.5, 'factor': 1.0},
            'light_rain': {'probability': 0.2, 'factor': 1.3},
            'heavy_rain': {'probability': 0.1, 'factor': 1.8},
            'cloudy': {'probability': 0.15, 'factor': 1.0},
            'foggy': {'probability': 0.05, 'factor': 1.4}
        }
        
        rand = random.random()
        cumulative = 0
        
        for condition, data in weather_conditions.items():
            cumulative += data['probability']
            if rand <= cumulative:
                return data['factor']
        
        return 1.0
    
    def _get_event_factor(self, timestamp):
        """Get traffic multiplier based on special events"""
        # Simulate special events that affect traffic
        
        # Festival periods (Diwali, Dussehra, etc.)
        if timestamp.month in [9, 10, 11] and random.random() < 0.1:
            return random.uniform(1.4, 2.0)
        
        # Cricket match days (especially India matches)
        if random.random() < 0.05:  # 5% chance of match day
            return random.uniform(0.7, 1.6)  # Can reduce or increase traffic
        
        # Tech conference/event days
        if timestamp.weekday() < 5 and random.random() < 0.03:  # Weekdays only
            return random.uniform(1.2, 1.8)
        
        # School holidays
        if timestamp.month in [5, 6, 12] and random.random() < 0.3:
            return random.uniform(0.8, 0.9)
        
        return 1.0
    
    def _calculate_speed_from_congestion(self, congestion_level):
        """Calculate average vehicle speed based on congestion level"""
        if congestion_level < 20:
            return random.uniform(45, 60)  # Free flow
        elif congestion_level < 40:
            return random.uniform(35, 50)  # Light traffic
        elif congestion_level < 60:
            return random.uniform(25, 40)  # Moderate traffic
        elif congestion_level < 80:
            return random.uniform(15, 30)  # Heavy traffic
        else:
            return random.uniform(5, 20)   # Stop-and-go
    
    def calculate_average_wait_time(self):
        """Calculate system-wide average wait time"""
        traffic_data = self.generate_traffic_data()
        
        total_wait_time = 0
        total_points = 0
        
        for point_data in traffic_data.values():
            total_wait_time += point_data['wait_time']
            total_points += 1
        
        if total_points == 0:
            return 0
        
        return round(total_wait_time / total_points, 2)
    
    def calculate_commute_reduction(self):
        """Calculate percentage reduction in commute time since system start"""
        # Simulate the impact of AI optimization over time
        hours_running = (datetime.now() - self.system_start_time).total_seconds() / 3600
        
        # Gradual improvement over time (learning effect)
        max_improvement = Config.TARGET_COMMUTE_REDUCTION
        learning_rate = 0.1  # 10% of max improvement per hour
        
        # Calculate improvement based on system runtime
        improvement_factor = 1 - math.exp(-learning_rate * hours_running)
        current_reduction = max_improvement * improvement_factor
        
        # Add some realistic variation
        current_reduction *= random.uniform(0.8, 1.2)
        
        # Cap at target reduction
        return min(max_improvement, max(0, current_reduction))
    
    def calculate_system_efficiency(self):
        """Calculate overall system efficiency percentage"""
        traffic_data = self.generate_traffic_data()
        
        efficiency_scores = []
        
        for point_id, point_data in traffic_data.items():
            # Efficiency based on congestion level (inverted)
            congestion_efficiency = max(0, (100 - point_data['congestion_level']) / 100)
            
            # Efficiency based on speed
            speed_efficiency = min(1.0, point_data['average_speed'] / 50)  # 50 km/h as ideal
            
            # Efficiency based on wait time
            wait_efficiency = max(0, (30 - point_data['wait_time']) / 30)  # 30 sec as max acceptable
            
            # Combined efficiency for this point
            point_efficiency = (congestion_efficiency + speed_efficiency + wait_efficiency) / 3
            efficiency_scores.append(point_efficiency)
        
        if not efficiency_scores:
            return 0
        
        # Calculate weighted average (high priority points have more weight)
        total_weight = 0
        weighted_efficiency = 0
        
        for point_id, efficiency in zip(traffic_data.keys(), efficiency_scores):
            priority = Config.MAJOR_TRAFFIC_POINTS[point_id]['priority']
            weight = {'high': 3, 'medium': 2, 'low': 1}[priority]
            
            weighted_efficiency += efficiency * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        system_efficiency = (weighted_efficiency / total_weight) * 100
        return round(system_efficiency, 1)
    
    def generate_historical_data(self, days=7):
        """Generate historical traffic data for analysis"""
        historical_data = []
        
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        current_time = start_time
        while current_time <= end_time:
            # Generate data for each point at this time
            for point_id, point_info in Config.MAJOR_TRAFFIC_POINTS.items():
                point_data = self._generate_point_data(point_id, point_info)
                point_data['timestamp'] = current_time.isoformat()
                point_data['point_id'] = point_id
                historical_data.append(point_data)
            
            # Move to next time interval (every 30 minutes)
            current_time += timedelta(minutes=30)
        
        return historical_data
    
    def simulate_route_optimization(self, from_point, to_point):
        """Simulate route optimization between two points"""
        # This would integrate with mapping APIs in a real system
        
        route_key = f"{from_point}_to_{to_point}"
        baseline_time = self.baseline_commute_times.get(route_key, 30)  # Default 30 min
        
        # Get current traffic conditions for route points
        traffic_data = self.generate_traffic_data()
        
        # Calculate route difficulty based on traffic conditions
        from_congestion = traffic_data.get(from_point, {}).get('congestion_level', 50)
        to_congestion = traffic_data.get(to_point, {}).get('congestion_level', 50)
        
        avg_congestion = (from_congestion + to_congestion) / 2
        
        # Apply congestion penalty to baseline time
        congestion_multiplier = 1 + (avg_congestion / 100)  # 1.0 to 2.0
        
        # Apply AI optimization benefit
        reduction = self.calculate_commute_reduction()
        optimization_multiplier = 1 - reduction
        
        current_time = baseline_time * congestion_multiplier * optimization_multiplier
        
        return {
            'route': route_key,
            'baseline_time_minutes': baseline_time,
            'current_time_minutes': round(current_time, 1),
            'time_saved_minutes': round(baseline_time - current_time, 1),
            'percentage_improvement': round(((baseline_time - current_time) / baseline_time) * 100, 1),
            'avg_congestion': round(avg_congestion, 1)
        }