#!/usr/bin/env python3
"""
Namma Traffic AI - Simple Web Application
A lightweight web app that works without heavy dependencies
Uses only the Python standard library with minimal Flask
"""

import json
import random
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class TrafficData:
    """Simple traffic data generator"""
    
    @staticmethod
    def get_traffic_points():
        return {
            'silk_board': {
                'name': 'Silk Board Junction',
                'priority': 'HIGH',
                'base_traffic': 350
            },
            'electronic_city': {
                'name': 'Electronic City Toll',
                'priority': 'HIGH',
                'base_traffic': 420
            },
            'hebbal': {
                'name': 'Hebbal Flyover',
                'priority': 'HIGH',
                'base_traffic': 380
            },
            'marathahalli': {
                'name': 'Marathahalli Bridge',
                'priority': 'MEDIUM',
                'base_traffic': 320
            },
            'whitefield': {
                'name': 'Whitefield Main Road',
                'priority': 'MEDIUM',
                'base_traffic': 280
            },
            'koramangala': {
                'name': 'Koramangala Junction',
                'priority': 'MEDIUM',
                'base_traffic': 290
            },
            'jayanagar': {
                'name': 'Jayanagar 4th Block',
                'priority': 'LOW',
                'base_traffic': 240
            },
            'richmond_circle': {
                'name': 'Richmond Circle',
                'priority': 'MEDIUM',
                'base_traffic': 260
            },
            'majestic': {
                'name': 'Majestic Bus Stand',
                'priority': 'HIGH',
                'base_traffic': 400
            }
        }
    
    @staticmethod
    def get_time_multiplier():
        hour = datetime.now().hour
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            return random.uniform(3.0, 4.5)
        elif 11 <= hour <= 16:
            return random.uniform(1.5, 2.5)
        elif 21 <= hour <= 23:
            return random.uniform(1.0, 1.8)
        else:
            return random.uniform(0.3, 0.8)
    
    @staticmethod
    def generate_current_data():
        points = TrafficData.get_traffic_points()
        multiplier = TrafficData.get_time_multiplier()
        result = {}
        
        for point_id, point_data in points.items():
            base = point_data['base_traffic']
            vehicles = int(base * multiplier * random.uniform(0.8, 1.2))
            congestion = min(95, (vehicles / base) * 100)
            
            if congestion < 30:
                speed = random.uniform(45, 60)
                signal_state = 'green'
                signal_time = 45
            elif congestion < 60:
                speed = random.uniform(25, 40)
                signal_state = 'green'
                signal_time = 60
            else:
                speed = random.uniform(10, 25)
                signal_state = 'red' if random.random() > 0.5 else 'yellow'
                signal_time = 75 if signal_state == 'green' else (60 if signal_state == 'red' else 5)
            
            result[point_id] = {
                'name': point_data['name'],
                'priority': point_data['priority'],
                'vehicles': vehicles,
                'congestion': round(congestion, 1),
                'speed': round(speed, 1),
                'signal_state': signal_state,
                'signal_time': signal_time
            }
        
        return result

class TrafficHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the traffic app"""
    
    def log_message(self, format, *args):
        """Override to reduce console noise"""
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_html()
        elif self.path == '/api/traffic':
            self.serve_api()
        elif self.path == '/api/stats':
            self.serve_stats()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Namma Traffic AI - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .traffic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .traffic-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .traffic-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .card-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }
        
        .priority-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .priority-HIGH { background: #ff6b6b; color: white; }
        .priority-MEDIUM { background: #feca57; color: #333; }
        .priority-LOW { background: #48dbfb; color: white; }
        
        .signal-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .traffic-light {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 15px;
            background: #2c3e50;
            border-radius: 15px;
        }
        
        .light {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #555;
            transition: all 0.3s;
        }
        
        .light.active-red { background: #ff4757; box-shadow: 0 0 20px #ff4757; }
        .light.active-yellow { background: #ffa502; box-shadow: 0 0 20px #ffa502; }
        .light.active-green { background: #2ed573; box-shadow: 0 0 20px #2ed573; }
        
        .signal-timer {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .metric {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        }
        
        .metric-label {
            display: block;
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-value {
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }
        
        .congestion-bar {
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .congestion-fill {
            height: 100%;
            background: linear-gradient(90deg, #2ed573 0%, #ffa502 50%, #ff4757 100%);
            transition: width 0.5s;
        }
        
        .update-time {
            text-align: center;
            color: white;
            margin-top: 20px;
            font-size: 0.9em;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .updating {
            animation: pulse 1s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚦 Namma Traffic AI</h1>
            <p>Smart Traffic Management System for Bangalore</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-label">Total Vehicles</div>
                <div class="stat-value" id="total-vehicles">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Average Congestion</div>
                <div class="stat-value" id="avg-congestion">0%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Average Speed</div>
                <div class="stat-value" id="avg-speed">0 km/h</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">System Status</div>
                <div class="stat-value" style="font-size: 1.8em;">🟢 ACTIVE</div>
            </div>
        </div>
        
        <div class="traffic-grid" id="traffic-grid"></div>
        
        <div class="update-time" id="update-time"></div>
    </div>
    
    <script>
        async function fetchTrafficData() {
            try {
                const response = await fetch('/api/traffic');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error fetching traffic data:', error);
            }
        }
        
        function updateDashboard(data) {
            const grid = document.getElementById('traffic-grid');
            grid.innerHTML = '';
            
            let totalVehicles = 0;
            let totalCongestion = 0;
            let totalSpeed = 0;
            let count = 0;
            
            for (const [pointId, pointData] of Object.entries(data)) {
                totalVehicles += pointData.vehicles;
                totalCongestion += pointData.congestion;
                totalSpeed += pointData.speed;
                count++;
                
                const card = createTrafficCard(pointId, pointData);
                grid.appendChild(card);
            }
            
            document.getElementById('total-vehicles').textContent = totalVehicles;
            document.getElementById('avg-congestion').textContent = 
                (totalCongestion / count).toFixed(1) + '%';
            document.getElementById('avg-speed').textContent = 
                (totalSpeed / count).toFixed(1) + ' km/h';
            
            document.getElementById('update-time').textContent = 
                'Last updated: ' + new Date().toLocaleTimeString();
        }
        
        function createTrafficCard(pointId, data) {
            const card = document.createElement('div');
            card.className = 'traffic-card';
            
            const signalStates = {
                'red': 'active-red',
                'yellow': 'active-yellow',
                'green': 'active-green'
            };
            
            card.innerHTML = `
                <div class="card-header">
                    <div class="card-title">${data.name}</div>
                    <div class="priority-badge priority-${data.priority}">${data.priority}</div>
                </div>
                
                <div class="signal-container">
                    <div class="traffic-light">
                        <div class="light ${data.signal_state === 'red' ? 'active-red' : ''}"></div>
                        <div class="light ${data.signal_state === 'yellow' ? 'active-yellow' : ''}"></div>
                        <div class="light ${data.signal_state === 'green' ? 'active-green' : ''}"></div>
                    </div>
                    <div class="signal-timer">${data.signal_time}s</div>
                </div>
                
                <div class="metrics">
                    <div class="metric">
                        <span class="metric-label">Vehicles</span>
                        <span class="metric-value">${data.vehicles}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Speed</span>
                        <span class="metric-value">${data.speed} km/h</span>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <span class="metric-label">Congestion Level</span>
                    <div class="congestion-bar">
                        <div class="congestion-fill" style="width: ${data.congestion}%"></div>
                    </div>
                    <div style="text-align: center; margin-top: 5px; font-weight: bold;">
                        ${data.congestion}%
                    </div>
                </div>
            `;
            
            return card;
        }
        
        // Initial fetch
        fetchTrafficData();
        
        // Auto-refresh every 5 seconds
        setInterval(fetchTrafficData, 5000);
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_api(self):
        """Serve traffic data API"""
        data = TrafficData.generate_current_data()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def serve_stats(self):
        """Serve statistics API"""
        data = TrafficData.generate_current_data()
        
        total_vehicles = sum(p['vehicles'] for p in data.values())
        avg_congestion = sum(p['congestion'] for p in data.values()) / len(data)
        avg_speed = sum(p['speed'] for p in data.values()) / len(data)
        
        stats = {
            'total_vehicles': total_vehicles,
            'avg_congestion': round(avg_congestion, 1),
            'avg_speed': round(avg_speed, 1),
            'monitoring_points': len(data),
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode())

def run_server(port=8000):
    """Run the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TrafficHandler)
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║     🚦 NAMMA TRAFFIC AI - Web Application Started 🚦         ║
╚═══════════════════════════════════════════════════════════════╝

✅ Server running on: http://localhost:{port}
✅ API endpoint: http://localhost:{port}/api/traffic
✅ Stats endpoint: http://localhost:{port}/api/stats

📊 Open your browser and navigate to: http://localhost:{port}

Press Ctrl+C to stop the server
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
        httpd.shutdown()
        print("✅ Server stopped successfully!\n")

if __name__ == '__main__':
    run_server(8000)
