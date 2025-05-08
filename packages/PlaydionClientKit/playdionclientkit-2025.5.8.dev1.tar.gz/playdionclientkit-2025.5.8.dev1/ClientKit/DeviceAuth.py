import requests

global devicecode
global authstatus

def initialize_auth():
    global devicecode
    auth_url = "https://onlineservices.adriandevprojects.com/v1/auth/devicelogin/new/"


    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(auth_url, headers=headers)
    data = response.json()
    requestid = data['requestid']
    devicecode = data['devicecode']

    check_auth(requestid)



def check_auth(requestid):
    global authstatus
    global devicecode
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
            authstatus = "Waiting for user to verify the device..."
            continue

        else:
            authstatus ="Login failed: " + status
            break


def get_auth_status():
    global authstatus
    return authstatus



