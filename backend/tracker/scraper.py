"""Adapter for the documented demo HTML format. No arbitrary URL API."""
from decimal import Decimal, InvalidOperation
from bs4 import BeautifulSoup
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
def parse_html(html):
    rows = []
    for item in BeautifulSoup(html, "html.parser").select("article.product"):
        try:
            price = Decimal(item.select_one(".price").get_text(strip=True).replace("₹","").replace(",",""))
            if not price.is_finite() or price < 0:
                raise ValueError("Invalid price")
            rows.append({"sku":item["data-sku"],"name":item.select_one("h2").get_text(strip=True),"category":item["data-category"],"source":item["data-source"],"url":item.select_one("a")["href"],"price":str(price),"currency":"INR","available":item["data-available"]=="true"})
        except (KeyError, AttributeError, InvalidOperation) as exc:
            raise ValueError("Malformed product card") from exc
    if not rows:
        raise ValueError("No products found; source adapter needs review")
    return rows
def fetch_permitted(url, allowed_hosts):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
        raise ValueError("Only explicitly approved HTTPS sources are allowed")
    robot = RobotFileParser(f"https://{parsed.netloc}/robots.txt")
    robot.read()
    if not robot.can_fetch("MarketPulseDemo", url):
        raise ValueError("robots.txt disallows this URL")
    response = requests.get(url, timeout=20, headers={"User-Agent":"MarketPulseDemo"}, allow_redirects=False)
    response.raise_for_status()
    return parse_html(response.text)
