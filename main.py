from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://www.amazon.com/Apple-2022-10-9-inch-iPad-Wi-Fi/dp/B0BJLXMVMV"

# ====================== Add Headers to the Request ===========================

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Dnt": "1",  # Do Not Track request header
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

print(soup.prettify())

price_element = soup.find(class_="a-offscreen")

if price_element:
    price = price_element.get_text().strip()

    price_without_currency = price.replace("$", "").replace(",", "")  # Remove $ and commas
    price_as_float = float(price_without_currency)

    print(f"Current Price: ${price_as_float}")

    title = soup.find(id="productTitle").get_text().strip()
    print(f"Product: {title}")

    BUY_PRICE = 300

    if price_as_float < BUY_PRICE:
        message = f"{title} is on sale for {price}!"

        # ====================== Send the Email Notification ===========================

        with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
            connection.starttls()
            connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
            connection.sendmail(
                from_addr=os.environ["EMAIL_ADDRESS"],
                to_addrs=os.environ["EMAIL_ADDRESS"],
                msg=f"Subject: Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
            )
        print("Email Sent! 🚀")
    else:
        print("Price is still above $300.")
else:
    print("Error: Could not find the price on the Amazon page.")