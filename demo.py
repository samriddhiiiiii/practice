#!/usr/bin/env python3
"""
Demo script for Namma Traffic AI system
Shows the system functionality without requiring a web browser
"""

import sys
import time
from datetime import datetime
from src.ai_models.traffic_predictor import TrafficPredictor
from src.data.traffic_simulator import TrafficSimulator
from src.traffic_analysis.traffic_monitor import TrafficMonitor
from config.config import Config

def demo_ai_prediction():
    """Demonstrate AI traffic prediction"""
    print("🤖 AI Traffic Prediction Demo")
    print("=" * 50)
    
    predictor = TrafficPredictor()
    simulator = TrafficSimulator()
    
    # Test predictions for major Bangalore locations
    locations = ['silk_board', 'electronic_city', 'hebbal']
    
    for location in locations:
        print(f"\n📍 Location: {Config.MAJOR_TRAFFIC_POINTS[location]['name']}")
        
        # Generate current traffic conditions
        current_data = {
            'vehicle_count': 250,
            'congestion_level': 65,
            'average_speed': 25
        }
        
        # Get AI prediction
        prediction = predictor.predict_optimal_timing(location, current_data)
        
        print(f"   Current: {current_data['vehicle_count']} vehicles, {current_data['congestion_level']}% congestion")
        print(f"   AI Recommendation: Green {prediction['green_duration']}s, Red {prediction['red_duration']}s")
        print(f"   Confidence: {prediction['confidence']:.1%}")

def demo_real_time_monitoring():
    """Demonstrate real-time traffic monitoring"""
    print("\n📡 Real-time Traffic Monitoring Demo")
    print("=" * 50)
    
    monitor = TrafficMonitor()
    simulator = TrafficSimulator()
    
    print("Monitoring traffic for 30 seconds...")
    
    for i in range(6):  # 6 iterations, 5 seconds each
        print(f"\n⏱️  Update {i+1}/6 - {datetime.now().strftime('%H:%M:%S')}")
        
        # Generate traffic data for all points
        traffic_data = simulator.generate_traffic_data()
        
        # Show top 3 congested areas
        sorted_points = sorted(
            traffic_data.items(), 
            key=lambda x: x[1]['congestion_level'], 
            reverse=True
        )[:3]
        
        for point_id, data in sorted_points:
            name = Config.MAJOR_TRAFFIC_POINTS[point_id]['name']
            print(f"   🚦 {name}: {data['vehicle_count']} vehicles, {data['congestion_level']:.1f}% congestion")
        
        time.sleep(5)

def demo_commute_reduction():
    """Demonstrate commute time reduction calculation"""
    print("\n📈 Commute Time Reduction Demo")
    print("=" * 50)
    
    simulator = TrafficSimulator()
    
    routes = [
        ('silk_board', 'electronic_city'),
        ('hebbal', 'marathahalli'),
        ('koramangala', 'whitefield')
    ]
    
    total_baseline = 0
    total_current = 0
    
    for from_point, to_point in routes:
        route_data = simulator.simulate_route_optimization(from_point, to_point)
        
        from_name = Config.MAJOR_TRAFFIC_POINTS[from_point]['name']
        to_name = Config.MAJOR_TRAFFIC_POINTS[to_point]['name']
        
        print(f"\n🛣️  Route: {from_name} → {to_name}")
        print(f"   Baseline time: {route_data['baseline_time_minutes']} minutes")
        print(f"   Current time: {route_data['current_time_minutes']} minutes")
        print(f"   Time saved: {route_data['time_saved_minutes']} minutes")
        print(f"   Improvement: {route_data['percentage_improvement']}%")
        
        total_baseline += route_data['baseline_time_minutes']
        total_current += route_data['current_time_minutes']
    
    overall_improvement = ((total_baseline - total_current) / total_baseline) * 100
    print(f"\n🎯 Overall System Performance:")
    print(f"   Total baseline time: {total_baseline} minutes")
    print(f"   Total current time: {total_current:.1f} minutes")
    print(f"   System-wide improvement: {overall_improvement:.1f}%")
    print(f"   Target achievement: {(overall_improvement / 10) * 100:.1f}% of 10% goal")

def demo_system_stats():
    """Show system statistics"""
    print("\n📊 System Statistics")
    print("=" * 50)
    
    simulator = TrafficSimulator()
    predictor = TrafficPredictor()
    
    # System efficiency
    efficiency = simulator.calculate_system_efficiency()
    print(f"System Efficiency: {efficiency}%")
    
    # Commute reduction
    reduction = simulator.calculate_commute_reduction() * 100
    print(f"Commute Time Reduction: {reduction:.1f}%")
    
    # Average wait time
    wait_time = simulator.calculate_average_wait_time()
    print(f"Average Wait Time: {wait_time:.1f} seconds")
    
    # Model performance
    model_performance = predictor.get_model_performance()
    trained_models = sum(1 for perf in model_performance.values() if perf['trained'])
    print(f"AI Models Active: {trained_models}/{len(model_performance)}")
    
    # Coverage
    print(f"Traffic Points Monitored: {len(Config.MAJOR_TRAFFIC_POINTS)}")
    print(f"Major Areas Covered:")
    for point_id, point_data in Config.MAJOR_TRAFFIC_POINTS.items():
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[point_data['priority']]
        print(f"   {priority_emoji} {point_data['name']} ({point_data['priority']} priority)")

def main():
    """Run the complete demo"""
    print("🚦 NAMMA TRAFFIC AI - Smart Traffic Management System")
    print("=" * 60)
    print("🏙️  Bangalore Smart City Initiative")
    print("🤖 AI-Powered Traffic Optimization")
    print("📱 Real-time Monitoring & Control")
    print("=" * 60)
    
    try:
        # Run all demos
        demo_ai_prediction()
        demo_real_time_monitoring()
        demo_commute_reduction()
        demo_system_stats()
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("🎯 Target: 10% commute time reduction")
        print("📊 System is operational and learning")
        print("🌐 Web dashboard available at: http://localhost:5000")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")

if __name__ == "__main__":
    main()