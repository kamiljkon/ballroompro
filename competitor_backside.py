from helperfunctions import getinput
from accountmanagement import User, Partnership
import os, json
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import hashlib
from organizer_backend import Competition
Base = declarative_base()
engine = create_engine("sqlite:///data.db", echo=False)
Session = sessionmaker(bind=engine)

def new_partnership(useremail):
    """
    Function to create new partnerships.

    Args:
        useremail (str) -> email of the operating user

    Returns:
        Creates a partnership object and appends the dataset
        
    """
    print("\n#######\nTo create a new partnership, input your partner's and the partnerships details.")
    print("BEWARE! If you plan switching between leading/following in various styles, you have to create two partnerships.\n")
    
    partnername = input("Please input your partner's last name: ").lower()

    session = Session()
    potentialpartners = session.query(User).filter(
        User.name.like(f"%{partnername}%"),
        User.account_type == "C").all()
    if len (potentialpartners) == 0:
        print(f"Found no partner with lastname {partnername}.")
        return None      
    if len(potentialpartners) == 1:
        print("Found your partner!")
        for partner in potentialpartners:
            partneremail = partner.email
    else:
        i = 1
        for partner in potentialpartners:
            print(f"Partner {i}:\nName: {partner.name}\nEmail: {partner.email}\n")
            i += 1
        partnerchoice = getinput("xchoices", "Found multiple partners, please select the correct one from the list: ", i)
        partneremail = potentialpartners[partnerchoice-1].email
    
    print("Please indicate your role in the partnership.")
    leadfollow = getinput("y/n", "Will you be leading [Y] or following [N]?: ")
    if leadfollow == "Y":
        leader_email = useremail
        follower_email = partneremail
    else:
        leader_email = partneremail
        follower_email = useremail
    
    existing_partnership = session.query(Partnership).filter(
        Partnership.leader_email == leader_email,
        Partnership.follower_email == follower_email).first()
    if existing_partnership:
        print("This partnership already exists.")
        return None
    
    new_partnership = Partnership(
        leader_email=leader_email,
        follower_email=follower_email)
    session.add(new_partnership)
    session.commit()
    print("Partnership succesfully added.")
        
def add_to_comp():
    """
    Function to register a partnership to an existing competition.

    Returns:
        Appends the .json file of the dance for which the partnership registered.
    
    """
    session = Session()
    avail_comps = session.query(Competition).all()
    print("#### AVAILABLE COMPETITIONS ####")
    for i, comps in enumerate(avail_comps):
        print(f"{i}. {comps.name}")
    choice = int(getinput("xchoices", "Which comp do you want to sign up for?: ", i+1))
    comp = avail_comps[choice].comp_code

    partnership = int(getinput("xchoices", "State the partnership ID for the partnership you're registering: "))
    #leader

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
        dancelist = os.listdir(f'comps/{comp}')
        print("## CHOOSE DANCES TO ADD ##")
        available_dances = [dance for dance in category if f"{level}__{dance}" in dancelist]

        for i, dance in enumerate(available_dances, 1):
            print(f"{i}. {dance.upper()}")

        dance_choice = (getinput("xchoices", "Choose a dance to add. If you wish to return, type [BACK]: ", len(available_dances)))
        if dance_choice == 404:
            return None
        if dance_choice == 304:
            break
        selected_dance = available_dances[dance_choice - 1]
        dance_filename = f"{level}__{selected_dance}"
        dance_filepath = f"comps/{comp}/{dance_filename}.json"

        if not os.path.exists(dance_filepath):
            with open(dance_filepath, 'w') as f:
                json.dump([], f) 

        with open(dance_filepath, 'r+') as f:
            dance_data = json.load(f)
            # Modify dance_data as needed
            if partnership not in dance_data:
                dance_data.append(partnership) 
                f.seek(0)
                json.dump(dance_data, f, indent=4)
                print(f"Updated {selected_dance} in {comp} successfully!")
            else:
                print("You are already registered for the dance!")