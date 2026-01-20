#!/usr/bin/env python3
"""
Namma Traffic AI - CLI Application
A simple command-line interface for the traffic management system
No external dependencies required!
"""

import random
import time
import os
from datetime import datetime

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class SimpleTrafficMonitor:
    """Lightweight traffic monitoring without external dependencies"""
    
    def __init__(self):
        self.traffic_points = {
            'Silk Board Junction': {'priority': 'HIGH', 'base_traffic': 350},
            'Electronic City Toll': {'priority': 'HIGH', 'base_traffic': 420},
            'Hebbal Flyover': {'priority': 'HIGH', 'base_traffic': 380},
            'Marathahalli Bridge': {'priority': 'MEDIUM', 'base_traffic': 320},
            'Whitefield Main Road': {'priority': 'MEDIUM', 'base_traffic': 280},
            'Koramangala Junction': {'priority': 'MEDIUM', 'base_traffic': 290},
            'Jayanagar 4th Block': {'priority': 'LOW', 'base_traffic': 240},
            'Richmond Circle': {'priority': 'MEDIUM', 'base_traffic': 260},
            'Majestic Bus Stand': {'priority': 'HIGH', 'base_traffic': 400},
        }
        self.signal_states = {}
        self.initialize_signals()
    
    def initialize_signals(self):
        """Initialize traffic signals"""
        for point in self.traffic_points:
            self.signal_states[point] = {
                'state': 'GREEN',
                'time_remaining': 45,
                'vehicles': random.randint(50, 100)
            }
    
    def get_time_multiplier(self):
        """Get traffic multiplier based on current time"""
        hour = datetime.now().hour
        if 8 <= hour <= 10 or 17 <= hour <= 20:  # Peak hours
            return random.uniform(3.0, 4.5)
        elif 11 <= hour <= 16:  # Day time
            return random.uniform(1.5, 2.5)
        elif 21 <= hour <= 23:  # Evening
            return random.uniform(1.0, 1.8)
        else:  # Night
            return random.uniform(0.3, 0.8)
    
    def update_traffic(self):
        """Update traffic conditions"""
        multiplier = self.get_time_multiplier()
        
        for point, data in self.traffic_points.items():
            base = data['base_traffic']
            vehicles = int(base * multiplier * random.uniform(0.8, 1.2))
            
            # Update signal state
            signal = self.signal_states[point]
            signal['time_remaining'] -= 1
            signal['vehicles'] = vehicles
            
            if signal['time_remaining'] <= 0:
                # Cycle through signals
                if signal['state'] == 'GREEN':
                    signal['state'] = 'YELLOW'
                    signal['time_remaining'] = 5
                elif signal['state'] == 'YELLOW':
                    signal['state'] = 'RED'
                    signal['time_remaining'] = 60
                else:
                    signal['state'] = 'GREEN'
                    # AI-based optimization: more vehicles = longer green
                    if vehicles > 300:
                        signal['time_remaining'] = 75
                    elif vehicles > 200:
                        signal['time_remaining'] = 60
                    else:
                        signal['time_remaining'] = 45
    
    def get_congestion_level(self, vehicles, base):
        """Calculate congestion level"""
        ratio = vehicles / base
        if ratio < 1.0:
            return 'LOW'
        elif ratio < 2.0:
            return 'MEDIUM'
        elif ratio < 3.0:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
    def get_signal_color(self, state):
        """Get colored signal indicator"""
        if state == 'RED':
            return f"{Colors.RED}●{Colors.END}"
        elif state == 'YELLOW':
            return f"{Colors.YELLOW}●{Colors.END}"
        else:  # GREEN
            return f"{Colors.GREEN}●{Colors.END}"
    
    def get_priority_color(self, priority):
        """Get colored priority badge"""
        if priority == 'HIGH':
            return f"{Colors.RED}{Colors.BOLD}{priority}{Colors.END}"
        elif priority == 'MEDIUM':
            return f"{Colors.YELLOW}{priority}{Colors.END}"
        else:
            return f"{Colors.GREEN}{priority}{Colors.END}"
    
    def display_dashboard(self):
        """Display the CLI dashboard"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║     🚦 NAMMA TRAFFIC AI - Smart Traffic Management 🚦       ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.END}")
        
        print(f"\n{Colors.BOLD}Current Time:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.BOLD}Target:{Colors.END} Reduce commute time by 10% across Bangalore\n")
        
        # Calculate system stats
        total_vehicles = sum(s['vehicles'] for s in self.signal_states.values())
        avg_vehicles = total_vehicles // len(self.signal_states)
        
        print(f"{Colors.BOLD}System Overview:{Colors.END}")
        print(f"  📊 Total Vehicles Monitored: {Colors.CYAN}{total_vehicles}{Colors.END}")
        print(f"  ⚡ Average Traffic Load: {Colors.CYAN}{avg_vehicles} vehicles/point{Colors.END}")
        print(f"  🎯 AI Optimization: {Colors.GREEN}ACTIVE{Colors.END}")
        
        print(f"\n{Colors.BOLD}Traffic Points Status:{Colors.END}\n")
        
        # Display each traffic point
        for i, (point, data) in enumerate(self.traffic_points.items(), 1):
            signal = self.signal_states[point]
            vehicles = signal['vehicles']
            base = data['base_traffic']
            
            congestion = self.get_congestion_level(vehicles, base)
            congestion_color = {
                'LOW': Colors.GREEN,
                'MEDIUM': Colors.YELLOW,
                'HIGH': Colors.RED,
                'CRITICAL': Colors.MAGENTA
            }.get(congestion, Colors.WHITE)
            
            signal_icon = self.get_signal_color(signal['state'])
            priority = self.get_priority_color(data['priority'])
            
            print(f"{i:2d}. {Colors.BOLD}{point:25s}{Colors.END} {signal_icon} "
                  f"[{signal['state']:6s}] {signal['time_remaining']:2d}s | "
                  f"🚗 {vehicles:3d} | "
                  f"{congestion_color}{congestion:8s}{Colors.END} | "
                  f"Priority: {priority}")
        
        print(f"\n{Colors.BOLD}Legend:{Colors.END} {Colors.GREEN}●{Colors.END} Green  "
              f"{Colors.YELLOW}●{Colors.END} Yellow  {Colors.RED}●{Colors.END} Red\n")
        
        print(f"{Colors.BOLD}Press Ctrl+C to exit{Colors.END}")
    
    def run(self):
        """Run the monitoring system"""
        print(f"\n{Colors.GREEN}Starting Namma Traffic AI CLI...{Colors.END}")
        time.sleep(1)
        
        try:
            while True:
                self.update_traffic()
                self.display_dashboard()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Shutting down Namma Traffic AI...{Colors.END}")
            print(f"{Colors.GREEN}Thank you for using our system!{Colors.END}\n")

def show_menu():
    """Show the main menu"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}     🚦 NAMMA TRAFFIC AI - Command Line Interface 🚦{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.END}\n")
    
    print(f"{Colors.BOLD}Smart Traffic Management System for Bangalore{Colors.END}\n")
    
    print(f"Select an option:\n")
    print(f"  {Colors.GREEN}1.{Colors.END} Live Traffic Monitoring Dashboard")
    print(f"  {Colors.GREEN}2.{Colors.END} View Traffic Statistics")
    print(f"  {Colors.GREEN}3.{Colors.END} About the System")
    print(f"  {Colors.GREEN}4.{Colors.END} Exit")
    
    choice = input(f"\n{Colors.CYAN}Enter your choice (1-4):{Colors.END} ")
    return choice

