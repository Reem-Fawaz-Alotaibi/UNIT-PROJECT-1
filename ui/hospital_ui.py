from core.models import UnknownPerson
from utils.storage_handler import save_to_json, load_from_json ,overwrite_patients_file
from datetime import datetime
import re


class HospitalUI:
    def auth_menu(self):
        print("\n--- Hospital Authentication ---")
        password = input("Enter Hospital Access Code: ")
        if password == "1234":
            self.menu()
        else:
            print("Access Denied!")
    
    def register_patient(self):
        print("\n" + "="*40)
        print("--- Registering New Unknown Patient ---")
        print("="*40)

        patients = load_from_json("patients")
        if patients:
            last_id_num = int(patients[-1]['patient_id'].split('-')[1])
            p_id = f"P-{last_id_num + 1}"
        else:
            p_id = "P-101"


        while True:
            try:
                age = input("Enter approximate age (1-120): ").strip()
                if not age.isdigit() or not (0 < int(age) < 120):
                    raise ValueError("Age must be a number between 1 and 120.")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        while True:
            try:
                gender = input("Enter gender (Male/Female): ").strip().capitalize()
                if gender not in ["Male", "Female"]:
                    raise ValueError("Gender must be 'Male' or 'Female'.")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        while True:
            try:
                height = input("Enter height in cm (30-250): ").strip()
                if not height.isdigit() or not (30 < int(height) < 250):
                    raise ValueError("Height must be between 30 and 250 cm.")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        while True:
            try:
                hair = input("Enter hair color: ").strip()
                if not hair:
                    raise ValueError("Hair color cannot be empty.")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        while True:
            try:
                eye = input("Enter eye color: ").strip()
                if not eye:
                    raise ValueError("Eye color cannot be empty.")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        while True:
            try:
                date = input("Entry date (YYYY-MM-DD): ").strip()
                datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("[ERROR] Invalid date format. Please use YYYY-MM-DD.")

        marks = input("Distinctive marks (e.g.,scar): ").strip()
        if not marks:
            marks = "None"

        while True:
            try:
                location = input("Found location: ").strip()
                if not location:
                    raise ValueError("Location cannot be empty.")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        new_person = UnknownPerson(
            p_id,
            age,
            gender,
            hair,
            eye,
            height,
            marks,
            date,
            location
        )

        save_to_json(new_person.to_dict(), "patients")

        print("\n" + "*"*40)
        print(f"[SUCCESS] Patient registered successfully!")
        print(f"Assigning Patient ID: {p_id}")
        print("*"*40)

    def view_all_patients(self):
        patients = load_from_json("patients")
        if not patients:
            print("\n[INFO] No records found.")
            return

        print("\n" + "="*135)
        print(f"{'ID':<7} | {'Age':<5} | {'Gender':<8} | {'Hair':<10} | {'Eyes':<8} | {'Height':<6} | {'Marks':<12} | {'Date':<15} | {'Location'} |")
        print("-" * 135)
        
        for p in patients:
            print(f"{p.get('patient_id','N/A'):<7} | "
                  f"{p.get('age','N/A'):<5} | "
                  f"{p.get('gender','N/A'):<8} | "
                  f"{p.get('hair','N/A'):<10} | "
                  f"{p.get('eye','N/A'):<8} | "
                  f"{p.get('height','N/A'):<6} | "
                  f"{p.get('marks','N/A'):<12} | "   
                  f"{p.get('date','N/A'):<15} | " 
                  f"{p.get('location','N/A')}")
        
        print("="*135)
        print(f"Total unknown Cases : {len(patients)}")
        print("="*135)

    def edit_patient_information(self):
        print("\n" + "="*50)
        print("--- Edit Patient Information ---")
        print("="*50)

        try:
            p_id = input("Enter Patient ID (e.g., P-101): ").strip().upper()
            patients = load_from_json("patients")
            patient = next((p for p in patients if p['patient_id'] == p_id), None)
            
            if not patient:
                print(f"[ERROR] ID {p_id} not found.")
                return

            print("\n--- Current Data ---")
            print(f"1. Age: {patient['age']}")
            print(f"2. Gender: {patient['gender']}")
            print(f"3. Height: {patient['height']}")
            print(f"4. Hair: {patient['hair']}")
            print(f"5. Eye: {patient['eye']}")
            print(f"6. Location: {patient['location']}")
            print(f"7. Marks: {patient['marks']}")
            print(f"8. Date: {patient['date']}")
            print("0. Save and Exit")

            keys = {"1":"age", "2":"gender", "3":"height", "4":"hair", "5":"eye", "6":"location", "7":"marks", "8":"date"}
            editing = True

            while editing:
                choice = input("\nSelect number to edit (0-8): ").strip()
                if choice == "0":
                    break
                if choice not in keys:
                    print("[ERROR] Invalid choice. Please pick 0-8.")
                    continue

                target_key = keys[choice]

                while True:
                    new_val = input(f"Enter new value for {target_key}: ").strip()
                    if not new_val:
                        print("[ERROR] Input cannot be empty.")
                        continue

                    if target_key == "age":
                        if not new_val.isdigit() or not (1 <= int(new_val) <= 120):
                            print("[ERROR] Age must be a number between 1 and 120!")
                            continue

                    elif target_key == "gender":
                        if new_val.lower() not in ["male", "female"]:
                            print("[ERROR] Gender must be 'male' or 'female' only!")
                            continue

                    elif target_key == "height":
                        if not new_val.isdigit() or not (100 <= int(new_val) <= 250):
                            print("[ERROR] Height must be a number between 100 and 250!")
                            continue

                    elif target_key in ["hair", "eye", "location", "marks"]:
                        if any(char.isdigit() for char in new_val):
                            print(f"[ERROR] {target_key.capitalize()} should not contain numbers!")
                            continue

                    elif target_key == "date":
                        try:
                            from datetime import datetime
                            datetime.strptime(new_val, "%Y-%m-%d")
                        except ValueError:
                            print("[ERROR] Date must be in YYYY-MM-DD format!")
                            continue

                    patient[target_key] = new_val
                    print(f"[SUCCESS] {target_key} updated successfully.")
                    break

                while True:
                    ask = input("\nDo you want to edit another field? (y/n): ").strip().lower()
                    if ask == 'y':
                        break
                    elif ask == 'n':
                        editing = False
                        break
                    else:
                        print("[ERROR] Please type 'y' or 'n' only.")

            overwrite_patients_file(patients, "patients")

            print("\n" + "*"*45)
            print(" [DONE] FINAL UPDATED DATA ")
            print("*"*45)
            print(f"{'FIELD':<20} | {'VALUE'}")
            print("-" * 40)
            display_map = [
                ("Patient ID", "patient_id"), ("Age", "age"), ("Gender", "gender"),
                ("Height", "height"), ("Hair Color", "hair"), ("Eye Color", "eye"),
                ("Location", "location"), ("Marks", "marks"), ("Date", "date")
            ]
            for label, key in display_map:
                print(f"{label:<20} | {patient.get(key)}")
            print("-" * 40)

        except Exception as e:
            print(f"\n[CRITICAL ERROR] {e}")

    def menu(self):
     while True:
            print("\n=== Hospital Management Menu ===")
            print("1- Register Unknown Patient")
            print("2- View All Unknown Patients")
            print("3- Edit Patient Information")
            print("6- Back to Main Menu")

            choice = input("\nChoose: ")
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.view_all_patients()
            elif choice == '3':
                self.edit_patient_information()
            elif choice == '4':
                pass 
            elif choice == '5':
                pass 
            elif choice == '6':
                break   


          
