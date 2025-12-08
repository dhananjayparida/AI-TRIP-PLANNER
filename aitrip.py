
import os

import datetime

import json

from dotenv import load_dotenv



# Google Gemini imports

import google.generativeai as genai



# Transformers (Hugging Face) imports

from transformers import pipeline



# ----------------------- CONFIGURATION -----------------------

load_dotenv()



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBZ_EZWe_Wac-kxbBq-1Mq-RzD5wg94-2M")



if GEMINI_API_KEY:

    genai.configure(api_key=GEMINI_API_KEY)

else:

    print("⚠ No Gemini API key found. Falling back to Transformers mode.\n")



# ----------------------- PROMPT TEMPLATE -----------------------



def build_prompt(source, destination, days, budget):

    """Creates the enhanced JSON-based trip prompt."""

    prompt = f"""

    You are an enthusiastic AI-powered travel influencer 🌍 who creates exciting, realistic, and budget-friendly itineraries.



    Plan a {days}-day trip from {source} to {destination} within ₹{budget}.

    Your tone should be practical, friendly, and visually rich with emojis.



    Respond **only in valid JSON** — no markdown, no extra text outside JSON.

    Use * as the bullet marker for all points.



    The JSON should strictly follow this format:

    {{

        "how_to_reach": "short bullet points with options, costs, travel time, and comfort",

        "where_to_stay": "3 options: 💸 Budget, 💼 Mid-range, 🌟 Premium — include landmarks and approx. cost/night",

        "food_and_drinks": "local dishes, famous eateries, and estimated daily food budget",

        "things_to_do": "top attractions, hidden gems, entry fees, or special experiences",

        "day_wise_itinerary": "brief plan for each day with sightseeing, meals, and evening ideas",

        "estimated_budget": "short cost breakdown (travel, stay, food, activities, extras)",

        "travel_tips": "2–3 smart tips or cultural advice",

        "overview": "a short travel influencer-style summary or caption for the trip"

    }}



    Each section must be realistic, compact, and written in engaging, emoji-filled influencer style.

    """

    return prompt.strip()



# GENERATION FUNCTIONS



def generate_with_gemini(prompt):

    """Try generating the trip plan using Gemini 2.5."""

    print("🤖 Using Gemini 2.5 for generation...")

    try:

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        text = response.text.strip()
        text = text.replace('*', '')

        # Ensure valid JSON

        return json.loads(text)

    except Exception as e:

        print(f"⚠ Gemini failed or invalid JSON: {e}")

        return None





def generate_with_transformers(prompt):

    """Fallback using Hugging Face Transformers."""

    print("💡 Switching to local Transformers model (Flan-T5)...")

    generator = pipeline("text2text-generation", model="google/flan-t5-large", device="cpu")

    result = generator(prompt, max_length=800, do_sample=True, temperature=0.8, top_p=0.9)

    text = result[0]["generated_text"].strip()

    try:

        return json.loads(text)

    except:

        print("⚠ Transformer output not valid JSON. Returning as text.")

        return {"raw_text": text}


# MAIN FUNCTION



def generate_trip_plan(source, destination, days, budget):

    """Generate and return the trip plan as structured JSON."""

    print("\n🚀 Generating your influencer-style travel plan...\n")



    prompt = build_prompt(source, destination, days, budget)



    # Try Gemini first

    data = generate_with_gemini(prompt)



    # Fallback

    if not data:

        data = generate_with_transformers(prompt)



    # Normalize fields then add meta info
    if isinstance(data, dict):
        data["metadata"] = {
            "source": source,
            "destination": destination,
            "days": days,
            "budget": f"₹{budget}",
            "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }



    print("✅ Trip plan generated successfully!\n")

    return data
