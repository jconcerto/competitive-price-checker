from os import write
import yaml
import csv
from pathlib import Path
from datetime import datetime

import utils.htmlparser as htmlparser

fixed_width = 10

HTML_REQUEST_INTERVAL = 10
HTML_REQUEST_TIMEOUT = 5
HTML_REQUEST_RETRIES = 2
TERMINATE_ON_FAILED_REQUEST = False

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def main():


    with open('product.yaml', 'r') as productfile:
        productfile = yaml.load(productfile)
        
    header   = []
    csv_rows = []
    for item in productfile:
        product_data = productfile[item]
        tree         = htmlparser.get_html_tree(product_data['url'])
        row      = dict()
        for csv_column_name in product_data['csv_data']:
            if csv_column_name not in header: header.append(csv_column_name)
            csv_column_value = product_data['csv_data'][csv_column_name]
            csv_column_value = htmlparser.convert_to_value(tree, csv_column_value)
            row[csv_column_name] = csv_column_value
        csv_rows.append(row)


    Path("results").mkdir(parents=True, exist_ok=True)
    with open('results/{}.csv'.format(datetime.now().strftime("%m-%d-%Y")), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(csv_rows)
    

def sort_csv_elements(csv_elems):
    return csv_elems
    
if __name__ == "__main__":
    main()