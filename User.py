import csv, json, logging
from pathlib import Path
import hashlib
# from Products import Products
import pandas as pd


my_logger = logging.getLogger('user_logger')
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


class User:

    def __init__(self, username, name, password, phone_number, access_level='customer', status='Active'):
        """
        :param access_level: user's access level : admin or customer
        :param username: user's username
        :param password: user's password
        :param name: user's name
        :param phone_number: user's phone number
        """
        self.access_level = access_level
        self.username = username
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.status = status

    @staticmethod
    def check_username(user_info, file_name):
        if Path(file_name).is_file():
            df = pd.read_csv(file_name, delimiter=',')
            if user_info in df.values:
                return False
            else:
                return True
        else:
            return True
    # def check_username(user_info, user_lst):
    #     for user in user_lst:
    #         if user['username'] == user_info[1]:
    #             return False
    #     return True

    @staticmethod
    def create_account(user_info, file_name):
        with open(file_name, 'a', newline='') as f:
            fields_name = ['username', 'name', 'password', 'phone_number', 'access_level', 'status']
            csv_writer = csv.DictWriter(f, fieldnames=fields_name)
            if Path(file_name).stat().st_size == 0:
                csv_writer.writeheader()
            csv_writer.writerow({'username': user_info.username,
                                 'name': user_info.name,
                                 'password': hashlib.md5(user_info.password.encode()).hexdigest(),
                                 'phone_number': user_info.phone_number,
                                 'access_level':user_info.access_level,
                                 'status': user_info.status})

    @staticmethod
    def login(file_name, username, password):
        with open(file_name, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                if row['username'] == username and \
                        row['password'] == hashlib.md5(password.encode()).hexdigest() and row['status'] == 'Active':
                    return True
        return False

    @staticmethod
    def chang_pass(file_name, *args):
        df = pd.read_csv(file_name)
        location = 0
        with open(file_name, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                if row['username'] == args[0] and row['password'] == args[1]:
                    df.loc[location, 'password'] = args[2]
                    df.to_csv(file_name, index=False)
                    print('password is changed.')
                location += 1


class Admin(User):
    admins_identification = 'admin_123'

    def __init__(self, username, name, password):
        """
        :param username: username of admin
        :param name: name of admin
        :param password: password of admin
        """
        super().__init__(username, name, password, 0, 'admin', 'Active')

    @staticmethod
    def change_status(username, status, file_name):
        df = pd.read_csv(file_name)
        location = 0
        with open(file_name, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                if row['username'] == username:
                    df.loc[location, 'status'] = status
                    df.to_csv(file_name, index=False)
                location += 1
        return True

    # @staticmethod
    # def create_account(user_info, file_name):
    #     with open(file_name, 'a', newline='') as f:
    #         fields_name = ['username', 'name', 'password']
    #         csv_writer = csv.DictWriter(f, fieldnames=fields_name)
    #         if Path(file_name).stat().st_size == 0:
    #             csv_writer.writeheader()
    #             csv_writer.writerow({'username': user_info.username,
    #                                  'name': user_info.name,
    #                                  'password': hashlib.md5(user_info.password.encode()).hexdigest()})

    # @staticmethod
    # def login(file_name, username, password):
    #     with open(file_name, 'r') as f:
    #         csv_reader = csv.DictReader(f)
    #         for row in csv_reader:
    #             if row['username'] == username and row['password'] == hashlib.md5(password.encode()).hexdigest():
    #                 return True
    #     return False
        # def login(users_list, username, password):
    #     for user in users_list:
    #         if user[0] == username and user[2] == hashlib.md5(password.encode()).hexdigest():
    #             return True
    #     return False

    @staticmethod
    def add_product(product_info):
        with open('Products_Inventory.csv', 'a', newline='') as f:
            fields = ['barcode', 'name', 'brand', 'price', 'stock']
            csv_writer = csv.DictWriter(f, fieldnames=fields)
            if Path('Products_Inventory.csv').stat().st_size == 0:
                csv_writer.writeheader()
            csv_writer.writerow({'barcode': product_info[0], 'name': product_info[1],
                                 'brand': product_info[2], 'price': product_info[3],
                                 'stock': product_info[4]})
        return True

    @staticmethod
    def view_invoices():
        """
        :return: admin can view invoices of customers base their date.
        """
        with open('Orders_invoices.json') as f:
            df = pd.DataFrame([json.loads(l) for l in f.readlines()])
        print(df)


class Customer(User):
    def __init__(self, username, name, password, phone_number):
        self.username = username
        self.name = name
        self.password = password
        self.phone_number = phone_number
        super().__init__(username, name, password, phone_number, 'customer', 'Active')

    @staticmethod
    def ordering(product, numbers):
        try:
            with open('Products_Inventory.csv', 'r') as f:
                csv_reader = csv.DictReader(f)
                line = 0
                for row in csv_reader:
                    if line == int(product):
                        assert int(row['stock']) > int(numbers)
                        return {'name': row['name'],
                                'brand': row['brand'],
                                'price(for one)': row['price'],
                                'number': int(numbers),
                                'total price': int(row['price']) * int(numbers)}
                    line += 1
        except AssertionError:
            my_logger.error('Inventory is not enough!', exc_info=True)
            return False

