from impacket.examples import logger
from impacket import version
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_PKT_PRIVACY, RPC_C_AUTHN_LEVEL_PKT_INTEGRITY


deep = False

def query(args):
    global deep
    target = args.target if args.target else 'localhost'
    command = args.command
    if args.dir:
        dir = args.dir
    if args.file:
        file = args.file
    username = args.username[0] if args.username else ''
    password = args.password[0] if args.password else ''
    domain = args.domain
    deep = args.deep
    namespace = args.namespace
    print(username, password)
    connection = setup_connection(target, domain, username, password, namespace)

def setup_connection(host, domain, username, password, namespace):
    dcom = DCOMConnection(host, username, password, domain, '', '', None, oxidResolver=True)
    iInterface = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login,wmi.IID_IWbemLevel1Login)
    iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
    iWbemServices= iWbemLevel1Login.NTLMLogin(namespace, NULL, NULL)

    return iWbemServices


def execute_query(conn, command, dir=None, filenames=None):
     for command in commands:
        if command == 'basicinfo':
            print("\n***Basic Info***")
            for info in conn.query():
                print(info)
            for info in conn.query("SELECT * FROM Win32_OperatingSystem"):
                print(info)
        if command == 'procs':
            print("\n***Running Processes***")
            for process in conn.query("SELECT * FROM Win32_Process"):
                if deep:
                    print(process)
                else:
                    print(process.caption)
        if command == 'services':
            print("***Services****")
            for info in conn.query("SELECT * FROM Win32_Service"):
                if deep:
                    print(info)
                else:
                    print(f'\nService: {info.name}')
                    print(f'State: {info.state}')
                    print(f'Start Mode: {info.startmode}')
                    print(f'Path: {info.pathname}')
