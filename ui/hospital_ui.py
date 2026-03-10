from core.models import UnknownPerson
from utils.storage_handler import save_to_json, load_from_json ,overwrite_patients_file
from datetime import datetime
from rich.console import Console
from rich.table import Table
from colorama import *

init(autoreset=True)
console = Console()

class HospitalUI:
      
    def access_hospital_portal(self):
        print(Fore.BLUE + Back.WHITE + " ***** Hospital Authentication ***** " + Style.RESET_ALL)
        password = input("Enter Hospital Access Code: ")
        if password == "1234":
            print(Fore.GREEN + Style.BRIGHT + "[SUCCESS] Logged in successfully")
            self.hospital_portal()
        else:
            console.print("\n[ACCESS DENIED] Wrong code!", style="bold red")

    def register_patient(self):
            """
            Registers a new patient with auto-ID and validated physical traits
            Saves the data to a JSON database with a default 'Not identified' status
            """

            header = " -- Registering New Unknown Patient -- "
            print(Back.WHITE + Fore.BLUE + header + Style.RESET_ALL) 

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
                    location = input("Found location: ").strip().upper()
                    if not location:
                        raise ValueError("Location cannot be empty")
                    elif any(char.isdigit() for char in location):
                        print("[ERROR] Location cannot contain numbers")
                    else:
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

            print(Fore.GREEN + Back.WHITE + "    [SUCCESS]   " + Style.RESET_ALL)
            print(f"Patient registered successfully!")
            print(f"Assigning Patient ID: {p_id}")
            print(f"Status: {status}")
    

    def view_all_patients(self):
        """
        Displays a formatted table of all unknown patient records
        """
        patients = load_from_json("patients")
        if not patients:
            console.print("\n[INFO] No records found", style="yellow")
            return
        
        table = Table(title="Unknown Patients", title_style="bold white",border_style="blue")
        table.add_column("ID", justify="center", width=13)
        table.add_column("Age", justify="center", width=13)
        table.add_column("Gender", justify="center", width=15)
        table.add_column("Hair", justify="center", width=15)
        table.add_column("Eyes", justify="center", width=10)
        table.add_column("Height", justify="center", width=15)
        table.add_column("Marks", justify="center", width=13)
        table.add_column("Date", justify="center", width=12)
        table.add_column("Location", justify="center", width=15)
        table.add_column("Status", justify="center", width=15)
        
        for p in patients:
            table.add_row(
                p.get('patient_id','N/A'),
                str(p.get('age','N/A')),
                p.get('gender','N/A'),
                p.get('hair','N/A'),
                p.get('eye','N/A'),
                str(p.get('height','N/A')),
                p.get('marks','N/A'),
                p.get('date','N/A'),
                p.get('location','N/A'),
                p.get('status','N/A')
            )

        
        console.print(table)
        console.print(f"Total unknown cases: {len(patients)}", style="bold blue", highlight=False)
    
    def edit_patient_information(self):
        """ 
        Modifies an existing patient record and display updated record
        """

        print(Fore.BLUE + Back.WHITE + " -- Edit Patient Information -- " + Style.RESET_ALL)

        try:
            p_id = input("Enter Patient ID (e.g , P-101): ").strip().upper()
            patients = load_from_json("patients")
            patient = next((p for p in patients if p['patient_id'] == p_id), None)
            
            if not patient:
                console.print(f"[ERROR] ID {p_id} not found", style="bold red")
                return

            table_current = Table(title="Current Data", border_style="bold blue")

            table_current.add_column("ID", justify="center")
            table_current.add_column("1-Age", justify="center")
            table_current.add_column("2-Gender", justify="center")
            table_current.add_column("3-Hair", justify="center")
            table_current.add_column("4-Eyes", justify="center")
            table_current.add_column("5-Height", justify="center")
            table_current.add_column("6-Marks", justify="center")
            table_current.add_column("7-Entry date", justify="center")
            table_current.add_column("8-Location", justify="center")
            table_current.add_column("Status", justify="center")

            table_current.add_row(
                str(patient.get("patient_id")),
                str(patient.get("age")),
                str(patient.get("gender")),
                str(patient.get("hair")),
                str(patient.get("eye")),
                str(patient.get("height")),
                str(patient.get("marks")),
                str(patient.get("date")),
                str(patient.get("location")),
                str(patient.get("status", "Unknown"))
            )

            console.print(table_current)

            keys = {"1":"age", "2":"gender", "3":"hair", "4":"eyes", "5":"height", 
                    "6":"marks", "7":"date", "8":"location"}
            editing = True

            while editing:
                choice = input("\nSelect number to edit (1-8): ").strip()
                if choice == "0":
                    break
                if choice not in keys:
                    console.print("[ERROR] Invalid choice please pick 1-8", style="bold red")
                    continue

                target_key = keys[choice]

                while True:
                    new_val = input(f"Enter new value for {target_key}: ").strip()
                    current_val = str(patient.get(target_key)).lower()
                    if new_val.lower() == current_val:
                        console.print("[WARNING] The value is the same as the current one. No change made.", style="bold red")
                        continue

                    if target_key == "age":
                        if not new_val.isdigit() or not (0 < int(new_val) <= 120):
                            console.print("[ERROR] Age must be a number between 1 and 120!", style="bold red")
                            continue

                    elif target_key == "gender":
                        if new_val.capitalize() not in ["male", "female"]:
                            console.print("[ERROR] Gender must be 'male' or 'female' only!", style="bold red")
                            continue

                    elif target_key == "height":
                        if not new_val.isdigit() or not (100 <= int(new_val) <= 250):
                            console.print("[ERROR] Height must be a number between 100 and 250!", style="bold red")
                            continue

                    elif target_key in ["hair", "eye", "location", "marks"]:
                        if any(char.isdigit() for char in new_val):
                            console.print(f"[ERROR] {target_key.capitalize()} should not contain numbers!", style="bold red")
                            continue

                    elif target_key == "date":
                        try:
                            datetime.strptime(new_val, "%Y-%m-%d")
                        except ValueError:
                            console.print("[ERROR] Entry date must be in YYYY-MM-DD format!", style="bold red")
                            continue

                    patient[target_key] = new_val
                    console.print(f" [SUCCESS] {target_key} updated successfully", style="bold green")
                    break

                while True:
                    ask = input("\nDo you want to edit another field? (y/n): ").strip().lower()
                    if ask == 'y':
                        break
                    elif ask == 'n':
                        editing = False
                        break
                    else:
                        console.print("[ERROR] Please type 'y' or 'n' only", style="bold red")

            overwrite_patients_file(patients, "patients")

            table_final = Table(title="Updated Data ", border_style="bold blue")

            table_final.add_column("ID", justify="center")
            table_final.add_column("Age", justify="center")
            table_final.add_column("Gender", justify="center")
            table_final.add_column("Hair", justify="center")
            table_final.add_column("Eyes", justify="center")
            table_final.add_column("Height", justify="center")
            table_final.add_column("Marks", justify="center")
            table_final.add_column("Entry date", justify="center")
            table_final.add_column("Location", justify="center")
            table_final.add_column("Status", justify="center")

            table_final.add_row(
                str(patient.get("patient_id")),
                str(patient.get("age")),
                str(patient.get("gender")),
                str(patient.get("hair")),
                str(patient.get("eye")),
                str(patient.get("height")),
                str(patient.get("marks")),
                str(patient.get("date")),
                str(patient.get("location")),
                str(patient.get("status", "Unknown"))
            )

            console.print(table_final)

        except Exception as e:
            console.print(f"\n[ERROR] {e}", style="bold red")
    

    def view_all_reports(self):
        """
        Displays all submitted missing person reports 
        """
      

        reports = load_from_json("missing_reports")

        if not reports:
            console.print("[INFO] No reports have been submitted by users yet", style="yellow")
            return

        table = Table(title="Missing Reports", border_style="bold blue")

        table.add_column("Rep. ID", justify="center")
        table.add_column("Age", justify="center")
        table.add_column("Gender", justify="center")
        table.add_column("Hair", justify="center")
        table.add_column("Eyes", justify="center")
        table.add_column("Height", justify="center")
        table.add_column("Date Submitted", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Last Seen Location", justify="center")

        for r in reports:
            table.add_row(
                str(r.get("report_id", "N/A")),
                str(r.get("age", "N/A")),
                str(r.get("gender", "N/A")),
                str(r.get("hair", "N/A")),
                str(r.get("eye", "N/A")),
                str(r.get("height", "N/A")),
                str(r.get("date_submitted", "N/A")),
                str(r.get("status", "Pending")),
                str(r.get("last_seen", "N/A"))
            )

        console.print(table)
        console.print(f"Total Missing Reports: {len(reports)}", style="bold blue", highlight=False)


    def view_specific_report(self):
        """
        display a single patient's full details by ID.
        """
        console = Console()
        print(Fore.BLUE + Back.WHITE + " ---------------------------------- " + Style.RESET_ALL)
        report_id_to_find = input("Enter report ID to search (e.g , R-101): ").strip().upper()
        
        reports = load_from_json("missing_reports")
        
        found_report = None
        for r in reports:
            if r.get('report_id') == report_id_to_find:
                found_report = r
                break
        
        if found_report:
            table = Table(title=f"Report Details: {report_id_to_find}", show_lines=True, style="cyan")

            fields = ["ID Number", "Phone Number", "Age", "Gender", "Hair Color", 
                    "Eye Color", "Height (cm)", "Last Seen", "Marks", "Date Submitted", "Current Status"]

            for field in fields:
                table.add_column(field, style="bold white", justify="center")

            table.add_row(
                found_report.get('user_id', "N/A"),
                found_report.get('phone', "N/A"),
                str(found_report.get('age')),
                found_report.get('gender'),
                found_report.get('hair'),
                found_report.get('eye'),
                str(found_report.get('height')),
                found_report.get('last_seen'),
                found_report.get('marks'),
                found_report.get('date_submitted'),
                found_report.get('status')
            )

            console.print(table)
        else:
            console.print(f"[bold red]\n[ERROR][/bold red] Report ID '{report_id_to_find}' not found")   
        
    
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

            table = Table(title="Patient Data", show_lines=True, style="cyan")
    
            fields = ["Age", "Gender", "Height", "Hair", "Eye", "Marks"]
            for field in fields:
                table.add_column(field, style="bold white", justify="center")
            
            table.add_row(
                str(patient.get("age", "N/A")),
                patient.get("gender", "N/A"),
                str(patient.get("height", "N/A")),
                patient.get("hair", "N/A"),
                patient.get("eye", "N/A"),
                patient.get("marks", "N/A")
            )
            
            console.print(table)

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

            print(Fore.BLUE + Back.WHITE + "  ▌ Hospital Portal ▐  " + Style.RESET_ALL)
            print(Fore.BLUE + "1- Register Unknown Patient" + Style.RESET_ALL)
            print(Fore.BLUE + "2- View All Unknown Patients" + Style.RESET_ALL)
            print(Fore.BLUE + "3- Edit Patient Information" + Style.RESET_ALL)
            print(Fore.BLUE + "4- View All Reports" + Style.RESET_ALL)
            print(Fore.BLUE + "5- Search Specific Report" + Style.RESET_ALL)
            print(Fore.BLUE + "6- Check for Matches" + Style.RESET_ALL)   
            print(Fore.BLUE + "7- Close Patient Case" + Style.RESET_ALL)
            print(Fore.BLUE + "8- Back to Main Menu" + Style.RESET_ALL)

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


          
