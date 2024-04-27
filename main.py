from helperfunctions import getinput
from organizer_interface import org_main
from competitor_interface import int_main

def main():
    """
    Initializing code from the user's point of view, allows selection of the interface to be run.

    """
    
    print("\n########")
    print("Welcome to BallroomPro. Please choose which interface to run.")
    print("########")
    print("[1]. Competitor\n[2]. Organizer\n")
    menuchoice = getinput("xchoices", "Select one of the options above: ", 2)
    if menuchoice == 1:
        int_main()
    if menuchoice == 2:
        org_main()

if __name__ == "__main__":
    main()