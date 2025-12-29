import requests
import json
import time

# Since we moved the Nginx proxy to 8080 to avoid Windows conflicts
GATEWAY_URL = "http://localhost:8080/chat"

def fire_agentic_request():
    print("🚀 Firing Mission-Critical Request to AI Superjack Mesh...")
    
    payload = {
        "task": "Research the top 3 AI marketing trends for 2026 and provide a strategic ROI roadmap for implementation.",
        "user_id": "stefanos_cunning"
    }
    
    start_time = time.time()
    
    try:
        # 1. Hit the Gateway
        response = requests.post(GATEWAY_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            duration = time.time() - start_time
            
            print(f"\n✅ MESH RESPONSE RECEIVED (took {duration:.2f}s)")
            print("-" * 50)
            print(f"🤖 FINAL STRATEGY:\n{result.get('final_output')}")
            print("-" * 50)
            print(f"📊 AGENT CHAIN: {' -> '.join(result.get('agent_chain', []))}")
            print("-" * 50)
            print("💡 PRO-TIP: Run this again to test the Semantic Cache speed!")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"🚨 Connection Failed: {str(e)}")

if __name__ == "__main__":
    fire_agentic_request()