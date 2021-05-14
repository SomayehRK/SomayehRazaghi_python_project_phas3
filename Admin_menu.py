from User import User, Admin
import csv, hashlib, logging
from Product import Product


my_logger = logging.getLogger('admin_logger')
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


def admin_menu():
    while True:
        print("========================================\n"
              "pleas login or create admin account\n"
              "========================================\n"
              "1. create account\n"
              "2. login\n"
              "3. back\n")

        choice = input("Enter choice: ")

        try:
            choice = int(choice)
        except ValueError:
            print("That's not an int!")
            continue

        if choice == 1:
            while True:
                admin_identify = input('\nplease enter admin identity code :')
                if admin_identify == Admin.admins_identification:
                    user_info = input("========================================\n"
                                      "please enter these information\n"
                                      "========================================\n"
                                      "your full name | an username | a password :").split('|')

                    user_exist = User.check_username(user_info[1], 'Admin_info.csv')

                    if user_exist:

                        admin = Admin(user_info[1], user_info[0], user_info[2])
                        Admin.create_account(admin, 'Admin_info.csv')
                        break
                    else:
                        print('there is an admin!')
                        break
                else:
                    print('admin identification code is wrong!\n')
                    break
        elif choice == 2:
            username = input('username:')
            user_exist = User.check_username(username, 'Admin_info.csv')
            if not user_exist:
                while True:
                    password = input('password:')
                    pass_correct = User.login('Admin_info.csv', username, password)
                    if pass_correct:
                        my_logger.info('admin login done', exc_info=True)
                        print(f'welcome dear {username}.\n')
                        needed_products = Product.check_inventory()
                        if len(needed_products):
                            print('========================================\n'
                                  'these products are finished.\n'
                                  '========================================')
                            print(needed_products)
                        logout = False
                        while True:
                            print('\n========================================\n'
                                  'please select a part.\n'
                                  '========================================\n'
                                  '1. add product\n'
                                  '2. see invoices\n'
                                  '3.chang password\n'
                                  '4. logout\n')
                            part = input('enter a choice:')
                            try:
                                part = int(part)
                            except ValueError:
                                print("That's not an int!")
                                continue

                            if part == 1:
                                while True:
                                    product_info = input('barcode | name | brand | price | stock :').split('|')
                                    insertion = Admin.add_product(product_info)
                                    if insertion:
                                        my_logger.info('new product added', exc_info=True)
                                        if int(input('1 - new product | 2 - finish :')) == 2:
                                            break
                            elif part == 2:
                                Admin.view_invoices()

                            elif part == 3:
                                old_pass = hashlib.md5(input('enter password:').encode()).hexdigest()
                                new_pass = hashlib.md5(input('enter new password:').encode()).hexdigest()
                                User.chang_pass('Admin_info.csv', username, old_pass, new_pass)
                                my_logger.info('admin change password', exc_info=True)

                            elif part == 4:
                                logout = True
                                break
                            else:
                                print('Invalid input.\n')
                        if logout:
                            break
                    else:
                        print('password is wrong. please try again.')
            else:
                print('this username does not exist. please create an account.')
        elif choice == 3:
            break
        else:
            print('Invalid input.\n')



