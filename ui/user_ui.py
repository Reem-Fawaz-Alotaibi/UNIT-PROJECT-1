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
                self.report_missing()
            elif choice == '2':
                self.check_status()
            elif choice == '3':
                self.view_all_reports()
            elif choice == '4':
                self.search_by_mark()
            elif choice == '5':
                break

    def report_missing(self):
        print("\n--- Missing Person Report ---")
        
        print("\nSearching for matches...")
        print("ALERT! Possible match found! (Example Result)")