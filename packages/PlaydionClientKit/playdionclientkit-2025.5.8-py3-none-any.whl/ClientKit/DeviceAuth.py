import requests
import webbrowser
import ClientKit

global devicecode
global authstatus
global requestid



def open_auth_website():
    webbrowser.open_new("https://onlineservices.adriandevprojects.com/v1/auth/devicelogin/")
    return

def initialize_auth():
    global devicecode
    global requestid
    auth_url = "https://onlineservices.adriandevprojects.com/v1/auth/devicelogin/new/"


    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if ClientKit.checklogin() is False:
        response = requests.post(auth_url, headers=headers)
        data = response.json()
        requestid = data['requestid']
        devicecode = data['devicecode']

        return check_auth(requestid)
    else:
        return "Already logged in"





def check_auth(requestid):
    global authstatus
    global devicecode


    open_auth_website()
    print("Waiting for authentication... CODE:")
    print(devicecode)


    auth_url = "https://onlineservices.adriandevprojects.com/v1/auth/devicelogin/check/"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    rid = {
        "requestid": requestid
    }

    success = False

    while success is False:
        response = requests.post(auth_url, headers=headers, data=rid)
        data = response.json()
        status = data['status']
        if status == "SUCCESS":
            userid = data['userid']
            with open("userdata.txt", "w+") as accfile:
                accfile.write(userid)
                success = True
                authstatus = "SUCCESS"
                break

        elif status == "WAITING":
            authstatus = "WAITING"
            continue

        else:
            authstatus ="FAILED"
            break



    return True




def get_device_code():
    global devicecode
    return devicecode

def get_request_id():
    global requestid
    return requestid