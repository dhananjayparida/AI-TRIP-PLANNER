from google import genai

client = genai.Client(api_key="AIzaSyCUCdsGEnc2isVLd2v1NfLafBeL_nUIEo4")


chat = client.chats.create(model="gemini-2.0-flash")


city = input("City: ")
destination = input("Destination: ")
days = input("Number of days: ")
budget = input("Budget: ") 
message = f"""You are an enthusiastic AI-powered travel planner who creates exciting, realistic, and budget-friendly itineraries.

Plan a fun and influencer-style {days}-day trip from {city} to {destination} within a budget of ₹{budget}.

Use markdown formatting, emojis, and an engaging tone. Keep it practical yet inspiring.

---

###  How to Reach
List the best travel options with cost, comfort, and travel time.

---

###  Where to Stay
Recommend 3 accommodation options:
-  Budget
-  Mid-range
-  Premium
Include nearby landmarks and approx. cost/night.

---

###  Food & Drinks
Include local dishes, famous eateries, and an estimated daily food budget.

---

###  Things to Do
Suggest must-visit attractions, hidden gems, and special local experiences.
Add entry fees or tips if needed.

---

###  Day-wise Itinerary
Plan each day briefly, including sightseeing, meals, and evening activities.

---

###  Estimated Total Budget
Summarize the approximate cost breakdown (travel, stay, food, activities, extras).

---

###  Travel Tips
Add 2–3 smart travel hacks or cultural tips for {destination}! 
Make it feel like a travel influencer’s post """
#message = f"Create a travel itinerary for a trip to {city} to {destination} for {days} days with a budget of {budget} Ruppees. Provide day-wise activities and places to visit. in brief points format, use * for points."
response = chat.send_message(message)
with open("data.txt", "w") as file:
   file.write(response.text)

with open("data.txt", "r") as file:
   content=file.read()
newcontent=content.replace("*"," ")
print("AI:", newcontent)
