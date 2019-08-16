import sys, getopt

from cyberarkAPI import cyberarkAPI

# def call(cyberarkAPI):


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hf:nHaso:", ["num=", "Host=", "APPID=", "Safe=", "Obj=", "folder=", "help"])
        account1 = cyberarkAPI()
    except getopt.GetoptError:
        # print("Usage: cyberarkCall.py -n <account_numbers> -H <CyberArk_Host> -a <APPID> -s <safe_name> -o "
            # "<object_name> -f <folder (optional)")
        print("Usage: cyberarkCall.py -H <CyberArk_Host> -a <APPID> -s <safe_name> -o <object_name> -f <folder (optional)")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "help", "--help"):
            # print("Usage: cyberarkCall.py -n <account_numbers> -H <CyberArk_Host> -a <APPID> -s <safe_name> -o "
            # "<object_name> -f <folder (optional)")
            print("Usage: cyberarkCall.py -H <CyberArk_Host> -a <APPID> -s <safe_name> -o <object_name> -f <folder (optional)")
            sys.exit()
#        elif opt in ("-n", "--num"):
#            inputfile = arg
        elif opt in ("-H", "--Host"):
            account1.setHost(arg)
        elif opt in ("-a", "--APPID"):
            account1.setappID(arg)
        elif opt in ("-s", "--Safe"):
            account1.setSafe(arg)
        elif opt in ("-o", "--Obj"):
            account1.setActName(arg)
        elif opt in ("-o", "--folder"):
            account1.setFolder(arg)

    print(account1.host, account1.aimURL, account1.appID, account1.safe, account1.actName)
    # print(account1.host, account1.aimURL)
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

