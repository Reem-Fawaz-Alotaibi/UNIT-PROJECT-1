import sys
from ui.hospital_ui import HospitalUI
from ui.user_ui import UserUI

def main_menu():
    """
    Main entry point to initialize UI and manage system navigation
    """
    hospital_ui = HospitalUI()
    user_ui = UserUI()

    while True:
        print("\n====  Welcome To Reunite System  ====")
        print("1- Hospital Portal (Staff Only)")
        print("2- User Portal (Public)")
        print("3- Exit")
        
        choice = input("\nChoose an option: ")
        if choice == '1':
           hospital_ui.access_hospital_portal()
        elif choice == '2':
           user_ui.user_portal()
        elif choice == '3':
           print("Exiting... Stay safe!")
           sys.exit()
        else:
            print(" Invalid choice please try again ")

if __name__ == "__main__":
    main_menu()