def show_statistics():
    """Show traffic statistics"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 Traffic Statistics{Colors.END}\n")
    
    print(f"{Colors.BOLD}System Performance Metrics:{Colors.END}\n")
    
    # Simulate some statistics
    reduction = random.uniform(7, 12)
    efficiency = random.uniform(75, 88)
    avg_wait = random.uniform(35, 55)
    
    print(f"  🎯 Commute Time Reduction: {Colors.GREEN}{reduction:.1f}%{Colors.END}")
    print(f"  ⚡ System Efficiency: {Colors.GREEN}{efficiency:.1f}%{Colors.END}")
    print(f"  ⏱️  Average Wait Time: {Colors.YELLOW}{avg_wait:.1f} seconds{Colors.END}")
    print(f"  🚗 Total Vehicles Today: {Colors.CYAN}{random.randint(45000, 65000)}{Colors.END}")
    print(f"  📍 Monitoring Points: {Colors.CYAN}9 major junctions{Colors.END}")
    
    print(f"\n{Colors.BOLD}Top Congestion Points Today:{Colors.END}\n")
    
    congestion_points = [
        ('Electronic City Toll', 87.3),
        ('Silk Board Junction', 84.6),
        ('Hebbal Flyover', 79.2)
    ]
    
    for i, (point, level) in enumerate(congestion_points, 1):
        color = Colors.RED if level > 80 else Colors.YELLOW
        print(f"  {i}. {point:25s} {color}{level:.1f}%{Colors.END}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def show_about():
    """Show about information"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"\n{Colors.CYAN}{Colors.BOLD}ℹ️  About Namma Traffic AI{Colors.END}\n")
    
    print(f"{Colors.BOLD}An AI-powered traffic management system for Bangalore{Colors.END}\n")
    
    print(f"Features:")
    print(f"  • Real-time traffic monitoring across 9 major junctions")
    print(f"  • AI-based signal optimization")
    print(f"  • Predictive congestion analysis")
    print(f"  • Target: 10% reduction in commute times\n")
    
    print(f"Technology Stack:")
    print(f"  • Python & Flask (Backend)")
    print(f"  • Machine Learning (Traffic Prediction)")
    print(f"  • Computer Vision (Vehicle Detection)")
    print(f"  • Real-time WebSocket Updates\n")
    
    print(f"Covered Locations:")
    print(f"  • Silk Board Junction")
    print(f"  • Electronic City Toll")
    print(f"  • Hebbal Flyover")
    print(f"  • Marathahalli Bridge")
    print(f"  • Whitefield Main Road")
    print(f"  • And 4 more major points\n")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def main():
    """Main application entry point"""
    print(f"\n{Colors.GREEN}Initializing Namma Traffic AI...{Colors.END}")
    time.sleep(0.5)
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            monitor = SimpleTrafficMonitor()
            monitor.run()
        elif choice == '2':
            show_statistics()
        elif choice == '3':
            show_about()
        elif choice == '4':
            print(f"\n{Colors.GREEN}Thank you for using Namma Traffic AI!{Colors.END}\n")
            break
        else:
            print(f"\n{Colors.RED}Invalid choice. Please try again.{Colors.END}")
            time.sleep(1)

if __name__ == '__main__':
    main()
