
import datetime
import json, os
from helperfunctions import getinput
from accountmanagement import signup, login

class Competition():
    def __init__(self, name):
        self.name = name

    def create_competition(self, useremail):
        """
        Function to create a new competition and initialize the basic information.
        """
        print("### CREATING A COMPETITION ###")
        comp_name = input("What is the name of your competition?: ")
        start_date = getinput("date", "Please enter the start date of your competition [YYYY/MM/DD]: ")
        end_date_check = getinput("y/n", "Are you hosting a one-day competition? [Y/N]: ")
        if end_date_check == "Y":
            end_date = start_date
        else:
            end_date = getinput("date", "Please enter the ending date of your competition [YYYY/MM/DD]: ")
        reg_close = getinput("date", "Please enter when you wish registration to close [YYYY/MM/DD]: ")
        comp_code = getinput("code", "Please provide a 4-letter long competition code [e.g. HBEG]: ")
        
        print(f"Here's the provided information about your competition:")
        print(f"Competition name: {comp_name}\nCompetition code: {comp_code}")
        print(f"Start date: {start_date}\nEnd date: {end_date}\nRegistration closes: {reg_close}")
        finalcheck = getinput("y/n", "Is all the information correct? [Y/N]: ")
        if finalcheck == "N":
            pass
        else:
            filename = comp_code + "_" + start_date[:4]
            newpath = f"{filename}"
            os.makedirs(newpath)
            comp_details = {
                "name": comp_name,
                "start date": start_date,
                "end date": end_date,
                "registration close": reg_close,
                "directory": newpath
            }

        with open("competitionsdata.json", "r+") as f:
            try:
                f_data = json.load(f)
            except json.JSONDecodeError:
                f_data = {}
            f_data[filename] = []
            f_data[filename].append(comp_details)
            f.seek(0)
            json.dump(f_data, f, indent=4)

        with open("userdata.json", "r") as f:
            f_data = json.load(f)
            f_data[useremail][0][1].append(filename)
        with open("userdata.json", "w") as f:
            json.dump(f_data, f, indent=4)

    def add_dances(self, useremail):
        mod_comp = input("Enter the competition code of the comp you wish to modify [ABCD_YYYY]: ")
        with open("userdata.json", "r") as f:
            f_data = json.load(f)
            if mod_comp.upper() in f_data[useremail][0][1]:
                access = True
            else:
                print("You do not have the permission to modify this competition.")
                return None

        self.dances = {}        
        levels = ['Newcomer', 'Bronze', 'Silver', 'Gold', 'Syllabus', 'Open']
        latin_dances = ['International_ChaCha', 'International_Rumba', 'Jive', 'Paso_Doble', 'Samba']
        rhytm_dances = ['American_ChaCha', 'American_Rumba', 'EastCoast_Swing', 'Bolero', 'Mambo']
        smooth_dances = ['American_Waltz', 'American_VWaltz', 'American_Foxtrot', 'American_Tango']
        standard_dances = ['International_Waltz', 'International_VWaltz', 'International_Tango', 'Quickstep']
        dance_categories = [latin_dances, rhytm_dances, smooth_dances, standard_dances]

        while access:
            print("## CHOOSE COMPETITON LEVEL TO ADD DANCES AT ##")
            print("# 1. NEWCOMER\n# 2. BRONZE\n# 3. SILVER\n# 4. GOLD\n# 5. SYLLABUS\n# 6. OPEN")
            input_level = getinput("xchoices", "Choose one of the competition levels [1-6]. If you are done, type [EXIT]: ", 6)
            if input_level == 404: return None
            level = levels[input_level-1]
            print("## CHOOSE CATEGORY ")
            print("# 1. LATIN\n# 2. RHYTM\n# 3. SMOOTH\n# 4. STANDARD")
            category = getinput("xchoices", "Choose one of the categories [1-4]. If you wish to return, type [EXIT]: ", 4)
            if category == 404: return None
            category = dance_categories[category-1]

            dancelist = []
            while True:
                print("## CHOOSE DANCES TO ADD ##")
                if category == latin_dances:
                    print("# 1. INT. CHA CHA\n# 2. INT. RUMBA\n# 3. JIVE\n# 4. PASO DOBLE\n# 5. SAMBA")
                if category == rhytm_dances:
                    print("# 1. AM. CHA CHA\n# 2. AM. RUMBA\n# 3. SWING\n# 4. BOLERO\n# 5. MAMBO")
                if category == smooth_dances:
                    print("# 1. AM. WALTZ\n# 2. AM. V. WALTZ\n# 3. AM. FOXTROT\n# 4. AM. TANGO")
                if category == standard_dances:
                    print("# 1. INT. WALTZ\n# 2. INT. V. WALTZ\n# 3. INT. TANGO\n# 4. QUICKSTEP")
                if category == 1 or 2:
                    adding_dances = getinput("xchoices", "Choose a dance to add [1-5]. If you wish to return, type [BACK]. If you wish to go back to the main menu, type [EXIT]: ", 5)
                else:
                    adding_dances = getinput("xchoices", "Choose a dance to add [1-4]. If you wish to return, type [BACK]. If you wish to go back to the main menu, type [EXIT]: ", 4)
                if adding_dances == 304: break
                elif adding_dances == 404: return None
                dancetype = category[adding_dances-1]
                dancefile_name = f"{level}__{dancetype}"
                f_data = {}
                with open(f"{mod_comp.upper()}/{dancefile_name}", "w+") as f:
                    json.dump(f_data, f, indent=4)
