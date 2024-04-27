import os
import sys 
import json

sys.path.insert(0, "/Users/kamilkon/ballroompro")

from organizer_backend import Competition
from helperfunctions import getinput, findkey
from accountmanagement import User, Partnership
from competitor_backside import new_partnership, add_to_comp
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import or_
from sqlalchemy.exc import OperationalError

import hashlib
Base = declarative_base()
engine = create_engine("sqlite:///data.db", echo=False)
Session = sessionmaker(bind=engine)

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
            User.signup("C")
        if menuchoice == 2:
            useremail, loginstatus = User.login()
            return useremail, loginstatus

def currentpartnerships(useremail):
    """
    String representation of the current partnerships of the user.

    Args:
        useremail (str) -> current user
    
    Returns:
        string output for the useremail's partnerships
    """

    session = Session()
    try:
        partnerships = session.query(Partnership).filter(
            or_(
                Partnership.leader_email == useremail,
                Partnership.follower_email == useremail
            )).all()
        if not partnerships:
            print("### YOU HAVE CURRENTLY NO PARTNERSHIPS ###")
        else:
            print("### YOUR CURRENT PARTNERSHIPS: ###")
            for partnership in partnerships:
                leader = session.query(User).filter(User.email == partnership.leader_email).first()
                follower = session.query(User).filter(User.email == partnership.follower_email).first()
                print(f"LEADER: {leader.name.title()} /// FOLLOWER: {follower.name.title()} [ID: {partnership.partnershipid}]")
    except OperationalError as e:
        print(f"Error {e} has occurred, no partnerships accessible right now.")


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
        currentpartnerships(useremail)
        print("########")
        print("\nPlease choose one of the options below:\n")
        print("[1]. Create partnership\n[2]. Register for dances")
        print("[3]. TBD\n")
        menuchoice = getinput("xchoices", "Select one of the options above: ", 3)
        if menuchoice == 1:
            new_partnership(useremail)
        if menuchoice == 2:
            add_to_comp()

def int_main():
    useremail, loginstatus = loginmenu()
    interface(useremail, loginstatus)

if __name__ == "__main__":
    int_main()