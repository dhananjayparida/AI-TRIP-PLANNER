# ==========================================================
# 🌍 AI Trip Planner v4 (Hybrid: Gemini 2.5 + Transformers)
# Author: Abhishek Thakur
# Description: Combines Gemini 2.5 API with local Transformers backup
# ==========================================================

import os
import datetime
from dotenv import load_dotenv

# Google Gemini imports
import google.generativeai as genai

# Transformers (Hugging Face) imports
from transformers import pipeline

# ----------------------- CONFIGURATION -----------------------

load_dotenv()

# Get Gemini API key from environment (do NOT hardcode keys in source)
# Ensure you have a .env file with GEMINI_API_KEY=your_key or set the env var
GEMINI_API_KEY = "AIzaSyBZ_EZWe_Wac-kxbBq-1Mq-RzD5wg94-2M"

# Configure Gemini if available
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ No Gemini API key found. Falling back to Transformers mode.\n")

# ----------------------- PROMPT TEMPLATE -----------------------

PROMPT_TEMPLATE = """You are an enthusiastic AI-powered travel planner who creates exciting, realistic, and budget-friendly itineraries.

Plan a fun and influencer-style {days}-day trip from {source} to {destination} within a budget of ₹{budget}.

Use markdown formatting, emojis, and an engaging tone. Keep it practical yet inspiring.

---

### ✈️ How to Reach
List the *best travel options* with cost, comfort, and travel time.

---

### 🏨 Where to Stay
Recommend 3 accommodation options:
- 💸 Budget
- 💼 Mid-range
- 🌟 Premium
Include nearby landmarks and approx. cost/night.

---

### 🍛 Food & Drinks
Include local dishes, famous eateries, and an estimated daily food budget.

---

### 🎡 Things to Do
Suggest must-visit attractions, hidden gems, and special local experiences.
Add entry fees or tips if needed.

---

### 🗓 Day-wise Itinerary
Plan each day briefly, including sightseeing, meals, and evening activities.

---

### 💰 Estimated Total Budget
Summarize the approximate cost breakdown (travel, stay, food, activities, extras).

---

### 💡 Travel Tips
Add 2–3 smart travel hacks or cultural tips for {destination}! 
Make it feel like a travel influencer’s post ✨
"""

# ----------------------- CORE FUNCTIONS -----------------------

def build_prompt(source, destination, days, budget):
    """Inject user inputs into the main prompt template."""
    return PROMPT_TEMPLATE.format(source=source, destination=destination, days=days, budget=budget)


def generate_with_gemini(prompt):
    """Try generating the trip plan using Gemini 2.5."""
    print("🤖 Using Gemini 2.5 for generation...")
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")
        return None


def generate_with_transformers(prompt):
    """Fallback: Generate the trip plan using Hugging Face Transformers."""
    print("💡 Switching to local Transformers model (Flan-T5)...")
    generator = pipeline("text2text-generation", model="google/flan-t5-large", device="cpu")
    result = generator(prompt, max_length=800, do_sample=True, temperature=0.8, top_p=0.9)
    return result[0]["generated_text"].strip()


def generate_trip_plan(source, destination, days, budget):
    """Generate the travel plan using Gemini (fallback to Transformers)."""
    print("\n🚀 Generating your influencer-style travel plan...\n")
    prompt = build_prompt(source, destination, days, budget)

    # Try Gemini first
    text = generate_with_gemini(prompt)

    # Fallback if Gemini fails
    if not text:
        text = generate_with_transformers(prompt)

    # Save output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tripplan_{destination.replace(' ', '_')}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    print("🗓 Trip Plan Generated Successfully!\n")
    print(f"\n💾 Saved to: {os.path.abspath(filename)}\n")
    return text
    


# ----------------------- MAIN ENTRY POINT -----------------------

if __name__ == "__main__":
    print("🧭 Welcome to AI Trip Planner v4 🌍 (Gemini + Transformers)\n")

    source = input("Enter your source city: ").strip() or "Deoghar"
    destination = input("Enter your destination city: ").strip() or "Puri"
    days = input("Number of travel days: ").strip() or "3"
    budget = input("Total budget (₹): ").strip() or "5000"

    try:
        int(days)
        int(budget)
    except ValueError:
        print("❌ Please enter valid numeric values for days and budget.")
        exit(1)

    generate_trip_plan(source, destination, days, budget)