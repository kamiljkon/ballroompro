import os
import sys 
import json

sys.path.insert(0, "/Users/kamilkon/ballroompro")

from organizer.organizer_backend import Competition
from helperfunctions import getinput, findkey
from accountmanagement import signup, login
from competitor.competitor_backside import new_partnership

def loginmenu():
    """
    Interface to register or login.

    Returns:
        useremail (str) -> logged in email's user
        loginstatus (bool) -> confirmation of login
    """
    loginstatus = False
    while loginstatus == False:
        print("\n########")
        print("Welcome to BallroomPro. Please register or login.")
        print("########")
        print("[1]. Register\n[2]. Login\n")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 2)
        if menuchoice == 1:
            signup("competitor")
        if menuchoice == 2:
            useremail, loginstatus = login()
            return useremail, loginstatus

def currentpartnerships(useremail):
    """
    String representation of the current partnerships of the user.

    Args:
        useremail (str) -> current user
    
    Returns:
        cur_partnerships (str) -> string featuring current partnerships
    """
    with open("userdata.json", "r") as f:
        f_data = json.load(f)
        userid = f_data[useremail]["userid"]
        print(userid)

    partnerships = []
    with open("partnerships.json", "r") as f:
        f_data = json.load(f)
        for partnership in f_data:
            print(partnership)
            if userid in partnership[0]:
                leader, follower = partnership[0][0], partnership[0][1]
                partnerships.append((leader, follower))
    print(partnerships)

    with open("userdata.json", "r") as f:
        f_data = json.load(f)
        leaders = []; followers = []
        for partner in partnerships:
            leader = findkey(f_data, partner[0])
            leaders.append(leader)
            follower = findkey(f_data, partner[1])
            followers.append(follower)
        print(leaders, followers)
    
    cur_partnerships = "\n#######\nYour current partnerships are:\n"
    for i in range(len(partnerships)):
        str = f"Leader: {leaders[i]} dances with follower: {followers[i]}\n"
        cur_partnerships += str
    
    return cur_partnerships


    

def interface(useremail, loginstatus):
    """
    Opening interface to choose a next step from the menu.

    Args:
        useremail (str) -> operating user's email
        loginstatus (bool) -> confirmation of succesful login
    """

    in_menu = True
    while in_menu:
        print("########")
        print("Welcome to BallroomPro organizing interface.")
        print("########")
        print(currentpartnerships(useremail))
        print("Please choose one of the options below:\n")
        print("[1]. Create partnership\n[2]. TBD")
        print("[3]. TBD\n")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 3)
        if menuchoice == 1:
            new_partnership(useremail)


useremail, loginstatus = loginmenu()
interface(useremail, loginstatus)