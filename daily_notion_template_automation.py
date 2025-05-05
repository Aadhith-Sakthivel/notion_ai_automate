import requests
from openai import OpenAI
import os
from datetime import datetime

# === CONFIGURATION ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
    prompt = "Give me one trending productivity or lifestyle digital template idea people are searching for today."
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "your prompt"}],
    temperature=0.7
    )
    print(response.choices[0].message.content)
    return response.choices[0].message['content'].strip().replace('"', '')

# === STEP 2: Generate Notion Template Content ===
def generate_template_content(topic):
    prompt = f"Create a full Notion template in markdown for: {topic}. Include sections, formatting, and realistic headings."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message['content']

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
        print(" Notion page created.")
        return res.json().get("url", "https://notion.so")
    else:
        print(" Failed to create Notion page:", res.text)
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

    # Gumroad API does not support direct product upload without manual file or approval
    # Simulate successful creation
    print(f" Simulated Gumroad upload for '{title}'.")
    return f"https://gumroad.com/l/{title.lower().replace(' ', '-')}"

# === STEP 5: Generate Image (Mocked) ===
def generate_pin_image(title):
    filename = f"pin_{title.replace(' ', '_')}.png"
    with open(filename, 'w') as f:
        f.write("Mock Pinterest image")
    return filename

# === STEP 6: Post to Pinterest (Mocked) ===
def post_to_pinterest(image_path, title, url):
    print(f" Posted to Pinterest: {title} → {url} (Mocked, implement API if needed)")

# === MAIN RUN ===
def main():
    topic = get_trending_topic()
    print(f" Trending Topic: {topic}")
    content = generate_template_content(topic)
    notion_url = create_notion_page(topic, content)
    gumroad_url = upload_to_gumroad(topic, "Free auto-generated Notion template", content)
    pin_image = generate_pin_image(topic)
    post_to_pinterest(pin_image, topic, gumroad_url)

if __name__ == "__main__":
    main()
