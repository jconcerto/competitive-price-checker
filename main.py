from os import write
from urllib.request import urlopen
import yaml
import csv
from pathlib import Path
from datetime import datetime

header = ['brand', 'category', 'subcategory', 'set', 'name', 'sku', 'vendor', 'price']
fixed_width = 10

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def main():

    with open('product.yaml', 'r') as productfile:
        products = yaml.load(productfile)

    with open('competitors.yaml', 'r') as competitorfile:
        competitors = yaml.load(competitorfile)
    
    for brand in products:
        csv_results = []

        product_details = products[brand]
        brand_name = product_details['name']

        for series_key in product_details['sets']:
            series = product_details['sets'][series_key]
            set_name = series['name']
            category_name = series['tag']
            for product_key in series['products']:
                product = series['products'][product_key]
                proudct_name = product['name']
                subcategory_name = product['tag']
                sku = product['sku']
                
                for competitor_key in competitors:
                    competitor = competitors[competitor_key]
                    competitor_name = competitor['name']
                    website_prefix = competitor['website']
                    starting_string = competitor['starting_string']
                    competitor_products = competitor[brand][series_key]
                    # for competitor_product_key in competitor_products:
                    if product_key in competitor_products:
                        product_url = competitor_products[product_key]
                        url = "{0}{1}".format(website_prefix, product_url)
                        page = urlopen(url)
                        html = page.read().decode('utf-8')

                        start = html.find(starting_string) + len(starting_string)
                        raw_string = html[start:(start+fixed_width)]
                        
                        for n in range(1, 10):
                            if not is_number(raw_string[0:n]):
                                break
                            else:
                                n = n+1

                        price = float(raw_string[:n-1])
                        # price = raw_string[:n-1]

                        row = [brand_name, category_name, subcategory_name, set_name, proudct_name, sku, competitor_name, price]
                        csv_results.append(row)

        Path("results").mkdir(parents=True, exist_ok=True)
        with open('results/{}.csv'.format(datetime.now().strftime("%m-%d-%Y")), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(csv_results)
        # print(csv_results)



if __name__ == "__main__":
    main()