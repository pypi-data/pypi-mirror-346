import webbrowser
from pathlib2 import Path

def info():
    print("Playdion ClientKit v2025.5.8rc1")



def checklogin():
    accfile = Path("userdata.txt")
    if accfile.is_file():
        with open("userdata.txt", "r") as accfile:
            userid = accfile.read()
            if userid is not None or "":
                return True
            else:
                return False
    else:
        return False


def getuserid():
    state = checklogin()
    if state is True:
        with open("userdata.txt", "r") as accfile:
            userid = accfile.read()
            return userid
    else:
        return False


def open_auth_url():
    auth_url = "https://onlineservices.adriandevprojects.com/v1/auth/devicelogin/"
    webbrowser.open_new(auth_url)