#!/usr/bin/env python3
"""
Demo client for the AI Backend Service
This script demonstrates how to use all the API endpoints
"""

import requests
import time
import json
from typing import Dict, Any

class AIBackendClient:
    """Client for the AI Backend Service"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
    
    def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        response = requests.get(f"{self.api_base}/health/")
        return response.json()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        response = requests.get(f"{self.api_base}/health/metrics")
        return response.json()
    
    def summarize_text(self, text: str, max_length: int = 200, async_mode: bool = False) -> Dict[str, Any]:
        """Summarize text"""
        endpoint = f"{self.api_base}/ai/summarize"
        if async_mode:
            endpoint += "/async"
        
        payload = {"text": text, "max_length": max_length}
        response = requests.post(endpoint, json=payload)
        return response.json()
    
    def answer_question(self, context: str, question: str, async_mode: bool = False) -> Dict[str, Any]:
        """Answer question based on context"""
        endpoint = f"{self.api_base}/ai/question-answer"
        if async_mode:
            endpoint += "/async"
        
        payload = {"context": context, "question": question}
        response = requests.post(endpoint, json=payload)
        return response.json()
    
    def rewrite_tone(self, text: str, target_tone: str, async_mode: bool = False) -> Dict[str, Any]:
        """Rewrite text with different tone"""
        endpoint = f"{self.api_base}/ai/tone-rewrite"
        if async_mode:
            endpoint += "/async"
        
        payload = {"text": text, "target_tone": target_tone}
        response = requests.post(endpoint, json=payload)
        return response.json()
    
    def translate_text(self, text: str, target_language: str, source_language: str = None, async_mode: bool = False) -> Dict[str, Any]:
        """Translate text"""
        endpoint = f"{self.api_base}/ai/translate"
        if async_mode:
            endpoint += "/async"
        
        payload = {
            "text": text,
            "target_language": target_language
        }
        if source_language:
            payload["source_language"] = source_language
        
        response = requests.post(endpoint, json=payload)
        return response.json()
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status"""
        response = requests.get(f"{self.api_base}/jobs/{job_id}")
        return response.json()
    
    def wait_for_job(self, job_id: str, timeout: int = 60) -> Dict[str, Any]:
        """Wait for async job to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            
            if status.get("status") in ["completed", "failed"]:
                return status
            
            time.sleep(2)
        
        return {"error": "Job timeout"}

def main():
    """Demo the AI Backend Service"""
    client = AIBackendClient()
    
    print("🚀 AI Backend Service Demo")
    print("=" * 50)
    
    # Health check
    print("\n1. Health Check")
    try:
        health = client.health_check()
        print(f"✅ Service Status: {health.get('status', 'unknown')}")
        print(f"📊 Services: {health.get('services', {})}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # System metrics
    print("\n2. System Metrics")
    try:
        metrics = client.get_metrics()
        if metrics.get("success"):
            data = metrics["data"]
            print(f"💻 CPU Usage: {data.get('cpu_usage_percent', 0):.1f}%")
            print(f"🧠 Memory Usage: {data.get('memory', {}).get('percent', 0):.1f}%")
        else:
            print(f"❌ Metrics failed: {metrics.get('error')}")
    except Exception as e:
        print(f"❌ Metrics failed: {e}")
    
    # Sample text for demos
    sample_text = """
    Artificial Intelligence (AI) is revolutionizing industries across the globe. 
    From healthcare to finance, AI technologies are enabling unprecedented automation 
    and decision-making capabilities. Machine learning algorithms can now process 
    vast amounts of data to identify patterns and make predictions that were 
    previously impossible for humans to achieve. As we move forward, the integration 
    of AI into everyday business processes will continue to accelerate, creating 
    new opportunities and challenges for organizations worldwide.
    """
    
    sample_context = """
    Python is a high-level, interpreted programming language with dynamic semantics. 
    Its high-level built-in data structures, combined with dynamic typing and dynamic 
    binding, make it very attractive for Rapid Application Development, as well as 
    for use as a scripting or glue language to connect existing components together. 
    Python was created by Guido van Rossum and first released in 1991.
    """
    
    # Text Summarization
    print("\n3. Text Summarization (Sync)")
    try:
        result = client.summarize_text(sample_text, max_length=150)
        if result.get("success"):
            summary = result["data"]["summary"]
            cached = result["data"].get("cached", False)
            print(f"📝 Summary: {summary}")
            print(f"⚡ Cached: {'Yes' if cached else 'No'}")
        else:
            print(f"❌ Summarization failed: {result}")
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
    
    # Question Answering
    print("\n4. Question Answering (Sync)")
    try:
        result = client.answer_question(sample_context, "Who created Python?")
        if result.get("success"):
            answer = result["data"]["answer"]
            cached = result["data"].get("cached", False)
            print(f"❓ Answer: {answer}")
            print(f"⚡ Cached: {'Yes' if cached else 'No'}")
        else:
            print(f"❌ Q&A failed: {result}")
    except Exception as e:
        print(f"❌ Q&A failed: {e}")
    
    # Tone Rewriting
    print("\n5. Tone Rewriting (Sync)")
    try:
        casual_text = "Hey, this AI stuff is pretty cool!"
        result = client.rewrite_tone(casual_text, "formal")
        if result.get("success"):
            rewritten = result["data"]["rewritten_text"]
            print(f"✏️  Original: {casual_text}")
            print(f"🎭 Formal: {rewritten}")
        else:
            print(f"❌ Tone rewriting failed: {result}")
    except Exception as e:
        print(f"❌ Tone rewriting failed: {e}")
    
    # Translation
    print("\n6. Translation (Sync)")
    try:
        result = client.translate_text("Hello, how are you?", "Spanish")
        if result.get("success"):
            translation = result["data"]["translation"]
            print(f"🌍 English: Hello, how are you?")
            print(f"🇪🇸 Spanish: {translation}")
        else:
            print(f"❌ Translation failed: {result}")
    except Exception as e:
        print(f"❌ Translation failed: {e}")
    
    # Async Processing Demo
    print("\n7. Async Processing Demo")
    try:
        # Start async summarization
        result = client.summarize_text(sample_text, max_length=100, async_mode=True)
        if result.get("success"):
            job_id = result["data"]["job_id"]
            print(f"🔄 Started async job: {job_id}")
            
            # Wait for completion
            print("⏳ Waiting for job completion...")
            final_result = client.wait_for_job(job_id)
            
            if final_result.get("status") == "completed":
                summary = final_result["result"]["summary"]
                print(f"✅ Async Summary: {summary}")
            else:
                print(f"❌ Async job failed: {final_result}")
        else:
            print(f"❌ Async job creation failed: {result}")
    except Exception as e:
        print(f"❌ Async processing failed: {e}")
    
    print("\n🎉 Demo completed!")
    print("\nTry the interactive API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()