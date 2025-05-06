from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    if not EMAIL or not PASSWORD:
        print("❌ GUMROAD_EMAIL or GUMROAD_PASSWORD not set in environment.")
        return

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")

    driver = webdriver.Chrome(options=options)

    try:
        print("🔐 Logging into Gumroad...")
        driver.get("https://gumroad.com/login")
        time.sleep(3)

        # Fill in login credentials using updated IDs
        driver.find_element(By.ID, ":R0:-email").send_keys(EMAIL)
        driver.find_element(By.ID, ":R0:-password").send_keys(PASSWORD)

        # Click the login button
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(5)

        print("🛒 Creating new product...")
        driver.get("https://gumroad.com/products/new")
        time.sleep(4)

        # Wait for "Name of product" input field
        print("Waiting for 'Name of product' input field...")
        product_name_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Name of product']"))
        )
        product_name_input.send_keys(title)

        # Wait for "Price your product" input field
        print("Waiting for 'Price your product' input field...")
        price_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Price your product']"))
        )
        price_input.clear()
        price_input.send_keys(str(price))

        # Wait for the file upload input to appear
        print("Waiting for file upload input...")
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "product[file_uploads][]"))
        )
        upload_input.send_keys(os.path.abspath(pdf_path))
        time.sleep(8)

        # Wait for the Publish button and click it
        print("Waiting for 'Publish' button...")
        publish_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish')]"))
        )
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