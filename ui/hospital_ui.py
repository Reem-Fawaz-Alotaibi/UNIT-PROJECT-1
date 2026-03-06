from core.models import UnknownPerson
from utils.storage_handler import save_to_json, load_from_json
from datetime import datetime

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

        marks = input("Distinctive marks (e.g., scar, tattoo): ").strip()
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

    def menu(self):
        while True:
            print("\n=== Hospital Management Menu ===")
            print("1- Register Unknown Patient")
            print("2- View All Unknown Patients")
            print("3- Edit Patient Data")
            print("4. Close Case (Move to Archive)")
            print("5. View Archive")
            print("6- Back to Main Menu")

            choice = input("\nChoose: ")
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.view_all_patients()
            elif choice == '3':
                pass
            elif choice == '4':
                pass
            elif choice == '5':
                pass
            elif choice == '6':
                break   