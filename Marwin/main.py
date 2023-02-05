import json
import random
import time

import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    project_data_list = []

    for item in range(3, 92):
        req = requests.get(url + f"?p={item}", headers)

        folder_name = f"data/data_{item}"
        with open("projects.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        lis = soup.find_all("li", class_="item product product-item")
        projects_urls = []
        for li in lis:
            project_url = li.find("div", class_="product-item-info").find("a").get("href")
            projects_urls.append(project_url)

        for project_url in projects_urls:
            req = requests.get(project_url, headers)
            project_name = project_url.split("/")[-1]

            with open(f"{folder_name}/{project_name}", "w") as file:
                file.write(req.text)

            with open(f"{folder_name}/{project_name}", "w") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")
            project_data = soup.find("div", class_="column main")

            project_name = project_data.find("div", class_="product-info-title").find("h1").text
            project_code = project_data.find("div", class_="value").text
            project_price = project_data.find("div", class_="product-info-title").find("span", class_="price").text
            project_attributes = project_data.find("div",
                                                   class_="additional-attributes-wrapper table-wrapper").find_all("tr")
            project_stock = project_data.find("div", class_="product-info-stock-sku").find("span").text
            project_rating = project_data.find("div", class_="rating-summary").find("span", class_="value").text

            project_data_list.append(
                {
                    "Product Name": project_name,
                    "Code": project_code,
                    "Price": project_price,
                    "Attributes": project_attributes,
                    "Stock": project_stock,
                    "Rating": project_rating
                }
            )
            time.sleep(random.randrange(2, 4))
    with open("data/projects_data.json", "a", encoding="utf-8") as file:
        json.dump(project_data_list, file, indent=4, ensure_ascii=False)


get_data("https://www.marwin.kz/toys-and-entertainment/lego/")
