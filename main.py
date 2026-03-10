import sys
from ui.hospital_ui import HospitalUI
from ui.user_ui import UserUI
from colorama import Fore, Back, Style, init
init(autoreset=True)

def main_menu():
    """
    Main entry point to initialize UI and manage system navigation
    """
    hospital_ui = HospitalUI()
    user_ui = UserUI()

    while True:

        print(Fore.BLUE + Back.WHITE + " ▌   Welcome To Reunite System    ▐ " + Style.RESET_ALL)
        print(Fore.BLUE +"1- Hospital Portal (Staff Only) " + Style.RESET_ALL)
        print(Fore.BLUE +"2- User Portal (Public)" + Style.RESET_ALL)
        print(Fore.BLUE +"3- Exit " + Style.RESET_ALL)


        choice = input("Choose an option: ")
        if choice == '1':
           hospital_ui.access_hospital_portal()
        elif choice == '2':
           user_ui.user_portal()
        elif choice == '3':
           print("Exiting... Stay safe!")
           sys.exit()
        else:
            print(" \nInvalid choice please try again ")

if __name__ == "__main__":
   try:
        main_menu()
   except KeyboardInterrupt:
        print("\n\nSystem stopped by user.")