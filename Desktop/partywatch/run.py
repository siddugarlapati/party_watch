#!/usr/bin/env python3
"""
PartyWatch Startup Script
Run this script to start the PartyWatch application
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'websockets',
        'firebase-admin',
        'pytube',
        'fastapi',
        'uvicorn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        print("   pip install -r backend/requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🔧 Starting FastAPI backend server...")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting backend server: {e}")

def start_streamlit():
    """Start the Streamlit application"""
    print("🚀 Starting Streamlit application...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit application stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")

def start_websocket_server():
    """Start the WebSocket server"""
    print("🔌 Starting WebSocket server...")
    try:
        subprocess.run([sys.executable, "websocket_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 WebSocket server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting WebSocket server: {e}")

def main():
    """Main startup function"""
    print("🎬 PartyWatch - Shared YouTube Watch Rooms")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🔧 Choose startup mode:")
    print("1. Full application (Backend + Frontend)")
    print("2. Frontend only (Streamlit)")
    print("3. Backend only (FastAPI)")
    print("4. WebSocket server only")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting full PartyWatch application...")
                print("🔧 Backend API: http://localhost:8000")
                print("📱 Frontend: http://localhost:8501")
                print("🌐 WebSocket: ws://localhost:8765")
                
                # Start backend in a separate thread
                backend_thread = threading.Thread(target=start_backend, daemon=True)
                backend_thread.start()
                
                # Give backend time to start
                time.sleep(3)
                
                # Start WebSocket server in a separate thread
                websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
                websocket_thread.start()
                
                # Give WebSocket server time to start
                time.sleep(2)
                
                # Start Streamlit app
                start_streamlit()
                break
                
            elif choice == "2":
                print("\n🎯 Starting Streamlit frontend only...")
                print("📱 Open your browser to: http://localhost:8501")
                print("⚠️  Note: Backend API calls will fail without the backend running")
                start_streamlit()
                break
                
            elif choice == "3":
                print("\n🔧 Starting FastAPI backend only...")
                print("🌐 Backend API: http://localhost:8000")
                print("📚 API docs: http://localhost:8000/docs")
                start_backend()
                break
                
            elif choice == "4":
                print("\n🔌 Starting WebSocket server only...")
                print("🌐 WebSocket server: ws://localhost:8765")
                start_websocket_server()
                break
                
            elif choice == "5":
                print("👋 Goodbye!")
                sys.exit(0)
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 