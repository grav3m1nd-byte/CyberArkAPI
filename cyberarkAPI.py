import datetime

import requests
from requests import HTTPError


# Class created as "framework" to perform CyberArk AIMWebService API Calls. This framework allows the creating
# multiple objects, which in turn allows retrieving multiple accounts.


class CyberarkAPI:
    # Private attributes can only receive values through the methods in this class.
    __cpmDisableReason, __cpmStatus, __aimURL = "", "success", "https://"

    # Boolean private attribute to be used for comparative statements to make sure the account management is enabled
    # or disabled. By default, it is assumed the account management will be enabled. To get the true management state,
    # the API call must happen first. To get the status, call the method getCPMDisabled(), which will also pull the
    # "disable reason" from the json output key value.
    __cpmDisable = False

    # Private attribute of dictionary data type that will contain the json output (dictionary) returned by the
    # AIMWebService API call. It can only be called by using the method getaimData(). In turn, this method is the one
    # to call so the API call happens.
    __aimData = dict()

    # The constructor method is used to initialize data. It is meant to assign default values to some of the
    # attributes required when creating object of this class. Default values are empty, except for the folder
    # attribute which by default should point to 'Root'.
    def __init__(self, appid="", safe="", actname="", host="", folder="Root"):
        self.appID = appid  # Initializing the appID public attribute. Provided by the CyberArk Admins.
        self.safe = safe  # Initializing the safe public attribute. Provided by the CyberArk Admins.
        self.actName = actname  # Initializing the actName public attribute. The actName attribute name is the
        # CyberArk account object name which is provided by the CyberArk Admins.

        self.__host = host  # Initializing the host private attribute. This attribute refers to the CyberArk DNS name
        # or IP address which hosts the AIMWebService. In case the system running a Python3 code with instances of
        # this class does not have the network's DNS servers configured, the python code should have its own methods
        # to query the network's DNS servers independently from the system's DNS configuration, so the CyberArk DNS
        # name is provided as host instead of an IP address.

        self.folder = folder  # Initializing the folder public attribute. By default, accounts are stored in the
        # safe's 'Root' folder, unless is configured otherwise. If so, the CyberArk Admins should provide this along
        # with the AppID, Object, and Safe.

    # To pass the host value, which is required to be passed to the object, it cannot be passed directly as __host is
    # a private attribute, and for this, the host setter 'setHost()' must be called, which also passes the value to
    # __aimURL through __setaimURL() to compose the URL.
    def setHost(self, host):
        self.__host = host
        self.__setaimURL(self.__host)

    # The method to pass values to the __aimURL is also a private method and values can only be passed to it by
    # setHost() which calls __setaimURL()
    def __setaimURL(self, host):
        self.__aimURL = "https://" + host + "/AIMWebService/api/Accounts"

    # As __host and __aimURL are private attributes, both get methods getHold() and getaimURL() must be used to
    # return the values.
    def getHost(self):
        return self.__host

    def getaimURL(self):
        return self.__aimURL

    # Private method is only meant to return a dictionary with each parameter required for the AIMWebService API Call
    def __getquerystring(self):
        return {"AppID": self.appID, "Safe": self.safe, "Folder": self.folder, "Object": self.actName}

    # Private method is responsible for performing the HTTP request using the values provided by getaimURL() and
    # __getquerystring(), stored in the local variable querystring. What the HTTP request returns, will be used to
    # create an instance of the requests class.
    def __getaimResponse(self):
        HEADERS = {'content-type': 'application/json'}  # Headers local variable is meant to be a constant
        # dictionary, defining the content type, which will be provided to the HTTP GET request.

        try:
            # Instance of the requests module, which will have the data returned by the HTTP GET request.
            response = requests.get(self.getaimURL(), params=self.__getquerystring(), headers=HEADERS)

            # IF statement will use the status codes returned from the HTTP GET request and raise an exception only IF
            # the status codes are not 200, 400, 403, 404. CyberArk will return its own message when returning status
            # codes 400, 403 and 404.
            if response.status_code not in [200, 400, 403, 404]:  # If the status code is not in the list, a HTTP
                # request exception will be raised for the status code.
                response.raise_for_status()
        except HTTPError as http_err:  # Raise HTTP Error Exceptions if something else occurred.
            print(f'HTTP error occurred: {http_err}')

        else:  # If no exception is raised, and status codes are 200, 400, 403, or 404, return the response object.
            if response.status_code in [200, 400, 403, 404]:
                return response

    # Public method used to engage in the CyberArk AIMWebService API call and store the json output into the private
    # attribute __aimData and returning it. By doing this, this method only needs to run once, and following getter
    # methods will call the specific key in __aimData. By retrieving the key in __aimData, the HTTP request only
    # needs to happen once as well through this method.
    def getaimData(self):
        self.__aimData = self.__getaimResponse().json()
        return self.__aimData

    # Public method to retrieve the UserName key value from __aimData as long as isAIMError() returns false. The
    # isAIMError() public # method returns true only if the 'ErrorCode' key exists in __aimData and it  will only be
    # retrieved IF # AIMWebService returns a status code 400, 403, or 404.
    def getUsername(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.__aimData['UserName']

    # Public method to retrieve the Content key value from __aimData as long as isAIMError() returns false. The
    # Content key value is the CyberArk Object password for which the AIMWebService API call is usually done. The
    # isAIMError() public # method returns true only if the 'ErrorCode' key exists in __aimData and it  will only be
    # retrieved IF # AIMWebService returns a status code 400, 403, or 404.
    def getPassword(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.__aimData['Content']

    # Public method to retrieve the Address key value from __aimData as long as isAIMError() returns false. The
    # Address key value is where the UserName/Password can be used to authenticate against. The isAIMError() public
    # method returns true only if the 'ErrorCode' key exists in __aimData and it  will only be retrieved IF
    # AIMWebService returns a status code 400, 403, or 404.
    def getAddress(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.__aimData['Address']

    # Public method to retrieve the CPMStatus key value from __aimData as long as isAIMError() returns false. The
    # CPMStatus key value returns success if no CPM tasks had had no errors. The isAIMError() public
    # method returns true only if the 'ErrorCode' key exists in __aimData and it  will only be retrieved IF
    # AIMWebService returns a status code 400, 403, or 404.
    def getCPMStatus(self):
        if self.isAIMError():
            return self.getAIMError()
        elif "CPMStatus" in self.__aimData.keys() and self.__aimData['CPMStatus'] == "success":
            self.__cpmStatus = "success"
            return self.__cpmStatus
        elif "CPMStatus" in self.__aimData.keys() and self.__aimData['CPMStatus'] != "success":
            self.__cpmStatus = self.__aimData['CPMStatus']
            return self.__cpmStatus
        else:
            pass

    # Public method to retrieve the CPMDisabled key value from __aimData as long as isAIMError() returns false. The
    # CPMDisabled key value returns the reason given to disable the account automatic management if any was given.
    # The isAIMError() public method returns true only if the 'ErrorCode' key exists in __aimData and it  will only
    # be retrieved IF AIMWebService returns a status code 400, 403, or 404.
    def getCPMDisabled(self):
        if self.isAIMError():
            return self.getAIMError()
        elif "CPMDisabled" in self.__aimData.keys():
            self.__cpmDisableReason = self.__aimData['CPMDisabled']  # The CPMDisabled key value is stored in
            # __CPMDisableReason in case it is desired to be used.

            self.__cpmDisable = True
            return self.__cpmDisable
        else:
            self.__cpmDisable = False
            return self.__cpmDisable

    def getCPMDisabledReason(self):  # Returns the CPMDisabled key value stored in __cpmDisableReason.
        return self.__cpmDisableReason

    # Public method to retrieve the LastSuccessChange key value from __aimData as long as isAIMError() returns false.
    # The LastSuccessChange key value returns the integer value as a string of the last successful password change
    # done by the CPM. The isAIMError() public method returns true only if the 'ErrorCode' key exists in __aimData
    # and it  will only be retrieved IF AIMWebService returns a status code 400, 403, or 404.
    def getLastSuccessChange(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.__aimData['LastSuccessChange']))  # The
            # LastSuccessChange integer timestamp is transformed into datetime format to perform date manipulations
            # such as "predicting" the next password change to be performed by the CPM per typical configuration.

    # Public method to calculate from getLastSuccessChange() the next possible password change to be performed by the
    # CPM per the typical configuration by using the datetime.timedelta(...) method as long as isAIMError() returns
    # false.
    def getNextChange(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessChange() + datetime.timedelta(days=30)

    # Public method used to convert the datetime value returned by getLastSuccessChange() into the ISO timestamp
    # format as long as isAIMError() returns false.
    def getLastSuccessChangeTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessChange().isoformat()

    # Public method to retrieve the LastSuccessReconciliation key value from __aimData as long as isAIMError()
    # returns false. The LastSuccessReconciliation key value returns the integer value as a string of the last
    # successful password reconcile done by the CPM. The isAIMError() public method returns true only if the 'ErrorCode'
    # key exists in __aimData and it  will only be retrieved IF AIMWebService returns a status code 400, 403, or 404.
    def getLastSuccessReconciliation(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.__aimData['LastSuccessReconciliation']))

    # Public method used to convert the datetime value returned by getLastSuccessReconciliation() into the ISO
    # timestamp format as long as isAIMError() returns false.
    def getLastSuccessReconciliationTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessReconciliation().isoformat()

    # Public method to retrieve the LastSuccessVerification key value from __aimData as long as isAIMError()
    # returns false. The LastSuccessVerification key value returns the integer value as a string of the last
    # successful password reconcile done by the CPM. The isAIMError() public method returns true only if the 'ErrorCode'
    # key exists in __aimData and it  will only be retrieved IF AIMWebService returns a status code 400, 403, or 404.
    def getLastSuccessVerification(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return datetime.datetime.fromtimestamp(int(self.__aimData['LastSuccessVerification']))

    # Public method to calculate from getLastSuccessVerification() the next possible password verification to be
    # performed by the CPM per the typical configuration by using the datetime.timedelta(...) method as long as
    # isAIMError() returns false.
    def getNextVerification(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessVerification() + datetime.timedelta(days=7)

    # Public method used to convert the datetime value returned by getLastSuccessVerification() into the ISO
    # timestamp format as long as isAIMError() returns false.
    def getLastSuccessVerificationTS(self):
        if self.isAIMError():
            return self.getAIMError()
        else:
            return self.getLastSuccessVerification().isoformat()

    # Public method to retrieve the LastTask key value from __aimData as long as isAIMError() returns false. The
    # LastTask key value returns the string value of the last task performed by the CPM. The isAIMError() public
    # method returns true only if the 'ErrorCode' key exists in __aimData and it  will only be retrieved IF
    # AIMWebService returns a status code 400, 403, or 404.
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

    # The isAIMError() public method returns true only if the 'ErrorCode' key exists in __aimData. This key will only be
    # retrieved IF AIMWebService returns a status code 400, 403, or 404.
    def isAIMError(self):
        if "ErrorCode" in self.__aimData.keys():
            return True
        else:
            return False

    # The getAIMError() public method is similar to isAIMError(), but instead returns the value of the 'ErrorCode'
    # key as an exception if it exists in __aimData. This key will only be found IF AIMWebService returns a status
    # code 400, 403, or 404.
    def getAIMError(self):
        if "ErrorCode" in self.__aimData.keys():
            raise Exception("ErrorCode: " + self.__aimData['ErrorCode'] + "-" + self.__aimData['ErrorMsg'])
        else:
            pass
