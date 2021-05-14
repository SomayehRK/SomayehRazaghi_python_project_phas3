from User import User, Admin, Customer
import csv, hashlib, logging
from Product import Product
import pandas as pd


my_logger = logging.getLogger('customer_logger')
my_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('File_log.log')
file_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(levelname)s -%(name)s- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(log_format)
my_logger.addHandler(file_handler)


def customer_menu():
    """

    :return: customer operation menu
    """
    while True:
        print("========================================\n"
              "pleas login or create admin account\n"
              "========================================\n"
              "1. create account\n"
              "2. login\n"
              "3. Active account\n"
              "4. back\n")
        choice = input('Enter choice: ')
        try:
            choice = int(choice)
        except ValueError:
            print("That's not an int!")
            continue

        if choice == 1:
            customer_info = input("========================================\n"
                                  "please enter these information\n"
                                  "========================================\n"
                                  "your full name | an username | a password | phone number :").split('|')
            customer_exist = User.check_username(customer_info[1], 'Customers_info.csv')
            if customer_exist:
                customer = Customer(customer_info[1], customer_info[0], customer_info[2], customer_info[3])
                User.create_account(customer, 'Customers_info.csv')
            else:
                print('this username already exists!')

        elif choice == 2:
            username = input('username:')
            customer_exist = User.check_username(username, 'Customers_info.csv')
            if not customer_exist:
                cnt = 0
                while cnt < 3:
                    password = input('password:')
                    pass_correct = User.login('Customers_info.csv', username, password)
                    if pass_correct:
                        print(f'welcome dear {username}.\n')
                        logout = False
                        while True:
                            print('========================================\n'
                                  'please select a part.\n'
                                  '========================================\n'
                                  '1. shopping\n'
                                  '2.change password\n'
                                  '3. logout\n')
                            part = input('enter a choice:')

                            try:
                                part = int(part)
                            except ValueError:
                                print("That's not an int!")
                                continue
                            if part == 1:
                                print('\n========================================\n'
                                      'list of our products\n'
                                      '========================================\n')
                                Product.display()
                                print('========================================\n')
                                order_list = []
                                while True:
                                    item, numbers = input('which item(enter column number), how many : ').split(',')
                                    order = Customer.ordering(item, numbers)
                                    if order is False:
                                        print('Inventory is not enough!')
                                    else:
                                        order_list.append(order)
                                        select = int(input('1 - continue | 2 - finish :'))
                                        if select == 2:
                                            break
                                df = pd.DataFrame(order_list,
                                                  columns=['name', 'brand', 'price(for one)', 'number', 'total price'])
                                total_price = sum([x['total price'] for x in order_list])
                                print('-' * 92)
                                print(f'your order list :\n{df}')
                                print('-' * 53)
                                print(f'your total price is : {total_price}')
                                print('-' * 92)

                                confirm = int(input('1 - confirm | 2 - discard :'))
                                if confirm == 1:
                                    my_logger.info('new invoice', exc_info=True)
                                    Product.update_inventory(order_list)
                                    Product.record_orders(order_list, username, total_price)

                            elif part == 2:
                                old_pass = hashlib.md5(input('enter password:').encode()).hexdigest()
                                new_pass = hashlib.md5(input('enter new password:').encode()).hexdigest()
                                User.chang_pass('Customers_info.csv', username, old_pass, new_pass)
                                my_logger.info('customer change password', exc_info=True)

                            elif part == 3:
                                logout = True
                                break
                            else:
                                print('Invalid input.\n')
                        if logout:
                            break
                    else:
                        print('password is wrong. please try again.')
                        cnt += 1
                if cnt == 3:
                    change_status = Admin.change_status(username, 'Deactivate', 'Customers_info.csv')
                    if change_status:
                        my_logger.info('locked user', exc_info=True)
                        print('your account is locked. please send request to admin.')
            else:
                print('this username does not exist. please create an account.')
        elif choice == 3:
            username = input('username:')
            customer_exist = User.check_username(username, 'Customers_info.csv')
            if not customer_exist:
                change_status = Admin.change_status(username, 'Active', 'Customers_info.csv')
                if change_status:
                    my_logger.info('active user', exc_info=True)
                    print('your account is active now. please login.')
        elif choice == 4:
            break
        else:
            print('Invalid input.\n')
