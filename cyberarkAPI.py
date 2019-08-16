import datetime
from typing import Any

import requests


class cyberarkAPI:
    appID = safe = actName = folder = host = aimURL = cpmDisableReason = None
    cpmDisable = False
    cpmStatus = "success"

    HEADERS = {'content-type': 'application/json'}
    querystring = aimData = dict()

    def __new__(cls):
        return super().__new__(cls)

    def __init__(self, appid="", safe="", actname="", host="", folder="Root"):
        self.appID = appid
        self.safe = safe
        self.actName = actname
        self.host = host
        self.aimURL = "https://" + self.host + "/AIMWebService/api/Accounts"
        self.folder = folder
        self.querystring = {"AppID": self.appID, "Safe": self.safe, "Folder": self.folder, "Object": self.actName}

    def setappID(self, appid):
        self.appID = appid

    def setSafe(self, safe):
        self.safe = safe

    def setActName(self, actname):
        self.actName = actname

    def setFolder(self, folder):
        self.folder = folder

    def setHost(self, host):
        self.host = host

    def getaimResponse(self):
        response = requests.request("GET", self.aimURL, headers=self.HEADERS, params=self.querystring)

        if response.status_code in [200, 400, 403, 404]:
            return response
        else:
            response.raise_for_status()

    def getaimData(self):
        self.aimData = self.getaimResponse().json()
        return self.aimData

    def getUsername(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.aimData['UserName']

    def getPassword(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.aimData['Content']

    def getAddress(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.aimData['Address']

    def getCPMStatus(self):
        if self.isAIMError():
            return self.getAIMError()
        elif "CPMStatus" in self.aimData.keys() and self.aimData['CPMStatus'] == "success":
            self.cpmStatus = "success"
            return self.cpmStatus
        elif "CPMStatus" in self.aimData.keys() and self.aimData['CPMStatus'] != "success":
            self.cpmStatus = self.aimData['CPMStatus']
            return self.cpmStatus
        else:
            pass

    def getCPMDisabled(self):
        if self.isAIMError():
            return self.getAIMError()
        elif "CPMDisabled" in self.aimData.keys():
            self.cpmDisableReason = self.aimData['CPMDisabled']
            self.cpmDisable = True
            return self.cpmDisable
        else:
            self.cpmDisable = False
            return self.cpmDisable

    def getLastSuccessChange(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.aimData['LastSuccessChange']))

    def getNextChange(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessChange() + datetime.timedelta(days=30)

    def getLastSuccessChangeTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessChange().isoformat()

    def getLastSuccessReconciliation(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.aimData['LastSuccessReconciliation']))

    def getLastSuccessReconciliationTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessReconciliation().isoformat()

    def getLastSuccessVerification(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.aimData['LastSuccessVerification']))

    def getNextVerification(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessVerification() + datetime.timedelta(days=7)

    def getLastSuccessVerificationTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessVerification().isoformat()

    def getLastTask(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.aimData['LastTask']

    def getPasswordChangeInProcess(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return bool(self.aimData['PasswordChangeInProcess'])

    def isAIMError(self):
        if "ErrorCode" in self.aimData.keys():
            return True
        else:
            return False

    def getAIMError(self):
        if "ErrorCode" in self.aimData.keys():
            raise Exception("ErrorCode: " + self.aimData['ErrorCode'] + "-" + self.aimData['ErrorMsg'])
        else:
            pass

