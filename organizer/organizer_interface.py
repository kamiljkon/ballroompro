from organizer.organizer_backend import Competition
from helperfunctions import getinput
from accountmanagement import signup, login

def main():
    loginstatus = False
    new_comp = Competition(1234)
    while loginstatus == False:
        print("\n########")
        print("Welcome to BallroomPro. Please register or login.")
        print("########")
        print("[1]. Register\n[2]. Login\n")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 2)
        if menuchoice == 1:
            signup("organizer")
        if menuchoice == 2:
            useremail, loginstatus = login()
            print(useremail, loginstatus)

    """
    Opening interface to choose a next step from the menu.
    """
    in_menu = True
    while in_menu:
        print("########")
        print("Welcome to BallroomPro organizing interface.")
        print("########")
        print("Please choose one of the options below:\n")
        print("[1]. Create a new competition\n[2]. Add dances to a competition")
        print("[3]. View your current competition\n")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 3)
        if menuchoice == 1:
            new_comp.create_competition(useremail)
        if menuchoice == 2:
            new_comp.add_dances(useremail)

main()