import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry

max_retries = 20
backoff_factor = 0.8

retry_strategy = Retry(
    total=max_retries,
    backoff_factor=backoff_factor,
    status_forcelist=[500, 502, 503, 504]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount('http://', adapter)
session.mount('https://', adapter)

html_text = session.get("https://www.nykaa.com/personal-care-landing-page/c/12930").text
print("Ready to scrap personal care items from nykaa.")
print("")
soup = BeautifulSoup(html_text, "lxml")
total_products = soup.find("h1", class_ = "css-mrgb7e")
total_product = int(total_products.span.text.replace("(", "").replace(")", ""))
print("There are {} available in personal care products.".format(total_product))
print("")
total_pages = soup.find("div", class_ = "css-fn0ggt")
total_page = int(total_pages.span.text.split(" ")[-1])
print("There are {} pages to scrap for personal care products.".format(total_page))
print("")

product_name = []
original_price = []
offer_price = []
offer_percentage = []
extra_offer = []
shade_or_size = []
featured = []
best_seller = []

print("But we are going to scrap 350 pages in personal care!!!!")
print("")
for i in range(1, 351):
    html_text = session.get("https://www.nykaa.com/personal-care-landing-page/c/12930?page_no={}".format(i)).text
    print("Scraping the page {} of personal care product.".format(i))
    print("")
    soup = BeautifulSoup(html_text, "lxml")
    products = soup.find_all("div", class_ = "productWrapper css-xin9gt")

    if products:
        for j in products:
            names = j.find_all("div", class_ = "css-xrzmfa")
            prices = j.find_all("span", class_ = "css-17x46n5")
            offer_prices = j.find_all("span", class_ = "css-111z9ua")
            offer_percentages = j.find_all("div", class_ = "css-1d0jf8e")
            extra_offers = j.find_all("div", class_ = "css-1rd7vky")
            shades_or_sizes = j.find_all("div", class_ = "css-a7hmoe")
            featured_best_seller = j.find_all("div", class_ = "css-wkluxr")
            
            if names:
                for k in names:
                    try:
                        name = k.text
                        product_name.append(name)
                    except:
                        product_name.append("Not available")

            if prices:
                for k in prices:
                    try:
                        price = int(k.span.text.replace("₹", ""))
                        original_price.append(price)
                    except:
                        original_price.append("Not available")

            if offer_prices:
                for k in offer_prices:
                    try:
                        off_price = int(k.text.replace("₹", ""))
                        offer_price.append(off_price)
                    except:
                        offer_price.append("Not available")

            if offer_percentages:
                for k in offer_percentages:
                    offer_percent = k.find_all("span")[-1]
                    try:
                        off_percent = offer_percent.text
                        if "%" in off_percent:
                            off = int(off_percent.replace("% Off", ""))
                            offer_percentage.append(off)
                        else:
                            offer_percentage.append("Not available")
                    except:
                        offer_percentage.append("Not available")

            if extra_offers:
                for k in extra_offers:
                    try:
                        extra_off = k.p.text
                        extra_offer.append(extra_off)
                    except:
                        extra_offer.append("Not available")
                
            if shades_or_sizes:
                for k in shades_or_sizes:
                    try:
                        sha_or_siz = k.text
                        if sha_or_siz != "":
                            shade_or_size.append(sha_or_siz)
                        else:
                            shade_or_size.append("Not available")
                    except:
                        shade_or_size.append("Not available")

            if featured_best_seller:
                for k in featured_best_seller:
                    try:
                        fea_sell = k.ul.text
                        if len(fea_sell) == 8 and fea_sell == "FEATURED":
                            featured.append(fea_sell)
                            best_seller.append("Not available")
                        elif len(fea_sell) == 10 and fea_sell == "BESTSELLER":
                            featured.append("Not available")
                            best_seller.append(fea_sell)
                        elif len(fea_sell) == 18 and fea_sell == "FEATUREDBESTSELLER":
                            featured.append("FEATURED")
                            best_seller.append("BESTSELLER")
                        else:
                            featured.append("Not available")
                            best_seller.append("Not available")
                    except:
                        featured.append("Not available")
                        best_seller.append("Not available")
    
    print("Completely scraped the page {}.".format(i))
print("")
print("Completed !!!!")
print("")

print(len(product_name))
print(len(original_price))
print(len(offer_price))
print(len(offer_percentage))
print(len(extra_offer))
print(len(shade_or_size))
print(len(featured))
print(len(best_seller))

print("Converting into Dataframe !!!")
print("")

personal_care_dictionary = {"Product_name" : product_name,
                            "Original_price" : original_price,
                            "Offer_price" : offer_price,
                            "Offer_percentage" : offer_percentage,
                            "Extra_offer" : extra_offer,
                            "Shades_and_sizes" : shade_or_size,
                            "Featured_product" : featured,
                            "Best_seller_product" : best_seller}

personal_care_data = pd.DataFrame(personal_care_dictionary)
print(personal_care_data.head())
print("")
print(personal_care_data.tail())
print("")
print(personal_care_data.shape)
print("")
personal_care_data.to_csv("Nykaa_personal_care_data.csv")