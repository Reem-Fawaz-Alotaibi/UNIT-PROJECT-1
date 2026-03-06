class UserUI:
    def menu(self):
        while True:
            print("\n=== Reunion System: User Menu ===")
            print("1- Report Missing Person")
            print("2- Check Report Status (By ID)")
            print("3- View Your Reports")
            print("4- Search by Distinctive Mark")
            print("5- Back to Main Menu")

            choice = input("\nChoose: ")

            if choice == '1':
                pass
            elif choice == '2':
                pass
            elif choice == '3':
                pass
            elif choice == '4':
                pass
            elif choice == '5':
                break

    def report_missing(self):
        print("\n--- Missing Person Report ---")
        
        print("\nSearching for matches...")
        print("ALERT! Possible match found! (Example Result)")