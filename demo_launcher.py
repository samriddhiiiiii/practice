#!/usr/bin/env python3
"""
Demo Launcher for Namma Traffic AI
Helps users choose which app to run
"""

import os
import sys
import subprocess

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    print("\n" + "="*70)
    print("   🚦 NAMMA TRAFFIC AI - Demo Launcher 🚦")
    print("   Smart Traffic Management System for Bangalore")
    print("="*70 + "\n")

def print_menu():
    print("Choose which application to run:\n")
    print("1. 📱 CLI Application (Terminal Dashboard)")
    print("   - Beautiful color-coded terminal interface")
    print("   - No dependencies required")
    print("   - Perfect for quick demos\n")
    
    print("2. 🌐 Simple Web Application")
    print("   - Stunning web dashboard with animations")
    print("   - No dependencies required")
    print("   - Opens in your browser\n")
    
    print("3. 🎯 Full Flask Application (Advanced)")
    print("   - Complete AI/ML features")
    print("   - Real-time WebSocket updates")
    print("   - Requires: pip install -r requirements.txt\n")
    
    print("4. ℹ️  Show Information")
    print("5. 🚪 Exit\n")

def run_cli_app():
    clear_screen()
    print("🚀 Starting CLI Application...\n")
    try:
        subprocess.run([sys.executable, "traffic_cli_app.py"])
    except KeyboardInterrupt:
        print("\n\n✅ CLI Application stopped.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

def run_web_app():
    clear_screen()
    print("🚀 Starting Web Application...\n")
    print("After it starts, open your browser to: http://localhost:8000\n")
    try:
        subprocess.run([sys.executable, "simple_web_app.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Web Application stopped.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

def run_flask_app():
    clear_screen()
    print("🚀 Starting Full Flask Application...\n")
    
    # Check if dependencies are installed
    try:
        import flask
        print("✅ Dependencies found!\n")
        print("After it starts, open your browser to: http://localhost:5000\n")
        subprocess.run([sys.executable, "app.py"])
    except ImportError:
        print("❌ Flask dependencies not installed!\n")
        print("Please run: pip install -r requirements.txt\n")
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\n✅ Flask Application stopped.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

def show_info():
    clear_screen()
    print_banner()
    print("📊 About Namma Traffic AI\n")
    print("This project includes THREE applications:\n")
    
    print("1. CLI Application (traffic_cli_app.py)")
    print("   ✓ Works immediately - no setup needed")
    print("   ✓ Beautiful terminal interface with colors")
    print("   ✓ Real-time traffic simulation")
    print("   ✓ Interactive menu system\n")
    
    print("2. Simple Web App (simple_web_app.py)")
    print("   ✓ Works immediately - no setup needed")
    print("   ✓ Gorgeous web interface")
    print("   ✓ Auto-refreshing dashboard")
    print("   ✓ Animated traffic lights")
    print("   ✓ RESTful API endpoints\n")
    
    print("3. Full Flask App (app.py)")
    print("   ✓ Complete ML/AI features")
    print("   ✓ Real-time WebSocket updates")
    print("   ✓ Computer vision integration")
    print("   ✓ Database storage")
    print("   ✓ Advanced analytics\n")
    
    print("📍 Monitored Locations:")
    print("   • Silk Board Junction (HIGH priority)")
    print("   • Electronic City Toll (HIGH priority)")
    print("   • Hebbal Flyover (HIGH priority)")
    print("   • Marathahalli Bridge (MEDIUM priority)")
    print("   • Whitefield Main Road (MEDIUM priority)")
    print("   • Koramangala Junction (MEDIUM priority)")
    print("   • Jayanagar 4th Block (LOW priority)")
    print("   • Richmond Circle (MEDIUM priority)")
    print("   • Majestic Bus Stand (HIGH priority)\n")
    
    print("🎯 Project Goals:")
    print("   • Reduce commute time by 10%")
    print("   • Real-time traffic monitoring")
    print("   • AI-based signal optimization")
    print("   • Smart congestion management\n")
    
    print("📖 For more details, see QUICKSTART.md\n")
    input("Press Enter to continue...")

def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                run_cli_app()
                input("\nPress Enter to return to menu...")
            elif choice == '2':
                run_web_app()
                input("\nPress Enter to return to menu...")
            elif choice == '3':
                run_flask_app()
                input("\nPress Enter to return to menu...")
            elif choice == '4':
                show_info()
            elif choice == '5':
                clear_screen()
                print("\n✅ Thank you for using Namma Traffic AI!\n")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except KeyboardInterrupt:
            clear_screen()
            print("\n\n✅ Thank you for using Namma Traffic AI!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()
