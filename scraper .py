import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

# 1. SETUP (GitHub will fill these in automatically)
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
MY_EMAIL = "muthoniemmanuel5@gmail.com"
MY_APP_PASSWORD = os.environ.get('EMAIL_PASS') 

def send_alert(product_name, current_price):
    msg = EmailMessage()
    msg['Subject'] = f"💰 PRICE DROP: {product_name}!"
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL 
    msg.set_content(f"The price for {product_name} dropped to £{current_price}! \nLink: {URL}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_APP_PASSWORD)
            smtp.send_message(msg)
        print("✅ Alert sent!")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("h1").get_text()
    price_text = soup.find("p", class_="price_color").get_text()
    price = float(price_text.replace('£', ''))

    # Trigger alert if price is under £60
    if price < 60.00:
        send_alert(title, price)

if __name__ == "__main__":
    check_price()