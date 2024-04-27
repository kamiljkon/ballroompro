# Simple registration and login functions using hashing
import hashlib
import json
import uuid

def signup(interface):
    """
    Function to register a profile.

    Args:
        interface (str) -> type of account to be created (e.g. organizer, competitor)
    
    Returns:
        competitionsdata.json
    """
    email = input("Enter email adress: ")
    name = input("Enter name and surname: ").lower()
    password = input("Enter password: ")
    conf_password = input("Confirm password: ")
    if conf_password == password:
        encoded = conf_password.encode()
        hashedpass = hashlib.md5(encoded).hexdigest()

        userid = str(uuid.uuid4())
    
        try:
            with open("userdata.json", "r") as f:
                f_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            f_data = {}

        authorized_comps = []
        if email not in f_data:
            f_data[email] = {
                "email": email,
                "name": name,
                "userid": userid,
                "account_type": interface,
                "password": hashedpass,
                "authorized_comps": []
                }
        else:
            print("Email already registered.")
            return None
        
        with open("userdata.json", "w") as f:
            json.dump(f_data, f, indent=4)

        print("You have registered successfully!\n")

    else:
        print("Password is not the same as above! \n")

def login():
    """
    Function to login and verify a user.

    Returns:
        userid (str) -> userid of the loggedin user
        True (bool) -> confirmation of succesful log-in
    """
    email = input("Enter email: ")
    password = input("Enter password: ")

    auth = password.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    with open("userdata.json", "r") as f:
        f_data = json.load(f)
        while True:
            try: 
                stored_pass = f_data[email]["password"]
                break
            except KeyError:
                print("E-mail doesn't exist.")
    f.close()

    if auth_hash == stored_pass:
        print("Logged in successfully!")
        userid = f_data[email]["userid"]
        return email, True
    else:
        print("Login failed!\n")
