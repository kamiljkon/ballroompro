import datetime
import json, os
from helperfunctions import getinput, findkey
from accountmanagement import User
from sqlalchemy import create_engine, Column, Integer, String, CHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from glob import glob
import re
import csv

# Initializing database
Base = declarative_base()
engine = create_engine("sqlite:///data.db", echo=False)
Session = sessionmaker(bind=engine)

def check_access(useremail):
        """
        Helper function to check if the user has access to modify or in other ways
        interfere with a competition.

        Args:
            useremail (str) -> email of the current user
        
        Returns:
            mod_comp (str) -> competition code
        """

        mod_comp = input("Enter the competition code of the comp you wish to setup [ABCD_YYYY]: ")
        session = Session()
        emailcheck = session.query(Competition).filter_by(organizer_email=useremail).one_or_none()
        if emailcheck is not None:
            return mod_comp
        else:
            print("You do not have the permissions to setup this competition.")
            return False

class Competition(Base):
    """
    Class using the SQLAlchemy library to create a database of competitions.

    """

    __tablename__ = "competitions"
    comp_code = Column(String, primary_key=True)
    name = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    reg_close = Column(String)
    dir = Column(String)
    organizer_email = Column(String)

    def __init__(self, comp_code, name, start_date, end_date, reg_close, dir, organizer_email):
        self.comp_code = comp_code
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.reg_close = reg_close
        self.dir = dir
        self.organizer_email = organizer_email

    def create_competition(useremail):
        """
        Function to create a new competition and initialize the basic information.

        Args:
            useremail (str) -> the email of the organizing user

        Returns:
            appends the competitons database
            directory for the competition (format: COMPCODE_YEAR)
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
        comp_code = getinput("code", "Please provide a 4-letter long competition code [e.g. HBEG]: ") + "_" + start_date[:4]
        
        print(f"Here's the provided information about your competition:")
        print(f"Competition name: {comp_name}\nCompetition code: {comp_code}")
        print(f"Start date: {start_date}\nEnd date: {end_date}\nRegistration closes: {reg_close}")
        finalcheck = getinput("y/n", "Is all the information correct? [Y/N]: ")
        if finalcheck == "N":
            print("Please try again.")
            return None
        filename = comp_code
        newpath = f"comps/{filename}"
        os.makedirs(newpath)

        session = Session()
        Base.metadata.create_all(bind=engine)
        new_comp = Competition(comp_code, comp_name, start_date, end_date, reg_close, newpath, useremail)
        session.add(new_comp)
        session.commit()


    def add_dances(useremail):
        """
        Function to add dances to an existing competition.

        Args:
            useremail (str) -> email of the current user

        Returns:
            .json file for every style (format: LEVEL_STYLE)

        """
        mod_comp = check_access(useremail)
        if mod_comp == False:
            return None

        dances = {}        
        levels = ['Newcomer', 'Bronze', 'Silver', 'Gold', 'Syllabus', 'Open']
        latin_dances = ['International_ChaCha', 'International_Rumba', 'Jive', 'Paso_Doble', 'Samba']
        rhytm_dances = ['American_ChaCha', 'American_Rumba', 'EastCoast_Swing', 'Bolero', 'Mambo']
        smooth_dances = ['American_Waltz', 'American_VWaltz', 'American_Foxtrot', 'American_Tango']
        standard_dances = ['International_Waltz', 'International_VWaltz', 'International_Tango', 'Quickstep']
        dance_categories = [latin_dances, rhytm_dances, smooth_dances, standard_dances]

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
            f_data = []
            with open(f"comps/{mod_comp.upper()}/{dancefile_name}.json", "w+") as f:
                json.dump(f_data, f, indent=4)

    def prepare_comp_list(useremail):
        """
        Function that prepares a list of heats and competitors before starting a competition.

        Args:
            useremail (str) -> operating user's email

        Returns:
            heatlist.json (.json file) -> heatlist file
        """

        mod_comp = check_access(useremail)
        if mod_comp == False:
            return None
        
        finalheats = []; sfheats = []; qfheats = []; r3heats = []; r2heats = []; r1heats = []
        compsdir = f"comps/{mod_comp.upper()}"
        levels = ['Newcomer', 'Bronze', 'Silver', 'Gold', 'Syllabus', 'Open']
        for level in levels:
            for file in glob(f"{compsdir}/{level}_*.json"):
                if "heatlist" not in os.path.basename(file):
                    with open(file, "r") as f:
                        filename = os.path.basename(file)
                        f = json.load(f)
                        competitors = f
                        if 24 < len(f):
                            r1heats.append(("Round1_" + filename, competitors)) 
                            competitors = []
                        if 20 < len(f):
                            r2heats.append(("Round2_" + filename, competitors))
                            competitors = []
                        if 16 < len(f):
                            r3heats.append(("Round3_" + filename, competitors))
                            competitors = []
                        if 10 < len(f):
                            qfheats.append(("Quarterfinal_" + filename, competitors))
                            competitors = []
                        if 6 < len(f):
                            sfheats.append(("Semifinal_" + filename, competitors))
                            competitors = []
                        if 0 < len(f):
                            finalheats.append(("Final_" + filename, competitors))

        allheats = r1heats + r2heats + r3heats + qfheats + sfheats + finalheats

        with open(f"{compsdir}/heatlist.json", "w+") as f:
            heatlist = {}
            for heat in range(len(allheats)):
                heatlist[f"Event_{heat+1}"] = {
                "event_name": allheats[heat][0][:-5],
                "event_contestants": allheats[heat][1]
                }
                    
            json.dump(heatlist, f, indent=4)
        
        print("Competition succesfully setup!")


    def run_comp(useremail):
        """
        Function to run a full competition, iterating over heats and choosing
        which competitors progress to the next round.

        Args:
            useremail (str) -> operating user's email
        
        Returns:
            detailedresults.json (.json file) -> raw data of all the results
        """

        mod_comp = check_access(useremail)
        if mod_comp == False:
            return None
        fn = 1; sf = 6; qf = 10; r3 = 16; r2 = 20; r1 = 24
        resultsdic = {}

        compsdir = f"comps/{mod_comp.upper()}"
        with open(f"{compsdir}/heatlist.json", "r") as f:
            heatlist = json.load(f)
            for i in range(1, len(heatlist)):
                event_name = heatlist[f"Event_{i}"]["event_name"]
                print(f"STARTING EVENT {i}")
                print(f"{event_name.upper()}\n")
                if "Final" in event_name: num_adv = 1
                if "Semi" in event_name: num_adv = 6
                if "Quarter" in event_name: num_adv = 10
                if "3" in event_name: num_adv = 16
                if "2" in event_name: num_adv = 20
                if "1" in event_name: num_adv = 24
                print(f"Please choose {num_adv} couples to go through to the next round.")
                print("Input the couples in the following format: 00, 01, 02..\n")

                print("COUPLES COMPETING IN THIS ROUND:")
                print(heatlist[f"Event_{i}"]["event_contestants"])
                while True:
                    try:
                        advancing_competitors = getinput("mulchoice", "YOUR CHOICES: ", num_adv)
                        advancing_competitors = re.findall(r'\d+', advancing_competitors)
                        advancing_competitors = [int(n) for n in advancing_competitors]
                        check_valid1 = set(advancing_competitors).issubset(set(heatlist[f"Event_{i}"]["event_contestants"]))
                        check_valid2 = len(advancing_competitors) == len(set(advancing_competitors))
                        print(check_valid1); print(check_valid2)
                        if check_valid1 == False: raise ValueError
                        if check_valid2 == False: raise IndexError
                        if check_valid1 and check_valid2 == True:
                            break
                    except ValueError:
                        print("Please only input competitors that are taking part in this round.")
                    except IndexError:
                        print("Please only input a partnership once.")

                for k in range(i, len(heatlist)):
                    if event_name in heatlist[f"Event_{k}"]["event_name"]:
                        set1 = set(heatlist[f"Event_{k}"]["event_contestants"]); set2 = set(advancing_competitors)
                        kicked_out_competitors = list(set1-set2)
                        resultsdic[f"Event_{k}"] = {
                            "event_name": event_name,
                            "kicked_out_competitors": kicked_out_competitors,
                            "advanced_competitors": advancing_competitors
                        }
                        break
                for j in range(i+1, len(heatlist)):
                    if event_name[10:] in heatlist[f"Event_{j}"]["event_name"]:
                        heatlist[f"Event_{j}"]["event_contestants"] = advancing_competitors
                        break

        with open(f"{compsdir}/detailedresults.json", "w") as f:
            json.dump(resultsdic, f, indent=4) 

    def produce_results(useremail):
        """
        Function that takes the raw result data from a recently run competition
        and produces a nicer summary in the form of a .csv file.

        Args:
            useremail (str) -> operating user's email

        Returns:
            results.json (.json file) -> .json file summarizing the outcomes of every heat
            results.csv (.csv file) -> spreadsheet presenting the detailed results of the competition

        """
        mod_comp = check_access(useremail)
        if mod_comp == False:
            return None
        compsdir = f"comps/{mod_comp.upper()}"

        events = []
        results = {}
        bannedfiles = ["heatlist.json", "detailedresults.json", "results.json", "results.csv", ".DS_Store"]
        for file in os.listdir(compsdir):
            filename = os.fsdecode(file)
            print(f"Found file: '{filename}'")
            if filename not in bannedfiles:
                events.append(filename)
        print(events)
        with open(f"{compsdir}/detailedresults.json", "r") as f:
            heatlist = json.load(f)
            for event in events:
                event = event[:-5]
                results[event] = {}
                for i in range(1, len(heatlist)+1):
                    if event[5:] in heatlist[f"Event_{i}"]["event_name"]:
                        prefix = re.match(r'^.*?_', heatlist[f"Event_{i}"]["event_name"])
                        results_update = {
                            f"{prefix.group()[:-1]}": heatlist[f"Event_{i}"]["kicked_out_competitors"],
                            "Winner": heatlist[f"Event_{i}"]["advanced_competitors"]
                        }
                        results[event].update(results_update)

        with open(f"{compsdir}/results.json", "w") as f:
            json.dump(results, f, indent=4)

        with open(f"{compsdir}/results.json", "r") as f:
            results = json.load(f)
            with open(f"{compsdir}/results.csv", "w") as csvf:
                columns = ["Level", "Event", "Round 3", "Round 2", "Round 1", "Quarterfinalists", "Semifinalists", "Finalists", "Winner"]
                writer = csv.DictWriter(csvf, fieldnames=columns)
                writer.writeheader()
                for result in results:
                    print(result)
                    parts = result.split("__", 1)
                    level = parts[0]
                    event_name = re.sub(r'_', ' ', parts[1])
                    writer.writerow({
                        "Level": level,
                        "Event": event_name,
                        "Round 3": results[result].get("Round_3", "X"),
                        "Round 2": results[result].get("Round_2", "X"),
                        "Round 1": results[result].get("Round_1", "X"),
                        "Quarterfinalists": results[result].get("Quarterfinal", "X"),
                        "Semifinalists": results[result].get("Semifinal", "X"),
                        "Finalists": results[result].get("Final", "X"),
                        "Winner": results[result].get("Winner", "X"),
                    })




            