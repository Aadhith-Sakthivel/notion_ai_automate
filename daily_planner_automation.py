import os
import datetime
import requests
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

load_dotenv()

def create_planner_pdf(filename):
    today = datetime.date.today().strftime('%A, %B %d, %Y')
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "Daily Planner")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 80, today)

    y = height - 130
    sections = [
        "☀️ Morning Routine:", "📋 To-Do List:", "📞 Appointments:",
        "🍱 Meals:", "💧 Water Intake:", "🧘 Self-Care:", "🌙 Evening Reflection:"
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

def upload_to_dropbox(file_path):
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    folder_path = os.getenv("DROPBOX_UPLOAD_FOLDER", "/")
    filename = os.path.basename(file_path)
    dropbox_path = f"{folder_path}/{filename}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": str({
            "path": dropbox_path,
            "mode": "add",
            "autorename": True,
            "mute": False
        }).replace("'", '"')  # Dropbox expects double quotes
    }

    with open(file_path, "rb") as f:
        response = requests.post("https://content.dropboxapi.com/2/files/upload", headers=headers, data=f)

    if response.status_code == 200:
        print("✅ Successfully uploaded to Dropbox.")
    else:
        print("❌ Dropbox upload failed:", response.text)

def main():
    filename = f"daily_planner_{datetime.date.today()}.pdf"
    create_planner_pdf(filename)
    upload_to_dropbox(filename)

if __name__ == "__main__":
    main()
