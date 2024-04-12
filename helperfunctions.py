import datetime

def getinput(type, instring, maxval=None):
    """
    Makes input processing easier by condensing the try/except code
    into one function. 
    'type' parameter takes in the type of the
    input desired (integer, boolean etc.)
    'input' takes in the desired string to be printed.
    """

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
                if 0 < output < maxval+1:
                    return output
                else:
                    raise ValueError
            except ValueError:
                print("Invalid format, please try again.")