# CyberArkAPI Project
Building AIMWebService API Call "Framework"

 Class created as "framework" to perform CyberArk AIMWebService API Calls. This framework allows the creating
 multiple objects, which in turn allows retrieving multiple accounts.

 Developed by Jorge Berrios
 \n\tContact information: <berriosj@autonation.com>, <jxberrios@gmail.com>

 Usage:
   1. Create instance: CyberarkAIM() - It can received values for AppID, Safe, Object and CyberArk DNS Name as
       arguments.
   2. Set AppID values: assign the string value to the public attribute appID from the newly created
       CyberAIM Object.
   3. Set Safe values: assign the string value to the public attribute safe from the newly created
       CyberAIM Object.
   4. Set Object values: assign the string value to the public attribute actName from the newly created
       CyberAIM Object.
   5. Set CyberArk DNS name: assign the string value to the public method setHost from the newly created
       CyberAIM Object.

 Retrieving Values through get methods:
   1. getHost: Returns the host or DNS name of CyberArk IF set.
   2. getaimURL: Returns the composed CyberArk AIMWebService URL
   3. getaimData: calls the private method responsible for the API call, and returns the value from the local attribute
   4. getUsername: returns the json key value of UserName
   5. getPassword: returns the json key value of Content
   6. getAddress: returns the json key value of Address
   7. getCPMStatus: returns the json key value of CPMStatus
   8. getCPMDisabled: returns a boolean to say if the account management is disabled.
   9. getCPMDisabledReason: returns the json key value of CPMDisabled IF it exists
  10. getLastSuccessChange: returns the datetime format of json key value of LastSuccessChange
  11. getNextChange: returns the next possible password change based on the typical 30 day policy.
  12. getLastSuccessChangeTS: returns the timestamp ISO format of json key value of LastSuccessChange
  13. getLastSuccessReconciliation: returns the datetime format of json key value of LastSuccessReconciliation
  14. getLastSuccessReconciliationTS: returns the timestamp ISO format of json key value of LastSuccessReconciliation
  15. getLastSuccessVerification: returns the datetime format of json key value of LastSuccessVerification
  16. getNextVerification: returns the next possible password verification based on the typical 7 day policy.
  17. getLastSuccessVerificationTS: returns the timestamp ISO format of json key value of LastSuccessVerificationTS
  18. getLastTask: returns the json key value of LastTask
  19. getPasswordChangeInProcess: returns the json key value of PasswordChangeInProcess
  20. isAIMError: returns a boolean if the json key ErrorCode exists from an AIMWebService error.
  21. getAIMError: IF the json key ErrorCode exists, it will print a custom error from the json key value ErrorMsg
       and exit the program. Similar to raising a custom exception.
