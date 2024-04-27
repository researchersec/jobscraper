import requests
import os
from bs4 import BeautifulSoup
import re
import json

URL = "https://www.jobindex.dk/jobsoegning/it/itdrift/region-nordjylland"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_="jobsearch-result")

# Define a function to extract the publication date from a result
def get_pub_date(result):
    pub_element = result.find("div", class_="jix-toolbar__pubdate")
    if pub_element:
        text_with_extra_spaces = pub_element.get_text()
        pub_date = re.sub(r'\s+', ' ', text_with_extra_spaces).strip("Indrykket: ")
        return pub_date
    return ""

# Sort the results by publication date
results_sorted = sorted(results, key=lambda result: get_pub_date(result), reverse=True)

# List to store job listings
job_listings = []

for result in results_sorted:
    title_element = result.find("h4").find("a") if result.find("h4") else None
    company_element = result.find("div", class_="jix-toolbar-top__company")
    location_element = (
        result.find("div", class_="jobad-element-area").find("span")
        if result.find("div", class_="jobad-element-area")
        else None
    )
    link_element = result.find("a", class_="btn btn-sm btn-block btn-primary d-md-none mt-2 seejobmobil")
    
    if (
        title_element is not None
        and company_element is not None
        and location_element is not None
    ):
        title = title_element.text.strip() if title_element else ""
        company = (
            company_element.find("a").text.strip()
            if company_element.find("a")
            else ""
        )
        location = location_element.text.strip()
        job_URL = link_element.get("href")
        pub_date = get_pub_date(result)
        
        job_listing = {
            "pub_date": pub_date,
            "title": title,
            "company": company,
            "location": location,
            "job_URL": job_URL
        }
        job_listings.append(job_listing)

        # Write to README.md
    with open("it/README.md", "w", encoding="utf-8") as file:
        file.write(f"# {title}\n")
        file.write(f"{pub_date}\n\n")
        file.write(f"{company}\n\n")
        file.write(f"{location}\n\n")
        file.write(f"Job URL: [link]({job_URL})\n\n\n")

# Write to JSON file
with open("it/data.json", "w") as json_file:
    json.dump(job_listings, json_file, indent=4, ensure_ascii=False)
