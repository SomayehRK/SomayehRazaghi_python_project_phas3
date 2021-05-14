from  User import User
import csv
from Admin_menu import admin_menu
from Customer_menu import customer_menu
from Product import Product


while True:
    print("========== * Somayeh Store * ==========\n"
          "1. Display available products\n"
          "2. Admin menu\n"
          "3. shopping\n"
          "4. Exit\n")
    choice = input("Enter choice: ")

    try:
        choice = int(choice)
    except ValueError:
        print("That's not an int!")
        continue

    if choice == 1:
        print('\n========================================\n'
              'list of our products\n'
              '========================================\n')
        Product.display()
        print('========================================\n')

    elif choice == 2:
        admin_menu()

    elif choice == 3:
        customer_menu()

    elif choice == 4:
        break

    else:
        print('Invalid input.\n')








