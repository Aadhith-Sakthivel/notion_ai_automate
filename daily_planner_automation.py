from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import datetime
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

def upload_to_gumroad(pdf_path, title, price):
    EMAIL = os.getenv("GUMROAD_EMAIL")
    PASSWORD = os.getenv("GUMROAD_PASSWORD")

    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    try:
        # Login
        driver.get("https://gumroad.com/login")
        time.sleep(3)
        driver.find_element(By.NAME, "user[email]").send_keys(EMAIL)
        driver.find_element(By.NAME, "user[password]").send_keys(PASSWORD)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(5)

        # Go to new product
        driver.get("https://gumroad.com/products/new")
        time.sleep(4)

        # Title
        driver.find_element(By.NAME, "product[name]").send_keys(title)

        # Price
        price_input = driver.find_element(By.NAME, "product[price]")
        price_input.clear()
        price_input.send_keys(str(price))

        # Upload PDF
        upload_input = driver.find_element(By.NAME, "product[file_uploads][]")
        upload_input.send_keys(os.path.abspath(pdf_path))
        time.sleep(8)

        # Click Publish
        publish_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Publish')]")
        driver.execute_script("arguments[0].scrollIntoView();", publish_button)
        time.sleep(1)
        publish_button.click()
        time.sleep(5)

        print("✅ Successfully uploaded and published product to Gumroad.")
    except Exception as e:
        print("❌ Error during Gumroad automation:", e)
    finally:
        driver.quit()

def main():
    filename = f"daily_planner_{datetime.date.today()}.pdf"
    create_planner_pdf(filename)

    title = f"Daily Planner - {datetime.date.today().strftime('%b %d, %Y')}"
    price = 5.00

    upload_to_gumroad(filename, title, price)

if __name__ == "__main__":
    main()