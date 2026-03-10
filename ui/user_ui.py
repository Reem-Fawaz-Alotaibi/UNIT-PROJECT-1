from utils.storage_handler import *
from datetime import datetime
from colorama import *
from rich.console import Console
from rich.table import Table

console = Console()

class UserUI:
   
    def report_missing_person(self, user_id, phone):
            """
            Allows a user to submit a new missing person report
            """

            print(Fore.BLUE + Back.WHITE + "--- Register Missing Person Report ---" + Style.RESET_ALL)

            try:
                while True:
                    try:
                        age = input("Enter age (1-120): ").strip()
                        if not age.isdigit() or not (0 < int(age) < 120):
                            raise ValueError("Age must be a number between 1 and 120")
                        break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

                while True:
                    try:
                        gender = input("Enter gender (Male/Female): ").strip().capitalize()
                        if gender not in ["Male", "Female"]:
                            raise ValueError("Gender must be 'Male' or 'Female'")
                        break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

                while True:
                    try:
                        height = input("Enter height in cm (30-250): ").strip()
                        if not height.isdigit() or not (30 < int(height) < 250):
                            raise ValueError("Height must be between 30 and 250 cm")
                        break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

                while True:
                    try:
                        hair = input("Enter hair color: ").strip()
                        if not hair or any(char.isdigit() for char in hair):
                            raise ValueError("Invalid hair color")
                        break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

                while True:
                    try:
                        eye = input("Enter eye color: ").strip()
                        if not eye or any(char.isdigit() for char in eye):
                            raise ValueError("Invalid eye color")
                        break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

                while True:
                    try:
                        date = input("Last seen date (YYYY-MM-DD): ").strip()
                        datetime.strptime(date, '%Y-%m-%d')
                        break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

                marks = input("Distinctive marks (e.g, scar, birthmarks , surgical marks , mole): ").strip().lower() or "none"

                while True:
                    try:
                        last_seen = input("Last seen location:").strip().lower()
                        if not last_seen:
                            raise("[ERROR] Location cannot be empty")
                        elif any(char.isdigit() for char in last_seen):
                            raise("[ERROR] Location cannot contain numbers")
                        else:
                            break
                    except ValueError as e:
                        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")


                current_reports = load_from_json("missing_reports")
                if current_reports is None:
                    current_reports = []

                report_id = f"R-{100 + len(current_reports) + 1}"

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
                
                current_reports.append(new_report)
                
                save_to_json(current_reports, "missing_reports")
                print(Fore.GREEN  +"SUCCESS: Your report has been submitted successfully" + Style.RESET_ALL)
                print(Fore.GREEN  +f"REPORT ID: {report_id}"+ Style.RESET_ALL)

            except Exception as e:
               print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

    def view_my_reports(self, user_id, phone):
            """
            Filters and displays reports specifically submitted by the current user
            """
            reports = load_from_json("missing_reports") or []

            my_reports = [r for r in reports if str(r.get("user_id")) == str(user_id)]

            if not my_reports:
                console.print("\n[INFO] No reports found for your account", style="yellow")
                return
            
            table = Table(title="My Missing Person Reports", border_style="blue")
            table.add_column("Report ID", justify="center", style="blue")
            table.add_column("Age", justify="center")
            table.add_column("Gender", justify="center")
            table.add_column("Height", justify="center")
            table.add_column("Hair", justify="center")
            table.add_column("Eye", justify="center")
            table.add_column("Last Seen", justify="center")
            table.add_column("Status", justify="center", style="bold green")

            for r in my_reports:
                table.add_row(
                    str(r.get("report_id", "N/A")),
                    str(r.get("age", "N/A")),
                    str(r.get("gender", "N/A")),
                    str(r.get("height", "N/A")),
                    str(r.get("hair", "N/A")),
                    str(r.get("eye", "N/A")),
                    str(r.get("last_seen", "N/A")),
                    str(r.get("status", "N/A"))
                )

            console.print(table)
            print(Fore.BLUE + f"\n---- My Reports ({len(my_reports)}) ----" + Style.RESET_ALL)


    def user_portal(self):
        """
         Displays the user menu and handles navigation 
        """ 
        print(Fore.BLUE + Back.WHITE + "---- User Account ----" + Style.RESET_ALL)

        while True:
            try:
                user_id = input("Enter your ID (10 digits): ").strip()
                if len(user_id) != 10:
                    raise ValueError("ID must be exactly 10 digits!")
                if not user_id.isdigit():  
                    raise ValueError("ID must contain numbers only!")
                break 
            except ValueError as e:
                print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
                continue
            break

      
        while True:
            try:
                phone = input("Enter your phone number (starts with 05, 10 digits): ").strip()
                if not phone.isdigit():  
                    raise ValueError("ID must contain numbers only!")            
                if len(phone) != 10:
                    raise ValueError("Phone must be exactly 10 digits!")
                if not phone.startswith("05"):
                    raise ValueError("Phone must start with 05!")
                break
            except ValueError as e:
                print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
                

        print(Fore.GREEN + Style.BRIGHT + "[SUCCESS] Log in successfully")

        while True:
            print(Fore.BLUE + Back.WHITE + "  ▌ User Menu ▐  " + Style.RESET_ALL)
            print(Fore.BLUE + "1- Submit Report " + Style.RESET_ALL)
            print(Fore.BLUE + "2- View My Reports " + Style.RESET_ALL)
            print(Fore.BLUE + "3- Exit " + Style.RESET_ALL)


            choice = input("Choose: ")

            if choice == '1':
                self.report_missing_person(user_id, phone)
            elif choice == '2':
                self.view_my_reports(user_id, phone)
            elif choice == '3':
                break
            else:
                print("[ERROR] Invalid choice")