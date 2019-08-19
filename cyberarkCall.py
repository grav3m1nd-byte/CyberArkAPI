import getopt
import sys

from cyberarkAPI import CyberarkAPI


# def call(cyberarkAPI):


def main(argv):
    # host = appid = safe = obj = folder = ""
    account1 = CyberarkAPI()

    try:
        # opts, args = getopt.getopt(argv, "hf:nHaso:", ["num=", "Host=", "APPID=", "Safe=", "Obj=", "folder=", "help"])
        opts, args = getopt.getopt(sys.argv[1:], "H:a:s:o:f:h", ["Host=", "APPID=", "Safe=", "Obj=", "folder=", "help"])

    except getopt.GetoptError:
        # print("Usage: cyberarkCall.py -n <account_numbers> -H <CyberArk_Host> -a <APPID> -s <safe_name> -o "
        # "<object_name> -f <folder (optional)")
        print("Usage: cyberarkCall.py -H <CyberArk_Host> -a <APPID> -s <safe_name> -o <object_name> -f <folder> (opt)")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "help", "--help"):
            # print("Usage: cyberarkCall.py -n <account_numbers> -H <CyberArk_Host> -a <APPID> -s <safe_name> -o "
            # "<object_name> -f <folder (optional)")
            print(
                "Usage: cyberarkCall.py -H <CyberArk_Host> -a <APPID> -s <safe_name> -o <object_name> -f <folder> (opt)")
            sys.exit()
            # elif opt in ("-n", "--num"):
            # inputfile = arg
        elif opt in ("-H", "--Host"):
            account1.setHost(arg)
        elif opt in ("-a", "--APPID"):
            account1.appID = arg
        elif opt in ("-s", "--Safe"):
            account1.safe = arg
        elif opt in ("-o", "--Obj"):
            account1.actName = arg
        elif opt in ("-o", "--folder"):
            account1.folder = arg
    #
    #     account1 = cyberarkAPI(appid, safe, obj, host)

    # account1.setappID("test_AIM")
    # account1.setSafe("Priv_BerriosJN")
    # account1.setActName("OS-WinDomain-US1-BerriosJN")
    # account1.setHost("cyberark.autonation.com")
    # account1.host = "cyberark.autonation.com"
    # account1.setaimURL(account1.host)
    # account1.setaimURL(account1.getHost())

    # print(account1.getaimURL())
    print(account1.host, account1.getaimURL(), account1.getquerystring())
    # print(account1.querystring)
    # print(account1.getaimResponse().status_code)
    # account1.getaimData()
    # print(account1.aimData)
    #
    # print(account1.getUsername(),": ", account1.getPassword())
    #
    # print("\nPrevious:", account1.getLastSuccessChangeTS(), "\nNext:", account1.getNextChange().isoformat())


if __name__ == "__main__":
    main(sys.argv[1:])

