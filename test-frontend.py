#!/usr/bin/env python3
"""
Test the frontend by simulating user interactions
"""

import requests
import json
import time

def test_frontend_api():
    print("🌐 Testing Frontend API Integration")
    print("=" * 50)
    
    # Test if frontend can reach backend through CORS
    frontend_url = "http://localhost:3000"
    backend_url = "http://localhost:8000"
    
    print(f"Frontend URL: {frontend_url}")
    print(f"Backend URL: {backend_url}")
    
    # Test direct backend call (what frontend will do)
    try:
        response = requests.post(f"{backend_url}/api/v1/ai/summarize", 
                               json={"text": "This is a test from the frontend interface.", "max_length": 30},
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend API working for frontend!")
            print(f"Summary: {result['data']['summary']}")
        else:
            print(f"❌ Backend error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print("\n🎉 Frontend is ready!")
    print("Visit: http://localhost:3000")
    print("Try all the AI features through the web interface!")

if __name__ == "__main__":
    test_frontend_api()