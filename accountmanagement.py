# Simple registration and login functions using hashing
import hashlib
import json

def signup():
    email = input("Enter email adress: ")
    password = input("Enter password: ")
    conf_password = input("Confirm password: ")
    if conf_password == password:
        encoded = conf_password.encode()
        hashedpass = hashlib.md5(encoded).hexdigest()
    
        with open("userdata.json", "r+") as f:
            try:
                f_data = json.load(f)
            except json.JSONDecodeError:
                f_data = {}
            f_data[email] = []
            authorized_comps = []
            if email not in f_data:
                f_data[email] = []
            f_data[email].append((hashedpass, authorized_comps))
            json.dump(f_data, f, indent=4)

        print("You have registered successfully!\n")

    else:
        print("Password is not the same as above! \n")

def login():
    email = input("Enter email: ")
    password = input("Enter password: ")

    auth = password.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    with open("userdata.json", "r") as f:
        f_data = json.load(f)
        while True:
            try: 
                stored_pass = f_data[email][0][0]
                break
            except KeyError:
                print("E-mail doesn't exist.")
    f.close()

    if auth_hash == stored_pass:
        print("Logged in successfully!")
        return email, True
    else:
        print("Login failed!\n")
