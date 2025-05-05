import requests
import google.generativeai as genai
import os
from datetime import datetime

# === CONFIGURATION ===
genai.configure(api_key=os.getenv("GEN_API_KEY"))  # Ensure this API key is set in your environment
model = genai.GenerativeModel('gemini-pro')
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
PINTEREST_TOKEN = os.getenv("PINTEREST_TOKEN")  # Still mocked below

headers_notion = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# === STEP 1: Generate a Trending Topic Using OpenAI ===
def get_trending_topic():
    topics = [
        "All-in-One Life OS", "Second Brain System", "Daily Planner + Habit Tracker",
        "Goal Setting + Vision Board", "Weekly Review System", "Time Blocking Planner",
        "Yearly Reflection Journal", "Freelancer Business Hub", "Client CRM + Invoice Tracker",
        "Content Creator Dashboard", "Social Media Content Planner", "Etsy/Digital Product Launch Planner",
        "Affiliate Income + Link Tracker", "Notion Website / Portfolio Builder", "Project & Task Management System",
        "Student Life Planner", "Assignment & Deadline Tracker", "Study Planner (Pomodoro + Revision)",
        "Class & Exam Schedule", "Thesis/Dissertation Tracker", "Ultimate Budget Tracker",
        "Subscription + Bill Tracker", "Debt Payoff Planner", "Investment Tracker", "Savings Goal Tracker",
        "Mental Health & Mood Tracker", "Fitness & Meal Plan Dashboard", "Gratitude Journal", "Sleep & Wellness Log",
        "Book & Learning Tracker"
    ]
    today = datetime.utcnow().day
    topic = topics[(today - 1) % len(topics)]
    return topic

# === STEP 2: Generate Notion Template Content ===
def generate_template_content(topic):
    models = genai.list_models()

    for m in models:
        print(m.name, "supports generateContent:", "generateContent" in m.supported_generation_methods)
    prompt = f"Create a full Notion template in markdown for: {topic}. Include sections, formatting, and realistic headings."
    response = model.generate_content(prompt)
    return response.text

# === STEP 3: Create Page in Notion with Content ===
def create_notion_page(title, content):
    url = "https://api.notion.com/v1/pages"
    today = datetime.now().strftime("%Y-%m-%d")

    payload = {
        "parent": {"page_id": NOTION_PAGE_ID},
        "properties": {
            "title": [
                {
                    "text": {"content": f"{title} - {today}"}
                }
            ]
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": content[:2000]}}]  # limit block length
                }
            }
        ]
    }

    res = requests.post(url, headers=headers_notion, json=payload)
    if res.status_code in [200, 201]:
        print("Notion page created successfully.")
        return res.json().get("url", "https://notion.so")
    else:
        print("Failed to create Notion page:", res.text)
        return "https://notion.so"

# === STEP 4: Upload Template to Gumroad ===
def upload_to_gumroad(title, description, content):
    gumroad_url = "https://api.gumroad.com/v2/products"
    payload = {
        "product": {
            "name": title,
            "description": description,
            "price": 0,
            "custom_permalink": title.lower().replace(" ", "-"),
            "is_free": True
        }
    }

    headers = {
        "Authorization": f"Bearer {GUMROAD_TOKEN}",
        "Content-Type": "application/json"
    }

    # Simulating Gumroad product creation as the Gumroad API does not support direct file uploads in this manner
    print(f"Simulated Gumroad upload for '{title}'.")
    return f"https://gumroad.com/l/{title.lower().replace(' ', '-')}"  # Simulated link

# === STEP 5: Generate Image (Mocked) ===
def generate_pin_image(title):
    filename = f"pin_{title.replace(' ', '_')}.png"
    with open(filename, 'w') as f:
        f.write("Mock Pinterest image")  # In reality, you'd generate an actual image here
    return filename

# === STEP 6: Post to Pinterest (Mocked) ===
def post_to_pinterest(image_path, title, url):
    print(f"Posted to Pinterest: {title} → {url} (Mocked, implement actual API if needed)")

# === MAIN RUN ===
def main():
    topic = get_trending_topic()
    print(f"Trending Topic: {topic}")
    content = generate_template_content(topic)
    notion_url = create_notion_page(topic, content)
    gumroad_url = upload_to_gumroad(topic, "Free auto-generated Notion template", content)
    pin_image = generate_pin_image(topic)
    post_to_pinterest(pin_image, topic, gumroad_url)

if __name__ == "__main__":
    main()
