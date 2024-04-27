from helperfunctions import getinput
import os, json

def new_partnership(userid):
    print("To create a new partnership, input your partner's and the partnerships details.")
    print("BEWARE! If you plan switching between leading/following in various styles, you have to create two partnerships.\n")
    partnername = input("Please input your partner's last name: ")
    potentialpartners = []
    with open("userdata.json", "r") as f:
        f_data = json.load(f)
        for name in f_data["name"]:
            if partnername in name:
                potentialpartners.append((name, f_data["email"], userid))
        if len(potentialpartners) == 0:
            print(f"Found no partner with lastname {partnername}.")
            return None
        if len(potentialpartners) == 1:
            print("Found your partner!")
            partnerid = potentialpartners[0][2]
        if len(potentialpartners) > 1:
            for i in len(potentialpartners):
                print(f"Partner {i}: {potentialpartners[i]}")
            partnerchoice = getinput("xchoices", "Found multiple partners, please select the correct one from the list: ")
            partnerid = potentialpartners[partnerchoice][2]

        leadfollow = getinput("Y/N", "Will you be leading [Y] or following [N]?: ")
        if leadfollow == "Y":
            partnership = (userid, partnerid)
        else:
            partnership = (partnerid, userid)
    
    teamname = input("Please state a short team name for your partnership. No spacebars!: ")
    with open("partnerships.json", "r") as f:
        f_data = json.load(f)
        f_data[teamname].append(partnership)
    with open("partnerships.json", "w") as f:
        json.dump(f_data, f, indent=4)
        
                



def add_to_comp(userid, comp):
    levels = ['Newcomer', 'Bronze', 'Silver', 'Gold', 'Syllabus', 'Open']
    latin_dances = ['International_ChaCha', 'International_Rumba', 'Jive', 'Paso_Doble', 'Samba']
    rhytm_dances = ['American_ChaCha', 'American_Rumba', 'EastCoast_Swing', 'Bolero', 'Mambo']
    smooth_dances = ['American_Waltz', 'American_VWaltz', 'American_Foxtrot', 'American_Tango']
    standard_dances = ['International_Waltz', 'International_VWaltz', 'International_Tango', 'Quickstep']
    dance_categories = [latin_dances, rhytm_dances, smooth_dances, standard_dances]
    
    print("\n#######")
    print("# 1. NEWCOMER\n# 2. BRONZE\n# 3. SILVER\n# 4. GOLD\n# 5. SYLLABUS\n# 6. OPEN")
    print("#######")
    input_level = getinput("xchoices", "Choose the competition level you wish to compete at [1-6]. If you are done, type [EXIT]: ", 6)
    if input_level == 404: return None
    level = levels[input_level-1]

    print("## CHOOSE CATEGORY ")
    print("# 1. LATIN\n# 2. RHYTM\n# 3. SMOOTH\n# 4. STANDARD")
    category = getinput("xchoices", "Choose one of the categories [1-4]. If you wish to return, type [EXIT]: ", 4)
    if category == 404: return None
    category = dance_categories[category-1]

    while True:
        dancelist = os.listdir('{comp}/')
        print("## CHOOSE DANCES TO ADD ##")
        if category == latin_dances:
            for dance in latin_dances:
                if f"{level}__{dance}" in dancelist:
                    i = 1
                    print(f"{i}. {dance.upper()}")
                    i += 1
        if category == rhytm_dances:
            for dance in latin_dances:
                if f"{level}__{dance}" in dancelist:
                    i = 1
                    print(f"{i}. {dance.upper()}")
                    i += 1
        if category == smooth_dances:
            for dance in latin_dances:
                if f"{level}__{dance}" in dancelist:
                    i = 1
                    print(f"{i}. {dance.upper()}")
                    i += 1
        if category == standard_dances:
            for dance in latin_dances:
                if f"{level}__{dance}" in dancelist:
                    i = 1
                    print(f"{i}. {dance.upper()}")
                    i += 1
        if category == 1 or 2:
            adding_dances = getinput("xchoices", "Choose a dance to add [1-5]. If you wish to return, type [BACK]. If you wish to go back to the main menu, type [EXIT]: ", 5)
        else:
            adding_dances = getinput("xchoices", "Choose a dance to add [1-4]. If you wish to return, type [BACK]. If you wish to go back to the main menu, type [EXIT]: ", 4)
            ### UNFINISHED == CONTINUE FROM HERE