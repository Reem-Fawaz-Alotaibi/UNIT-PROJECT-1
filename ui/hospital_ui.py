from core.models import UnknownPerson
from utils.storage_handler import save_to_json, load_from_json ,overwrite_patients_file
from datetime import datetime
import re
#-------------------

class HospitalUI:
    #
    def access_hospital_portal(self):
        """
        Verifies hospital access code then opens hospital portal
        """
        print("\n---- Hospital Authentication ----")
        password = input("Enter Hospital Access Code: ")
        if password == "1234":
            self.hospital_portal()
        else:
            print("Access Denied!")
    #
    def register_patient(self):
        """
        Registers a new patient with auto-ID and validated physical traits
        Saves the data to a JSON database with a default 'Not identified' status
        """
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
                date = input("Entry date (YYYY-MM-DD): ").strip()
                datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("[ERROR] Invalid date format please use YYYY-MM-DD")


        marks = input("Distinctive marks (e.g, scar, birthmarks , surgical marks , mole): ").strip()
        if not marks:
            marks = "None"

        while True:
            try:
                location = input("Found location: ").strip()
                if not location:
                    raise ValueError("Location cannot be empty")
                break
            except ValueError as e:
                print(f"[ERROR] {e}")

        status = "Not identified"
        new_person = UnknownPerson(
            p_id,
            age,
            gender,
            hair,
            eye,
            height,
            marks,
            date,
            location,
            status
        )

        save_to_json(new_person.to_dict(), "patients")

        print("\n" + "*"*40)
        print(f"[SUCCESS] Patient registered successfully!")
        print(f"Assigning Patient ID: {p_id}")
        print(f"Status: {status}")
        print("*"*40)
    #
    def view_all_patients(self):
        """
        Displays a formatted table of all unknown patient records
        """
        patients = load_from_json("patients")
        if not patients:
            print("\n[INFO] No records found")
            return

        print("\n" + "="*135)
        print(f"{'ID':<7} | {'Age':<5} | {'Gender':<8} | {'Hair':<10} | {'Eyes':<8} | {'Height':<6} | {'Marks':<12} | {'Date':<15} | {'Location':<15} | {'status':<15}")
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
                  f"{p.get('location','N/A'):<15} | " 
                  f"{p.get('status','N/A')}")
        
        print("="*135)
        print(f"Total unknown cases : {len(patients)}")
        print("="*135)
    #
    def edit_patient_information(self):
        """ 
        Modifies an existing patient record and display updated record
        """
        print("\n" + "="*50)
        print("--- Edit Patient Information ---")
        print("="*50)

        try:
            p_id = input("Enter Patient ID (e.g , P-101): ").strip().upper()
            patients = load_from_json("patients")
            patient = next((p for p in patients if p['patient_id'] == p_id), None)
            
            if not patient:
                print(f"[ERROR] ID {p_id} not found")
                return

            print("\n---- Current Data -----")
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
                    print("[ERROR] Invalid choice please pick 0-8")
                    continue

                target_key = keys[choice]

                while True:
                    new_val = input(f"Enter new value for {target_key}: ").strip()
                    if not new_val:
                        print("[ERROR] Input cannot be empty")
                        continue

                    if target_key == "age":
                        if not new_val.isdigit() or not (0 < int(new_val) <= 120):
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
                    print(f"[SUCCESS] {target_key} updated successfully")
                    break

                while True:
                    ask = input("\nDo you want to edit another field? (y/n): ").strip().lower()
                    if ask == 'y':
                        break
                    elif ask == 'n':
                        editing = False
                        break
                    else:
                        print("[ERROR] Please type 'y' or 'n' only")

            overwrite_patients_file(patients, "patients")

            print("\n" + "*"*45)
            print(" [DONE] FINAL UPDATED DATA ")
            print("*"*45)
            print(f"{'FIELD':<20} | {'VALUE'}")
            print("-" * 40)
            display_map = [
                ("Patient ID", "patient_id"), 
                ("Age", "age"), 
                ("Gender", "gender"),
                ("Height", "height"), 
                ("Hair Color", "hair"), 
                ("Eye Color", "eye"),
                ("Location", "location"),
                ("Marks", "marks"), 
                ("Date", "date")
            ]
            
            for key, value in display_map:
                print(f"{key:<20} | {patient.get(value)}")
            print("-" * 40)

        except Exception as e:
            print(f"\n[CRITICAL ERROR] {e}")
    #
    def view_all_reports(self):
        """
        Displays all submitted missing person reports 
        """
        print("\n" + "="*145)
        print(f"{'--- user submitted missing person reports ---':^145}")
        print("="*145)

        reports = load_from_json("missing_reports")

        if not reports:
            print(f"{'[INFO] No reports have been submitted by users yet':^145}")
            return

        header = (f"{'Rep. ID':<8} | {'Age':<5} | {'Gender':<8} | {'Hair':<10} | "
                  f"{'Eyes':<8} | {'Height':<6} | {'Date Sub.':<12} | {'Status':<10} | "
                  f"{'Last Seen Location'}")
        
        print(header)
        print("-" * 145)

        for r in reports:
            print(f"{r.get('report_id', 'N/A'):<8} | "
                  f"{r.get('age', 'N/A'):<5} | "
                  f"{r.get('gender', 'N/A'):<8} | "
                  f"{r.get('hair', 'N/A'):<10} | "
                  f"{r.get('eye', 'N/A'):<8} | "
                  f"{r.get('height', 'N/A'):<6} | "
                  f"{r.get('date_submitted', 'N/A'):<12} | "
                  f"{r.get('status', 'Pending'):<10} | "
                  f"{r.get('last_seen', 'N/A')}")
        
        print("-" * 145)

    #
    def view_specific_report(self):
        """
        display a single patient's full details by ID.
        """
        print("\n" + "-"*40)
        report_id_to_find = input("Enter report ID to search (e.g., R-101): ").strip().upper()
        
        reports = load_from_json("missing_reports")
        
        found_report = None
        for r in reports:
            if r.get('report_id') == report_id_to_find:
                found_report = r
                break
        
        if found_report:
            print("\n" + "="*50)
            print(f"--- DETAILS FOR REPORT: {report_id_to_find} ---")
            print("="*50)
            print(f"Age:            {found_report.get('age')}")
            print(f"Gender:         {found_report.get('gender')}")
            print(f"Hair Color:     {found_report.get('hair')}")
            print(f"Eye Color:      {found_report.get('eye')}")
            print(f"Height:         {found_report.get('height')} cm")
            print(f"Last Seen:      {found_report.get('last_seen')}")
            print(f"Marks:          {found_report.get('marks')}")
            print(f"Date Submitted: {found_report.get('date_submitted')}")
            print(f"Current Status: {found_report.get('status')}")
            print("="*50)
        else:
            print(f"\n[ERROR] Report ID '{report_id_to_find}' not found")
    #
    def check_matching_report(self):
        """
        Matches a specific patient against the missing persons database 
        based on physical attributes and calculates a similarity score
        """
        try:
            patient_id = input("Enter patient ID: ").strip().upper()

            patients = load_from_json("patients")
            patient = None

            for p in patients:
                if p["patient_id"] == patient_id:
                    patient = p
                    break

            if not patient:
                print("Patient not found")
                return

            print("\nPatient Data:")
            print("Age:", patient["age"])
            print("Gender:", patient["gender"])
            print("Height:", patient["height"])
            print("Hair:", patient["hair"])
            print("Eye:", patient["eye"])
            print("Marks:", patient["marks"])

            reports = load_from_json("missing_reports")
            fields = ["age","gender","height","hair","eye","marks"]
            found = False

            for r in reports:
               
                matched = 0
                if patient["age"] == r["age"]:
                    matched += 1
                if patient["gender"].lower() == r["gender"].lower():
                    matched += 1
                if patient["height"] == r["height"]:
                    matched += 1
                if patient["hair"] == r["hair"]:
                    matched += 1
                if patient["eye"] == r["eye"]:
                    matched += 1
                if patient["marks"] == r["marks"]:
                    matched += 1

                match_percentage = (matched / len(fields)) * 100

                if match_percentage >= 50:

                    found = True
                    print("\nPossible match found!")
                    print("------------------------")
                    print("Report ID:", r["report_id"])
                    print("Reported By ID:", r["user_id"])
                    print("Phone number:", r["phone"])
                    print("Match:", f"{match_percentage:.0f}%")

                    if match_percentage >= 70:
                        print("HIGH PROBABILITY MATCH")
                    else:
                        print("POSSIBLE MATCH")

                    r["status"] = "Possible match"
                    r["patient_id"] = patient["patient_id"]

            if found:
                overwrite_patients_file(reports,"missing_reports")
                print("\nThe hospital will contact the family")
            else:
                print("\nNo matching reports found")

        except Exception as e:
            print("[ERROR]", e)

    def close_case(self):
        """
        Finalizes a missing person case by moving the report to the archive
        and updating the linked patient status to 'Identified'
        """
        try:
            report_id = input("Enter Report ID to close case: ").strip().upper()

            reports = load_from_json("missing_reports")
            archive = load_from_json("archive")

            found = False

            for r in reports:
                if r["report_id"] == report_id:

                    print(f"\nReport ID: {r['report_id']}")
                    print(f"Status: {r['status']}")

                    if r["status"].lower() != "possible match":
                        print("This case cannot be closed yet")
                        print("Status must be 'Possible Match' first")
                        found = True
                        break

                    confirm = input("Are you sure you want to close this case? (y/n): ").lower()

                    if confirm == "y":

                        r["status"] = "Closed"

                        try:
                            patients = load_from_json("patients")

                            for p in patients:
                                if p["patient_id"] == r["patient_id"]:
                                    p["status"] = "Identified"
                                    break

                            overwrite_patients_file(patients, "patients")

                        except Exception as patient_error:
                            print("[WARNING] Patient status could not be updated:", patient_error)
               

                        archive.append(r)
                        reports.remove(r)

                        overwrite_patients_file(reports, "missing_reports")
                        overwrite_patients_file(archive, "archive")

                        print("\nCase closed and moved to archive")
                        print("The family has been notified")

                    else:
                        print("\nOperation cancelled")

                    found = True
                    break

            if not found:
                print("Report not found")

        except Exception as e:
            print("Error while closing case:", e)

    def hospital_portal(self):
     """
     Displays the hospital menu and handles navigation 
     """
     while True:
            print("\n---- Hospital Portal ----")
            print("1- Register Unknown Patient")
            print("2- View All Unknown Patients")
            print("3- Edit Patient Information")
            print("4- View All Reports")
            print("5- Search Specific Report")
            print("6- Check for Matches")   
            print("7- Close Patient Case")
            print("8- Back to Main Menu")

            choice = input("\nChoose: ")
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.view_all_patients()
            elif choice == '3':
                self.edit_patient_information()
            elif choice == '4':
                self.view_all_reports() 
            elif choice == '5':
                self.view_specific_report() 
            elif choice == '6':
                self.check_matching_report()
            elif choice == '7':
                self.close_case()
            elif choice == '8':
                break 


          
