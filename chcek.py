import google.generativeai as genai
import os

# 1. Setup your key (I am using the one from your previous message)
genai.configure(api_key="AIzaSyCFMZl8Zx2uO9d-KHlNG4vBlamQsz5yEjw")

print("------ ASKING GOOGLE FOR AVAILABLE MODELS ------")

try:
    # 2. Get the list of models
    for m in genai.list_models():
        # 3. Only show models that can generate text
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ NAME: {m.name}")
            
except Exception as e:
    print(f"❌ Error: {e}")

print("------------------------------------------------")