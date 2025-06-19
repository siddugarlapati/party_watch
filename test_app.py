#!/usr/bin/env python3
"""
Test script for PartyWatch app
Run this to verify everything works before deployment
"""

import requests
import json
import time
import subprocess
import sys
import os

def test_backend():
    """Test backend API endpoints"""
    print("🧪 Testing Backend API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print("❌ Root endpoint failed")
            return False
        
        # Test API root endpoint
        response = requests.get(f"{base_url}/api")
        if response.status_code == 200:
            print("✅ API root endpoint working")
        else:
            print("❌ API root endpoint failed")
            return False
        
        # Test room creation
        room_data = {
            "room_code": "TEST123",
            "host_id": "test_user",
            "video_id": "dQw4w9WgXcQ",
            "room_name": "Test Room",
            "room_type": "YouTube"
        }
        
        response = requests.post(f"{base_url}/api/rooms", json=room_data)
        if response.status_code == 200:
            print("✅ Room creation working")
        else:
            print("❌ Room creation failed")
            return False
        
        # Test room retrieval
        response = requests.get(f"{base_url}/api/rooms/TEST123")
        if response.status_code == 200:
            print("✅ Room retrieval working")
        else:
            print("❌ Room retrieval failed")
            return False
        
        # Test chat message
        chat_data = {
            "room_code": "TEST123",
            "user_id": "test_user",
            "username": "TestUser",
            "message": "Hello World!"
        }
        
        response = requests.post(f"{base_url}/api/chat/messages", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat message working")
        else:
            print("❌ Chat message failed")
            return False
        
        print("🎉 Backend tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Start with: uvicorn backend.app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_frontend():
    """Test frontend functionality"""
    print("\n🧪 Testing Frontend...")
    
    try:
        # Check if streamlit app can be imported
        import streamlit as st
        print("✅ Streamlit import working")
        
        # Check if main app file exists
        if os.path.exists("streamlit_app.py"):
            print("✅ Frontend file exists")
        else:
            print("❌ Frontend file missing")
            return False
        
        # Check if requirements are met
        import requests
        print("✅ Requests library available")
        
        print("🎉 Frontend tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Frontend test error: {e}")
        return False

def test_dependencies():
    """Test if all dependencies are available"""
    print("\n🧪 Testing Dependencies...")
    
    required_packages = [
        "streamlit",
        "requests", 
        "fastapi",
        "uvicorn",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements_streamlit.txt")
        return False
    
    print("🎉 All dependencies available!")
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        "streamlit_app.py",
        "backend/app/main.py",
        "backend/requirements.txt",
        "requirements_streamlit.txt",
        "render.yaml"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("🎉 All required files present!")
    return True

def main():
    """Run all tests"""
    print("🚀 PartyWatch Pre-Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_dependencies,
        test_frontend,
        test_backend
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Deploy backend to Render")
        print("2. Deploy frontend to Render")
        print("3. Set environment variables")
        print("4. Test live deployment")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 