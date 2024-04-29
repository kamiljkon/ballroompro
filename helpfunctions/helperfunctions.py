import datetime

def getinput(type, instring, maxval=None):
    """
    Makes input processing easier by condensing the try/except code
    into one function. 

    Args:
        type (str) -> takes in type of input desired (integer, boolean etc.)
        instring (str) -> the string to be printed
        maxval (int, def=None) -> for xchoices type, selects maximum value; for mulchoice, selects number of expected choices

    Returns:
        choice
    """

    if type == " ":
        return None

    if type == "y/n":
        while True:
            output = input(instring)
            if output != "Y".upper() or "N".upper():
                break
            else:
                print("Invalid format, please try again.")
        return output

    if type == "date":
        while True:
            output = input(instring)
            try:
                output = datetime.datetime.strptime(output, "%Y/%m/%d")
                break
            except ValueError:
                print("Invalid format, please try again.")
        return str(output.date())
    
    if type == "code":
        while True: 
            output = input(instring)
            try:
                if len(output) != 4:
                    raise ValueError
                else: 
                    break
            except ValueError:
                print("Invalid format, please try again.")
        return output
    
    if type == "xchoices":
        while True:
            output = input(instring)
            if output.upper() == "EXIT":
                return int(404)
            if output.upper() == "BACK":
                return int(304)
            else:
                output = int(output)
            try:
                if maxval == None: 
                    if 0 <= output:
                        return output
                else:
                    if 0 <= output < maxval+1:
                        return output
                    else:
                        raise ValueError
            except ValueError:
                print("Invalid format, please try again.")

    if type == "mulchoice":
        while True:
            output = input(instring)
            try:
                if output.count(",") != maxval-1:
                    raise ValueError
                else:
                    return output
            except ValueError:
                print("Invalid format, please try again.")

def findkey(dict, target_value):
    """
    Helps find the corresponding key to a value, such as userid.

    Args:
        dict (dict) -> the dictionary to be searched
        target_value () -> the value searched for
    
    Returns:
        key (str) -> the key corresponding to the value
    """
    for key, value in dict.items():
        if value == target_value:
            return key
    return None