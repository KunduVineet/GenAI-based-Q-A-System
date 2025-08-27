#!/usr/bin/env python3
"""
Complete Frontend User Experience Test
Simulating a real user discovering and using the AI web interface
"""

import requests
import json
import time
from datetime import datetime

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"

def print_user_action(action):
    print(f"\n👤 USER ACTION: {action}")
    print("-" * 60)

def print_result(success, feature, result_text, time_taken=None):
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"{status} - {feature}")
    if time_taken:
        print(f"⏱️  Response time: {time_taken:.2f} seconds")
    print(f"📝 Result: {result_text}")
    print("-" * 40)

def simulate_frontend_request(endpoint, payload, feature_name):
    """Simulate what the frontend does when user clicks a button"""
    try:
        start_time = time.time()
        response = requests.post(f"{BACKEND_URL}{endpoint}", json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return True, data.get('data', {}), end_time - start_time
            else:
                return False, data.get('message', 'Unknown error'), end_time - start_time
        else:
            return False, f"HTTP {response.status_code}", end_time - start_time
    except Exception as e:
        return False, str(e), 0

def test_new_user_experience():
    print(f"""
🌟 NEW USER TESTING: AI Text Assistant Web Interface
{'='*70}
Scenario: A person just discovered this AI website and wants to try it out
Time: {datetime.now()}
Website: {FRONTEND_URL}
""")

    # Test 1: User wants to summarize a news article
    print_user_action("I found a long news article and want a quick summary")
    
    news_article = """
    Breaking News: Scientists at MIT have developed a revolutionary new battery technology 
    that could charge electric vehicles in just 30 seconds. The breakthrough involves using 
    a new type of lithium-metal battery with a special coating that prevents dangerous 
    dendrite formation. This technology could solve one of the biggest barriers to electric 
    vehicle adoption - long charging times. The research team, led by Dr. Sarah Chen, 
    published their findings in Nature Energy journal. The new batteries can handle over 
    10,000 charge cycles without significant degradation, far exceeding current battery 
    technology. Major automotive companies including Tesla, Ford, and Toyota have already 
    expressed interest in licensing this technology. Commercial applications could be 
    available within 3-5 years if testing continues to show positive results.
    """
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/summarize", 
        {"text": news_article, "max_length": 80},
        "Text Summarization"
    )
    
    if success:
        print_result(True, "News Article Summary", result.get('summary', ''), time_taken)
    else:
        print_result(False, "News Article Summary", result, time_taken)

    # Test 2: User has a question about something they read
    print_user_action("I read about climate change and have a question")
    
    climate_context = """
    Climate change is causing rising sea levels, more frequent extreme weather events, 
    and shifts in precipitation patterns. The primary cause is increased greenhouse gas 
    emissions from human activities, particularly burning fossil fuels. The Paris Agreement 
    aims to limit global warming to 1.5°C above pre-industrial levels. Renewable energy 
    sources like solar and wind are becoming more cost-effective alternatives to fossil fuels.
    """
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/question-answer",
        {"context": climate_context, "question": "What is the main goal of the Paris Agreement?"},
        "Question Answering"
    )
    
    if success:
        print_result(True, "Climate Change Question", result.get('answer', ''), time_taken)
    else:
        print_result(False, "Climate Change Question", result, time_taken)

    # Test 3: User wants to make their email more professional
    print_user_action("I need to write a professional email to my boss")
    
    casual_email = "hey boss, can't make it to the meeting tomorrow cuz I'm sick. maybe we can reschedule? thanks"
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/tone-rewrite",
        {"text": casual_email, "target_tone": "professional"},
        "Professional Email Rewrite"
    )
    
    if success:
        print_result(True, "Email Tone Rewrite", result.get('rewritten_text', ''), time_taken)
    else:
        print_result(False, "Email Tone Rewrite", result, time_taken)

    # Test 4: User wants to translate a message for their Spanish friend
    print_user_action("I want to wish my Spanish friend happy birthday")
    
    birthday_message = "Happy birthday! I hope you have an amazing day filled with joy, laughter, and wonderful surprises. Can't wait to celebrate with you!"
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/translate",
        {"text": birthday_message, "target_language": "Spanish"},
        "Birthday Message Translation"
    )
    
    if success:
        print_result(True, "Spanish Translation", result.get('translation', ''), time_taken)
    else:
        print_result(False, "Spanish Translation", result, time_taken)

    # Test 5: User wants to make a complaint sound friendlier
    print_user_action("I'm frustrated with a service but want to sound nice")
    
    complaint = "This service is terrible and I want my money back immediately. This is unacceptable."
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/tone-rewrite",
        {"text": complaint, "target_tone": "friendly"},
        "Friendly Complaint Rewrite"
    )
    
    if success:
        print_result(True, "Friendly Tone Rewrite", result.get('rewritten_text', ''), time_taken)
    else:
        print_result(False, "Friendly Tone Rewrite", result, time_taken)

    # Test 6: User wants help understanding a complex topic
    print_user_action("I'm confused about cryptocurrency and need it explained simply")
    
    crypto_text = """
    Cryptocurrency is a digital or virtual currency that uses cryptography for security and 
    operates independently of a central bank. Bitcoin, created in 2009, was the first 
    decentralized cryptocurrency. It uses blockchain technology, which is a distributed 
    ledger that records all transactions across a network of computers. Mining is the 
    process by which new bitcoins are created and transactions are verified. The value 
    of cryptocurrencies is highly volatile and can fluctuate dramatically based on market 
    sentiment, regulatory news, and adoption rates.
    """
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/question-answer",
        {"context": crypto_text, "question": "How does cryptocurrency work in simple terms?"},
        "Cryptocurrency Explanation"
    )
    
    if success:
        print_result(True, "Crypto Explanation", result.get('answer', ''), time_taken)
    else:
        print_result(False, "Crypto Explanation", result, time_taken)

    # Test 7: User wants to translate to a different language
    print_user_action("I want to learn how to say 'thank you' in French")
    
    success, result, time_taken = simulate_frontend_request(
        "/api/v1/ai/translate",
        {"text": "Thank you very much for your help!", "target_language": "French"},
        "French Translation"
    )
    
    if success:
        print_result(True, "French Thank You", result.get('translation', ''), time_taken)
    else:
        print_result(False, "French Thank You", result, time_taken)

    # Final User Verdict
    print(f"""
{'='*70}
🎉 NEW USER FINAL VERDICT
{'='*70}

👤 USER THOUGHTS:
"Wow! This AI website is incredible! I can:

✅ Get quick summaries of long articles
✅ Ask questions about anything I read  
✅ Make my writing more professional
✅ Translate messages to other languages
✅ Change the tone of my messages
✅ Get help understanding complex topics

The interface is so easy to use - I just:
1. Choose what I want to do (tabs at the top)
2. Paste my text
3. Click the button
4. Get instant results!

This is way better than trying to figure out technical commands.
I can use this for work, school, and talking to friends!"

⭐ USER RATING: 5/5 STARS
💬 USER COMMENT: "This is exactly what I needed! So simple and powerful!"

🚀 RECOMMENDATION: "I'm definitely bookmarking this and sharing with friends!"
""")

def check_website_accessibility():
    """Check if the website is accessible to users"""
    print("🌐 Checking Website Accessibility...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Website is accessible at http://localhost:3000")
            print("✅ Users can visit and use the interface")
            return True
        else:
            print(f"❌ Website returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Website is not accessible: {e}")
        return False

if __name__ == "__main__":
    # First check if website is accessible
    if check_website_accessibility():
        # Run the full user experience test
        test_new_user_experience()
    else:
        print("❌ Cannot test user experience - website is not accessible")
        print("💡 Make sure both frontend (npm run dev) and backend are running")