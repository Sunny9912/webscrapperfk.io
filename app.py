from flask import Flask, request, render_template, send_from_directory
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        num_pages = int(request.form["num_pages"])
        file_name = request.form["file_name"]
        scraping_option = request.form["scraping_option"]

        if scraping_option == "rows_and_columns":
            scrape_rows_and_columns(url, num_pages, file_name)
        elif scraping_option == "columns_only":
            scrape_columns_only(url, num_pages, file_name)

        return send_from_directory("Downloads", f"{file_name}.csv", as_attachment=True)

    return render_template("index.html")

def scrape_rows_and_columns(url, num_pages, file_name):
    Names = []
    Prices = []
    Reviews = []

    for i in range(1, num_pages + 1):
        page_url = f"{url}&page={i}"
        r = requests.get(page_url)

        soup = BeautifulSoup(r.text, "html.parser")
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        names = box.find_all("a", class_="s1Q9rs")
        prices = box.find_all("div", class_="_30jeq3")
        reviews = box.find_all("div", class_="_3LWZlK")

        min_length = min(len(names), len(prices), len(reviews))

        for i in range(min_length):
            product_name = names[i].text if i < len(names) else "NA"
            product_price = prices[i].text if i < len(prices) else "NA"
            product_review = reviews[i].text if i < len(reviews) else "NA"

            Names.append(product_name)
            Prices.append(product_price)
            Reviews.append(product_review)

    df = pd.DataFrame({"Product Name": Names, "Product Price": Prices, "Ratings": Reviews})
    df.to_csv(f"Downloads/{file_name}.csv", index=False)

def scrape_columns_only(url, num_pages, file_name):
    Names = []
    Prices = []
    Desc = []
    Reviews = []

    for i in range(1, num_pages + 1):
        page_url = f"{url}&page={i}"
        r = requests.get(page_url)

        soup = BeautifulSoup(r.text, "html.parser")
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        names = box.find_all("div", class_="_4rR01T")
        prices = box.find_all("div", class_="_30jeq3 _1_WHN1")
        desc = box.find_all("ul", class_="_1xgFaf")
        reviews = box.find_all("div", class_="_3LWZlK")

        max_length = max(len(names), len(prices), len(desc), len(reviews))

        for j in range(max_length):
            name = names[j].text if j < len(names) else 'NA'
            price = prices[j].text if j < len(prices) else 'NA'
            description = desc[j].text if j < len(desc) else 'NA'
            review = reviews[j].text if j < len(reviews) else 'NA'

            Names.append(name)
            Prices.append(price)
            Desc.append(description)
            Reviews.append(review)

    df = pd.DataFrame({"Product Name": Names, "Product Price": Prices, "Description": Desc, "Ratings": Reviews})
    df.to_csv(f"Downloads/{file_name}.csv", index=False)

if __name__ == "__main__":
    app.run(debug=True)
