import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

# 1. SETUP (GitHub fills 'EMAIL_PASS' from your Secrets automatically)
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
MY_EMAIL = "muthoniemmanuel5@gmail.com"
MY_APP_PASSWORD = os.environ.get('EMAIL_PASS') 

def send_alert(product_name, current_price):
    msg = EmailMessage()
    msg['Subject'] = f"💰 PRICE DROP: {product_name}!"
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL 
    msg.set_content(f"Good news! The price for {product_name} has dropped to £{current_price}. \nCheck it out here: {URL}")

    try:
        # Connect to Gmail's server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_APP_PASSWORD)
            smtp.send_message(msg)
        print("✅ SUCCESS: Alert sent to your inbox!")
    except Exception as e:
        print(f"❌ ERROR: Could not send email. {e}")

def check_price():
    print("Searching the website...")
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the title and price
        title = soup.find("h1").get_text()
        price_text = soup.find("p", class_="price_color").get_text()
        price = float(price_text.replace('£', ''))

        print(f"Product: {title}")
        print(f"Current Price: £{price}")

        # Logic: Trigger if price is under £60
        if price < 60.00:
            print("Target met! Sending email...")
            send_alert(title, price)
        else:
            print("Price is still high.")
            
    except Exception as e:
        print(f"❌ SCRAPING ERROR: {e}")

if __name__ == "__main__":
    check_price()
