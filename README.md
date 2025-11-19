📰 News Headline Harvester (CNA Asia Focus)

A robust Python script designed for reliable, structured data acquisition of current news headlines. This project prioritizes efficiency by using direct RSS feed consumption, with a robust fallback mechanism using Selenium for dynamic content or structural changes.

🚀 Key Features

Dual Extraction Strategy: Primary data extraction via the clean, fast CNA Asia RSS feed. Includes a Selenium fallback for resilience against anti-bot measures or if the RSS feed is unavailable.

Structured Output: Automatically organizes scraped headlines into two essential formats:

CSV: Ready for data analysis, databases, or spreadsheet manipulation.

PDF Report: A cleanly formatted document for easy reporting and archival using the reportlab library.

Data Hygiene: Implements duplicate removal and cleaning functions (unique_clean) to ensure data integrity.

Timestamped Archiving: All output files are timestamped and saved into an isolated outputs folder, ensuring a clean project structure and historical data preservation.

🛠️ Technologies & Prerequisites

This project is built using Python and requires the following libraries:

Library

Purpose

requests

Handles HTTP communication (fetching RSS feeds).

xml.etree.ElementTree

Standard library for parsing XML/RSS feed data.

selenium

Browser automation (required for the web scraping fallback).

reportlab

Generates professional PDF reports.

csv, os, datetime

Standard libraries for file handling and timestamps.

Installation

Clone the Repository:

git clone [https://github.com/Keerthana093/Web-Scraper-for-News-Headline.git]
cd YourRepoName


Install Dependencies:
You will need to install the external libraries used in the script.

pip install requests selenium reportlab


Setup WebDriver (for Selenium Fallback):
If the RSS feed fails, the script requires the Chrome WebDriver. Ensure you have Google Chrome installed and the corresponding ChromeDriver binary is in your system's PATH, or accessible by the script.

⚡ How to Run

Execute the script directly from your terminal:

python newsscraper.py


Expected Output

Upon successful execution, the script will display a log of the action taken and where the files were saved:

Fetched 20 CNA headlines from RSS
Saved CSV: outputs\cna_headlines_20251119_142433.csv
Saved PDF: outputs\cna_headlines_20251119_142433.pdf


The output files will be automatically generated inside the newly created outputs folder, categorized by the current date and time.

📁 Project Structure

The project maintains a clean and organized directory structure:

webscraper/
├── newsscraper.py      # Main Python scraper script
├── outputs/            # Folder where all CSV and PDF reports are saved
│   ├── cna_headlines_20251119_142433.csv
│   └── cna_headlines_20251119_142433.pdf
└── README.md


⚠️ Ethical & Legal Considerations

This project adheres to ethical scraping guidelines:

Politeness: The RSS feed is a clean, server-friendly method. The Selenium fallback uses a time delay (time.sleep(3)) to minimize server load.

Target: The script targets publicly available content and is intended for personal use, data analysis, or reporting purposes.
