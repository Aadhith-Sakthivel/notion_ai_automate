import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import requests

def create_planner_pdf(filename):
    today = datetime.date.today().strftime('%A, %B %d, %Y')
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "Daily Planner")

    # Date
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 80, today)

    # Sections
    y = height - 130
    sections = [
        "☀️ Morning Routine:",
        "📋 To-Do List:",
        "📞 Appointments:",
        "🍱 Meals:",
        "💧 Water Intake:",
        "🧘 Self-Care:",
        "🌙 Evening Reflection:"
    ]

    c.setFont("Helvetica-Bold", 12)
    for section in sections:
        c.drawString(50, y, section)
        y -= 20
        c.setFont("Helvetica", 10)
        for _ in range(5):
            c.drawString(70, y, "__________________________")
            y -= 15
        y -= 10
        c.setFont("Helvetica-Bold", 12)

    c.save()
    print(f"✅ PDF created at {filename}")

def create_gumroad_product(title, description, price, token):
    url = "https://api.gumroad.com/v2/products"
    payload = {
        "name": title,
        "description": description,
        "price": int(float(price) * 100),  # in cents
        "published": False
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, data=payload, headers=headers)

    print(f"📡 Gumroad response code: {response.status_code}")
    print(f"📡 Gumroad response body: {response.text}")

    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ Failed to decode Gumroad response as JSON.")
        raise

    if not res.get("success"):
        raise Exception(f"❌ Gumroad API error: {res}")

    product_id = res["product"]["id"]
    print(f"✅ Created Gumroad product with ID: {product_id}")
    return product_id

def upload_file_to_gumroad(product_id, file_path, token):
    url = f"https://api.gumroad.com/v2/products/{product_id}/files"
    files = {'file': open(file_path, 'rb')}
    data = {'name': os.path.basename(file_path)}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, files=files, data=data, headers=headers)

    print(f"📡 Upload file response: {response.status_code}")
    print(f"📡 Upload response body: {response.text}")

    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ File upload failed: response not JSON.")
        raise

    if not res.get("success"):
        raise Exception(f"❌ File upload failed: {res}")

    print("✅ File uploaded to Gumroad")

def main():
    filename = f"daily_planner_{datetime.date.today()}.pdf"
    create_planner_pdf(filename)

    title = f"Daily Planner - {datetime.date.today().strftime('%b %d, %Y')}"
    description = "A printable daily planner to help you stay organized and mindful throughout your day."
    price = 5.00

    gumroad_token = os.getenv("GUMROAD_TOKEN")
    if not gumroad_token:
        raise EnvironmentError("❌ GUMROAD_TOKEN not found in environment variables")

    product_id = create_gumroad_product(title, description, price, gumroad_token)
    upload_file_to_gumroad(product_id, filename, gumroad_token)

if __name__ == "__main__":
    main()
