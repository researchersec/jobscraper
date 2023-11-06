import requests
import os
from bs4 import BeautifulSoup
import re

#fi
criteria = "it-support"

URL = f"https://www.jobindex.dk/jobsoegning/it/itdrift/region-nordjylland?q={criteria}&subid=1&subid=4&subid=6&subid=7&subid=93"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_="jobsearch-result")


with open("it/README.md", "w", encoding="utf-8") as file:
    for result in results:
        title_element = result.find("h4").find("a") if result.find("h4") else None
        company_element = result.find("div", class_="jix-toolbar-top__company").find("a")
        location_element = result.find("div", class_="jobad-element-area").find("span") if result.find("div", class_="jobad-element-area") else None
        link_element = result.find("a", class_="btn btn-sm btn-primary")
        pub_element = result.find("div", class_="jix-toolbar__pubdate")

        if title_element is not None and company_element is not None and location_element is not None:
            title = title_element.text.strip()
            company = company_element.text.strip()
            location = location_element.text.strip()
            job_URL = link_element.get("href")

            text_with_extra_spaces = pub_element.get_text()
            pub_date = re.sub(r'\s+', ' ', text_with_extra_spaces).strip("Indrykket: ")

            file.write(f"# {title}\n")
            file.write(f"{pub_date}\n\n")
            file.write(f"{company}\n\n")
            file.write(f"{location}\n\n")
            file.write(f"Job URL: [link]({job_URL})\n\n\n")
