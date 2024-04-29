from .organizer_backend import Competition
from helpfunctions.helperfunctions import getinput
from helpfunctions.accountmanagement import User
import sys

def org_main():
    """
    Opening interface to login/register and choose a next step from the menu.
    """

    loginstatus = False
    while loginstatus == False:
        print("\n########")
        print("Welcome to BallroomPro. Please register or login.")
        print("########")
        print("[1]. Register\n[2]. Login\n")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 2)
        if menuchoice == 1:
            User.signup("O")
        if menuchoice == 2:
            user_email, loginstatus = User.login()

    # DEBUG
    # user_email = "hbdt@gmail.com"

    in_menu = True
    while in_menu:
        print("########")
        print("Welcome to BallroomPro organizing interface.")
        print("########")
        print("Please choose one of the options below:\n")
        print("[1]. Create a new competition\n[2]. Add dances to a competition")
        print("[3]. Setup competition\n[4]. Run competition")
        print("[5]. Produce a reuslt list for your competition")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 5)
        if menuchoice == 1:
            Competition.create_competition(user_email)
        if menuchoice == 2:
            Competition.add_dances(user_email)
        if menuchoice == 3:
            Competition.prepare_comp_list(user_email)
        if menuchoice == 4:
            Competition.run_comp(user_email)
        if menuchoice == 5:
            Competition.produce_results(user_email)

if __name__ == "__main__":
    org_main()