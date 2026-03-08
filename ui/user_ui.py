from utils.storage_handler import *
from datetime import datetime

class UserUI:
   
   def report_missing_person(self,user_id, phone):
        """
        Allows a user to submit a new missing person report
        """
        print("\n" + "="*60)
        print("--- Register Missing Person Report ---")
        print("="*60)

        try:
            while True:
                try:
                    age = input("Enter age (1-120): ").strip()
                    if not age.isdigit() or not (0 < int(age) < 120):
                        raise ValueError("Age must be a number between 1 and 120")
                    break
                except ValueError as e:
                    print(f"[ERROR] {e}")

            while True:
                try:
                    gender = input("Enter gender (Male/Female): ").strip().capitalize()
                    if gender not in ["Male", "Female"]:
                        raise ValueError("Gender must be 'Male' or 'Female'")
                    break
                except ValueError as e:
                    print(f"[ERROR] {e}")

            while True:
                try:
                    height = input("Enter height in cm (30-250): ").strip()
                    if not height.isdigit() or not (30 < int(height) < 250):
                        raise ValueError("Height must be between 30 and 250 cm")
                    break
                except ValueError as e:
                    print(f"[ERROR] {e}")

            while True:
                try:
                    hair = input("Enter hair color: ").strip()
                    if not hair:
                        raise ValueError("Hair color cannot be empty")
                    if any(char.isdigit() for char in hair):
                        raise ValueError("Hair color cannot contain numbers")
                    break
                except ValueError as e:
                    print(f"[ERROR] {e}")

            while True:
                try:
                   eye = input("Enter eye color: ").strip()
                   if not eye:
                       raise ValueError("Eye color cannot be empty")
                   if any(char.isdigit() for char in eye):
                       raise ValueError("Eye color cannot contain numbers")
                   break
                except ValueError as e:
                    print(f"[ERROR] {e}")

            while True:
                try:
                    date = input("Last seen date (YYYY-MM-DD): ").strip()
                    datetime.strptime(date, '%Y-%m-%d')
                    break
                except ValueError:
                    print("[ERROR] Invalid date format. Please use YYYY-MM-DD")

            marks = input("Distinctive marks (e.g.,scar, birthmarks , surgical marks , mole): ").strip().lower()
            if not marks: 
                marks = "none"

            while True:
                last_seen = input("Last seen location : ").strip().lower()
                if last_seen:
                    break
                print("[ERROR] Location cannot be empty")

            reports = load_from_json("missing_reports")
            report_id = f"R-{100 + len(reports) + 1}"

            new_report = {
                "report_id": report_id,
                "user_id": user_id,         
                "phone": phone,            
                "age": age,
                "gender": gender,
                "height": height,
                "hair": hair,
                "eye": eye,
                "last_seen": last_seen,
                "marks": marks,
                "status": "Not identified",
                "date_submitted": date
            }
            
            reports = load_from_json("missing_reports")
            reports.append(new_report)
            save_to_json(reports, "missing_reports")
            
            print("\n" + "*"*50)
            print(" SUCCESS: Your report has been submitted successfully")
            print(f" REPORT ID: {report_id}")
            print(" Our team will review the report")
            print(" The hospital will contact you if the person is identified")
            print("*"*50)

        except Exception as e:
            print(f"\n[SYSTEM ERROR] {e}")

   
   def view_my_reports(self, user_id, phone):
    """
    Filters and displays reports specifically submitted by the current user
    """
    reports = load_from_json("missing_reports")

    my_reports = [r for r in reports if r.get("user_id") == user_id and r.get("phone") == phone]

    if not my_reports:
        print("No reports found for your ID and phone")
        return

    for r in my_reports:
        print("\nReport ID:", r["report_id"])
        print("Age:", r["age"])
        print("Gender:", r["gender"])
        print("Height:", r["height"])
        print("Hair:", r["hair"])
        print("Eye:", r["eye"])
        print("Last Seen:", r["last_seen"])
        print("Status:", r["status"])


   def user_portal(self):
        """
         Displays the user menu and handles navigation 
        """ 
        print("\n---- User Portal ----")

        while True:
            try:
                user_id = input("Enter your ID (10 digits): ").strip()
                if len(user_id) != 10:
                    raise ValueError("ID must be exactly 10 digits!")
                if not user_id.isdigit():  
                    raise ValueError("ID must contain numbers only!")
            except ValueError as e:
                print(f"[ERROR] {e}")
                continue
            break

      
        while True:
            try:
                phone = input("Enter your phone number (starts with 05, 10 digits): ").strip()
                if not user_id.isdigit():  
                    raise ValueError("ID must contain numbers only!")            
                if len(phone) != 10:
                    raise ValueError("Phone must be exactly 10 digits!")
                if not phone.startswith("05"):
                    raise ValueError("Phone must start with 05!")
                
            except ValueError as e:
                print(f"[ERROR] {e}")
                continue
            break

        print("\n[SUCCESS] Login successful")

        while True:
            print("\n--- User Menu ---")
            print("1. Submit Report")
            print("2. View My Reports")
            print("3. Exit")

            choice = input("Choose: ")

            if choice == '1':
                self.report_missing_person(user_id, phone)
            elif choice == '2':
                self.view_my_reports(user_id, phone)
            elif choice == '3':
                break
            else:
                print("[ERROR] Invalid choice")
