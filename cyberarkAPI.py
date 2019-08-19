import datetime

import requests


class CyberarkAPI:
    __cpmDisableReason, __cpmStatus, __aimURL = "", "success", "https://"
    __cpmDisable = False
    __aimData = dict()

    def __init__(self, appid="", safe="", actname="", host="", folder="Root"):
        super().__init__()
        self.appID = appid
        self.safe = safe
        self.actName = actname
        self.host = host
        self.folder = folder

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
        self.setaimURL(host)

    def getHost(self):
        return self.host

    def setaimURL(self, host):
        self.__aimURL = "https://" + host + "/AIMWebService/api/Accounts"

    def getquerystring(self):
        return {"AppID": self.appID, "Safe": self.safe, "Folder": self.folder, "Object": self.actName}

    def getaimURL(self):
        return self.__aimURL

    def getaimResponse(self):
        HEADERS = {'content-type': 'application/json'}
        querystring = self.getquerystring()
        response = requests.request("GET", self.__aimURL, headers=HEADERS, params=querystring)

        if response.status_code in [200, 400, 403, 404]:
            return response
        else:
            response.raise_for_status()

    def getaimData(self):
        self.__aimData = self.getaimResponse().json()
        return self.__aimData

    def getUsername(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.__aimData['UserName']

    def getPassword(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.__aimData['Content']

    def getAddress(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.__aimData['Address']

    def getCPMStatus(self):
        if self.isAIMError():
            return self.getAIMError()
        elif "CPMStatus" in self.__aimData.keys() and self.__aimData['CPMStatus'] == "success":
            self.cpmStatus = "success"
            return self.cpmStatus
        elif "CPMStatus" in self.__aimData.keys() and self.__aimData['CPMStatus'] != "success":
            self.cpmStatus = self.__aimData['CPMStatus']
            return self.cpmStatus
        else:
            pass

    def getCPMDisabled(self):
        if self.isAIMError():
            return self.getAIMError()
        elif "CPMDisabled" in self.__aimData.keys():
            self.__cpmDisableReason = self.__aimData['CPMDisabled']
            self.__cpmDisable = True
            return self.__cpmDisable
        else:
            self.__cpmDisable = False
            return self.__cpmDisable

    def getCPMDisabledReason(self):
        return self.__cpmDisableReason

    def getLastSuccessChange(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.__aimData['LastSuccessChange']))

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
            return datetime.datetime.fromtimestamp(int(self.__aimData['LastSuccessReconciliation']))

    def getLastSuccessReconciliationTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessReconciliation().isoformat()

    def getLastSuccessVerification(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.__aimData['LastSuccessVerification']))

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
            return self.__aimData['LastTask']

    def getPasswordChangeInProcess(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return bool(self.__aimData['PasswordChangeInProcess'])

    def isAIMError(self):
        if "ErrorCode" in self.__aimData.keys():
            return True
        else:
            return False

    def getAIMError(self):
        if "ErrorCode" in self.__aimData.keys():
            raise Exception("ErrorCode: " + self.__aimData['ErrorCode'] + "-" + self.__aimData['ErrorMsg'])
        else:
            pass

