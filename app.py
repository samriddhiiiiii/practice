from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import random
import time
from datetime import datetime, timedelta
import threading
from config.config import Config
from src.traffic_analysis.traffic_monitor import TrafficMonitor
from src.ai_models.traffic_predictor import TrafficPredictor
from src.data.traffic_simulator import TrafficSimulator

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
traffic_monitor = TrafficMonitor()
traffic_predictor = TrafficPredictor()
traffic_simulator = TrafficSimulator()

# Global state
current_traffic_data = {}
signal_states = {}
system_stats = {
    'total_vehicles_processed': 0,
    'average_wait_time': 0,
    'commute_time_reduction': 0,
    'system_efficiency': 0
}

def initialize_signals():
    """Initialize all traffic signals to default state"""
    global signal_states
    for point_id, point_data in Config.MAJOR_TRAFFIC_POINTS.items():
        signal_states[point_id] = {
            'current_state': 'green',
            'time_remaining': Config.DEFAULT_SIGNAL_TIMINGS['green'],
            'auto_mode': True,
            'vehicles_waiting': random.randint(10, 50),
            'last_updated': datetime.now()
        }

def update_traffic_data():
    """Background task to update traffic data"""
    global current_traffic_data, system_stats
    
    while True:
        try:
            # Simulate real-time traffic data
            new_data = traffic_simulator.generate_traffic_data()
            current_traffic_data = new_data
            
            # Update system statistics
            system_stats['total_vehicles_processed'] += sum([data['vehicle_count'] for data in new_data.values()])
            system_stats['average_wait_time'] = traffic_simulator.calculate_average_wait_time()
            system_stats['commute_time_reduction'] = traffic_simulator.calculate_commute_reduction()
            system_stats['system_efficiency'] = traffic_simulator.calculate_system_efficiency()
            
            # Emit updates to connected clients
            socketio.emit('traffic_update', {
                'traffic_data': current_traffic_data,
                'system_stats': system_stats,
                'signal_states': signal_states
            })
            
            time.sleep(Config.DATA_REFRESH_INTERVAL)
            
        except Exception as e:
            print(f"Error updating traffic data: {e}")
            time.sleep(5)

def signal_controller():
    """Background task to manage traffic signals"""
    global signal_states
    
    while True:
        try:
            for point_id, signal in signal_states.items():
                if signal['auto_mode']:
                    # Get AI prediction for optimal timing
                    prediction = traffic_predictor.predict_optimal_timing(
                        point_id, 
                        current_traffic_data.get(point_id, {})
                    )
                    
                    # Update signal timing based on prediction
                    signal['time_remaining'] -= 1
                    
                    if signal['time_remaining'] <= 0:
                        # Cycle through traffic light states
                        if signal['current_state'] == 'green':
                            signal['current_state'] = 'yellow'
                            signal['time_remaining'] = Config.DEFAULT_SIGNAL_TIMINGS['yellow']
                        elif signal['current_state'] == 'yellow':
                            signal['current_state'] = 'red'
                            signal['time_remaining'] = prediction.get('red_duration', Config.DEFAULT_SIGNAL_TIMINGS['red'])
                        else:  # red
                            signal['current_state'] = 'green'
                            signal['time_remaining'] = prediction.get('green_duration', Config.DEFAULT_SIGNAL_TIMINGS['green'])
                    
                    signal['last_updated'] = datetime.now()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in signal controller: {e}")
            time.sleep(5)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html', 
                         traffic_points=Config.MAJOR_TRAFFIC_POINTS,
                         bangalore_coords=Config.BANGALORE_COORDINATES)

@app.route('/api/traffic-data')
def get_traffic_data():
    """API endpoint to get current traffic data"""
    return jsonify({
        'traffic_data': current_traffic_data,
        'signal_states': signal_states,
        'system_stats': system_stats,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/signal-control', methods=['POST'])
def control_signal():
    """API endpoint to manually control traffic signals"""
    data = request.json
    point_id = data.get('point_id')
    action = data.get('action')  # 'manual', 'auto', 'change_state'
    
    if point_id not in signal_states:
        return jsonify({'error': 'Invalid traffic point'}), 400
    
    if action == 'toggle_mode':
        signal_states[point_id]['auto_mode'] = not signal_states[point_id]['auto_mode']
    elif action == 'change_state' and not signal_states[point_id]['auto_mode']:
        new_state = data.get('state')
        if new_state in ['red', 'yellow', 'green']:
            signal_states[point_id]['current_state'] = new_state
            signal_states[point_id]['time_remaining'] = Config.DEFAULT_SIGNAL_TIMINGS[new_state]
    
    return jsonify({'success': True, 'signal_state': signal_states[point_id]})

@app.route('/api/analytics')
def get_analytics():
    """API endpoint to get traffic analytics"""
    analytics_data = traffic_monitor.get_analytics_data()
    return jsonify(analytics_data)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'data': 'Connected to Namma Traffic AI'})
    # Send initial data
    emit('traffic_update', {
        'traffic_data': current_traffic_data,
        'system_stats': system_stats,
        'signal_states': signal_states
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Initialize the system
    initialize_signals()
    
    # Start background tasks
    traffic_thread = threading.Thread(target=update_traffic_data)
    traffic_thread.daemon = True
    traffic_thread.start()
    
    signal_thread = threading.Thread(target=signal_controller)
    signal_thread.daemon = True
    signal_thread.start()
    
    print("Starting Namma Traffic AI System...")
    print("Dashboard will be available at: http://localhost:5000")
    
    # Run the Flask-SocketIO app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)