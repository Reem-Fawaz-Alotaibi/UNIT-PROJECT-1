class HospitalUI:
    def auth_menu(self):
        print("\n--- Hospital Authentication ---")
        password = input("Enter Hospital Access Code: ")
        if password == "1234":
            self.menu()
        else:
            print("Access Denied!")

    def menu(self):
        while True:
            print("\n=== Hospital Management Menu ===")
            print("1- Register Unknown Patient")
            print("2- View All Unknown Patients")
            print("3- Edit Patient Data")
            print("4- Identify/Remove Patient (Found)")
            print("5- Back to Main Menu")

            choice = input("\nChoose: ")
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.view_patients()
            elif choice == '3':
                self.edit_patient()
            elif choice == '4':
                self.remove_patient()
            elif choice == '5':
                break

    def register_patient(self):
        print("\n--- Registering New Unknown Patient ---")

        print(" Patient registered successfully!")