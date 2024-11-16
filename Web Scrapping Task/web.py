import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# Define headers to mimic a browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Base URL of Yellow Pages
BASE_URL = "https://www.yellowpages.com/search?search_terms=Financial%20Services&geo_location_terms=CA"

# Function to extract company details from the detailed page
def scrape_company_details(company_url):
    response = requests.get(company_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: Unable to access {company_url} (Status Code: {response.status_code})")
        return {}

    soup = BeautifulSoup(response.content, "html.parser")
    details = {}

    try:
        details["Company Name"] = soup.select_one("h1.business-name").text.strip()
        
        # Extract contact number from <span class="full">
        contact_tag = soup.select_one("span.full")
        details["Contact Number"] = contact_tag.text.strip() if contact_tag else "N/A"
        
        details["Website URL"] = soup.select_one("a.website-link")["href"].strip() if soup.select_one("a.website-link") else "N/A"
        
        # Handle nested address structure
        address_tag = soup.select_one("span.address")
        if address_tag:
            address_parts = [part.text.strip() for part in address_tag.find_all("span")]  # Extract nested spans
            details["Location/Address"] = " ".join(address_parts) + " " + address_tag.get_text(strip=True).replace("".join(address_parts), "").strip()
        else:
            details["Location/Address"] = "N/A"

        details["Email Address"] = soup.select_one("a.email-business")["href"].replace("mailto:", "").strip() if soup.select_one("a.email-business") else "N/A"
        
        # Extract company description from <dd class="general-info">
        general_info_tag = soup.select_one("dd.general-info")
        details["Company Description"] = general_info_tag.text.strip() if general_info_tag else "N/A"

        # Extract industry/category from <div class="categories">
        categories_div = soup.select_one("div.categories")
        if categories_div:
            categories = [category.text.strip() for category in categories_div.find_all("a")]
            details["Industry/Category"] = ", ".join(categories)
        else:
            details["Industry/Category"] = "N/A"
    
    except Exception as e:
        print(f"Error parsing details from {company_url}: {e}")

    return details

# Function to extract links to company pages from a single search results page
def scrape_search_results(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: Unable to access {url} (Status Code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    company_links = []

    try:
        results = soup.select("a.business-name")
        for result in results:
            company_links.append("https://www.yellowpages.com" + result["href"])
    except Exception as e:
        print(f"Error parsing search results: {e}")

    return company_links

# Scrape data from multiple pages
def scrape_directory(base_url, pages=5):
    all_companies = []
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        search_url = f"{base_url}&page={page}"
        company_links = scrape_search_results(search_url)

        for company_url in company_links:
            print(f"Scraping details for {company_url}...")
            details = scrape_company_details(company_url)
            if details:
                all_companies.append(details)

            # Add a delay between requests to avoid being blocked
            time.sleep(random.uniform(2, 5))

    return all_companies

# Save data to a CSV file
def save_to_csv(data, filename="F:/companies.csv"):
    keys = ["Company Name", "Contact Number", "Website URL", "Location/Address", "Email Address", "Company Description", "Industry/Category"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data successfully saved to {filename}")

# Main script execution
if __name__ == "__main__":
    try:
        scraped_data = scrape_directory(BASE_URL, pages=5)
        if scraped_data:
            save_to_csv(scraped_data)
        else:
            print("No data scraped. Please check the target URL or the website structure.")
    except Exception as e:
        print(f"An error occurred: {e}")
