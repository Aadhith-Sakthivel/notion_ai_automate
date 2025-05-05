import os
import requests
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

# ========== STEP 1: Create a Beautiful PDF ==========
def create_stylish_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    story.append(Paragraph("🌞 Daily Planner", title_style))
    story.append(Spacer(1, 0.3 * inch))

    sections = [
        ("📝 To-Do List", 5),
        ("📅 Appointments", 4),
        ("💡 Notes", 4),
        ("🙏 Gratitude", 2),
    ]

    for section_title, lines in sections:
        story.append(Paragraph(f"<b>{section_title}</b>", styles["Heading2"]))
        for _ in range(lines):
            story.append(Paragraph("__________________________________________", styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

    doc.build(story)
    print(f"✅ PDF created at {output_path}")

# ========== STEP 2: Create Product on Gumroad ==========
def create_gumroad_product(title, description, price_usd, token):
    url = "https://api.gumroad.com/v2/products"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": title,
        "description": description,
        "price": int(price_usd * 100),  # in cents
        "published": False
    }

    response = requests.post(url, headers=headers, data=data)
    res = response.json()
    if res.get("success"):
        print("✅ Product created.")
        return res["product"]["id"]
    else:
        print("❌ Failed to create product:", res)
        return None

# ========== STEP 3: Upload File to Gumroad ==========
def upload_to_gumroad(product_id, file_path, token):
    url = f"https://api.gumroad.com/v2/products/{product_id}/files"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open(file_path, "rb")}
    data = {"name": os.path.basename(file_path)}

    response = requests.post(url, headers=headers, files=files, data=data)
    res = response.json()
    if res.get("success"):
        print("✅ File uploaded to product.")
    else:
        print("❌ Upload failed:", res)

# ========== MAIN WORKFLOW ==========
def main():
    # Load environment variables
    gumroad_token = os.getenv("GUMROAD_TOKEN")
    if not gumroad_token:
        raise EnvironmentError("Missing GUMROAD_TOKEN env var")

    today = datetime.now().strftime('%Y-%m-%d')
    title = f"Daily Planner - {today}"
    description = "A printable PDF to organize your daily tasks, appointments, and gratitude entries."
    price = 5.00
    output_path = f"daily_planner_{today}.pdf"

    create_stylish_pdf(output_path)
    product_id = create_gumroad_product(title, description, price, gumroad_token)

    if product_id:
        upload_to_gumroad(product_id, output_path, gumroad_token)

if __name__ == "__main__":
    main()
