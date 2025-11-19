import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from datetime import datetime
import os
import time

# RSS feed for CNA Asia
CNA_RSS_ASIA = "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6511"  # Asia category :contentReference[oaicite:1]{index=1}

def fetch_rss(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_cna_rss(xml_data):
    root = ET.fromstring(xml_data)
    headlines = []
    # RSS format: <item><title>Headline</title>...
    for item in root.findall(".//item"):
        title = item.find("title")
        if title is not None and title.text:
            headlines.append(title.text.strip())
    return headlines

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)

def scrape_cna(driver):
    # Fallback: if RSS fails or you want full page headlines
    driver.get("https://www.channelnewsasia.com/asia")
    time.sleep(3)
    # You need to inspect CNA HTML for correct selector; here is a generic one
    items = driver.find_elements(By.CSS_SELECTOR, "h3, h2, a")  
    texts = [i.text.strip() for i in items if i.text.strip()]
    return texts

def unique_clean(headlines):
    cleaned = []
    seen = set()
    for h in headlines:
        lower = h.lower()
        if lower not in seen:
            seen.add(lower)
            cleaned.append(h)
    return cleaned

def save_csv(rows, folder, prefix):
    os.makedirs(folder, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"{prefix}_{ts}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "headline"])
        writer.writerows(rows)
    return path

def save_pdf(rows, folder, prefix):
    os.makedirs(folder, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"{prefix}_{ts}.pdf")
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=letter)
    flow = []
    for src, text in rows:
        flow.append(Paragraph(f"<b>{src.upper()}</b>: {text}", styles["Normal"]))
        flow.append(Spacer(1, 8))
    doc.build(flow)
    return path

def main():
    all_rows = []

    # 1. Try scraping via RSS
    try:
        xml = fetch_rss(CNA_RSS_ASIA)
        cna_headlines = parse_cna_rss(xml)
        cna_headlines = unique_clean(cna_headlines)
        for h in cna_headlines:
            all_rows.append(("cna", h))
        print(f"Fetched {len(cna_headlines)} CNA headlines from RSS")
    except Exception as e:
        print("RSS fetch failed, falling back to Selenium:", e)
        driver = get_driver()
        fallback = scrape_cna(driver)
        fallback = unique_clean(fallback)
        for h in fallback:
            all_rows.append(("cna", h))
        driver.quit()

    # Save results
    if not all_rows:
        print("No CNA headlines found.")
        return

    csv_path = save_csv(all_rows, "outputs", "cna_headlines")
    pdf_path = save_pdf(all_rows, "outputs", "cna_headlines")

    print("Saved CSV:", csv_path)
    print("Saved PDF:", pdf_path)

if __name__ == "__main__":
    main()