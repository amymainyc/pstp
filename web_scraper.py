import json
from bs4 import BeautifulSoup
import mechanicalsoup as ms

types = [("american-darling", 45)]

'''
login to american darling 
returns: StatefulBrowser object
'''
def login():
    with open("credentials.json") as f:
        creds = json.load(f)

    browser = ms.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
    )

    browser.open("https://americandarlingbag.com/account/login?")
    browser.select_form(nr=0)
    browser["customer[email]"] = creds["email"]
    browser["customer[password]"] = creds["password"]
    resp = browser.submit_selected()
    return browser

'''
scrape the listing data for each category and page
requires: browser (StatefulBrowser), category, page
'''
def scrape_price_and_images(browser, category, page):
    browser.open(f"https://americandarlingbag.com/collections/{category}?page={page}")
    soup = browser.page

    with open("items.json") as f:
        data = json.load(f)

    products = soup.findAll("div", class_="product-details")
    for p in products:
        code = p.span.string
        price = p.find(class_="price-box").span.string
        if not code in data:
            data[code] = []
        data[code].append(price)

    pics = soup.findAll("picture")
    for p in pics:
        code = p.img["alt"]
        if not code in data:
            data[code] = []
        images = p.img["data-srcset"].split("\n")
        i = images[-1].strip()[2:]
        if not i in data[code]:
            data[code].append(i)

    with open("items.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    b = login()
    for t in types:
        c = t[0]
        pages = t[1]
        for p in range(pages+1):
            print(f"{c}: page {p}")
            scrape_price_and_images(b, c, p)


hours_worked = 2