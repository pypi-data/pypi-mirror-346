from typing import List
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time  # For rate limiting


def scrape_to_csv(
        urls: List[str], tags: List[str], write_to_csv: bool = True, output_file: str = "scraped_data.csv",
        return_structured_data: bool = False, headless: bool = True):
    """
    Scrapes data from multiple URLs using Selenium and BeautifulSoup, returns a Pandas DataFrame,
    optionally saves it to a CSV file and optionally returns the structured data.

    Args:
        urls: A list of URLs to scrape.
        tags: A list of CSS selectors to extract data from.
        write_to_csv: Write returned data into a CSV file.
        output_file: The name of the CSV file to save the data to.
        return_structured_data: If True, returns the scraped data in its original nested list format.
        headless: If True, runs Chrome in headless mode (no GUI).
    """
    # Setup Chrome options
    options = Options()
    if headless:
        options.add_argument("--headless")  # Run in headless mode (no GUI)

    # Initialize Chrome with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    results = []

    try:
        for url in urls:
            driver.get(url)
            print(f"Scraping: {url}")
            row = {'url': url}
            for tag in tags:
                try:
                    # Wait for elements to be present (dynamic content)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag))
                    )
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    elements = soup.select(tag)
                    row[tag] = [el.get_text(strip=True) for el in elements]
                except Exception as e:
                    print(f"Error finding elements with tag '{tag}' on {url}: {e}")
                    row[tag] = []
            results.append(row)
            time.sleep(1)

        # Grouped by URL and tag, stored as lists of strings
        grouped_data = []
        for row in results:
            grouped_row = {'url': row['url']}
            for tag in tags:
                # Join multiple elements into a single string (separated by a comma)
                grouped_row[tag] = ', '.join(row[tag])
            grouped_data.append(grouped_row)

        df = pd.DataFrame(grouped_data)
        if write_to_csv:
            df.to_csv(output_file, index=False)
            print(f"Data written to {output_file}")
        else:
            print(df)

        if return_structured_data:
            print(results)

    finally:
        driver.quit()
