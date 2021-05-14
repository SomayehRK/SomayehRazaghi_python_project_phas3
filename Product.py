import csv, json, logging
import pandas as pd
from pathlib import Path
from datetime import date
import numpy as np
from random import randint


my_logger = logging.getLogger('product_logger')
my_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('File_log.log')
# std_handler = logging.StreamHandler()
file_handler.setLevel(logging.DEBUG)
# std_handler.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s -%(name)s- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)
# std_handler.setFormatter(log_format)
my_logger.addHandler(file_handler)
# my_logger.addHandler(std_handler)


def my_converter(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, datetime.datetime):
        return obj.__str__()


class Product:
    def __init__(self, barcode, name, brand, price, stock):
        """
        :param barcode: product's barcode
        :param name: product's name
        :param brand: product's brand
        :param price: product's price
        :param stock: product's stock
        """
        self.barcode = barcode
        self.name = name
        self.brand = brand
        self. price = price
        self.stock = stock

    @staticmethod
    def display():
        """
        :param goods_info_file: The goods information file
        :return: a table containing the product name, brand and price of each unit is displayed to the customer.
        """
        try:
            df = pd.read_csv('Products_Inventory.csv')
            show_list = df.loc[:, ['name', 'brand', 'price']]
            print(show_list)
            # return show_list
        except FileNotFoundError:
            print('there are not any products in store.\n')
            # return False

    @staticmethod
    def update_inventory(customer_order_list):
        df = pd.read_csv('Products_Inventory.csv')
        with open('Products_Inventory.csv', 'r') as f:
            csv_reader = csv.DictReader(f)
            for item in customer_order_list:
                location = 0
                for row in csv_reader:
                    if item['name'] == row['name'] and item['brand'] == row['brand']:
                        df.loc[location, 'stock'] = int(row['stock']) - int(item['number'])
                        df.to_csv('Products_Inventory.csv', index=False)
                        break
                    location += 1
                f.seek(0)
                next(csv_reader)

    @staticmethod
    def record_orders(customer_order_list, customer_info, total_purchase_price):
        if Path('Orders_invoices.json').is_file():
            orders = {randint(100, 999): {'date': str(date.today()), 'username': customer_info,
                                          'orders': customer_order_list,
                                          'total_price': total_purchase_price}}
            with open('Orders_invoices.json', 'r+') as f:
                data = json.load(f)
                data.update(orders)
                f.seek(0)
                json.dump(data, f, default=my_converter)
        else:
            orders = {randint(100, 999): {'date': str(date.today()), 'username': customer_info,
                                          'orders': customer_order_list,
                                          'total_price': total_purchase_price}}
            with open('Orders_invoices.json', 'w') as write_f:
                json.dump(orders, write_f, default=my_converter)

    @staticmethod
    def check_inventory():
        finishing_products = []
        with open('Products_Inventory.csv', 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                if int(row['stock']) == 0:
                    print(row['name'])
                    finishing_products.append({row['name']: row['brand']})
                    my_logger.info(f"{row['name']} from brand {row['brand']} is finished", exc_info=True)
        print(finishing_products)
        return finishing_products

