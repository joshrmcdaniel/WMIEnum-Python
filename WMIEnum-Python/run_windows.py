import wmi


deep = False
target = None
username = ''
password = ''

def main(args):
    global deep
    global conn
    global target
    global username
    global password
    target = args.target if args.target else '127.0.0.1'
    commands = args.command
    if args.dir:
        dir = args.dir
    if args.file:
        file = args.file
    username = args.username
    password = args.password
    deep = args.deep
    run_query(commands)

def connect(host, user, password, namespace='root\cimv2'):
    if user:
        return wmi.WMI(host, user, password, namespace=namespace)
    else:
        return wmi.WMI(host, namespace=namespace)

def list_basic_info():
    print("\n***Basic Info***")
    conn = connect(target, username, password)
    for info in conn.query("SELECT * FROM Win32_ComputerSystem"):
        if deep:
            print(info)
        else:
            print(f'Name:    {info.name}')
            print(f'Domain:  {info.domain}')
    for info in conn.query("SELECT * FROM Win32_OperatingSystem"):
        if deep:
            print(info)
        else:
            print(f'Version: {info.version}')

 
def list_processes():
    print("\n***Running Processes***")
    conn = connect(target, username, password)
    for process in conn.query("SELECT * FROM Win32_Process"):
        if deep:
            print(process)
        else:
            print(process.caption)


def list_services():
    print("***Services****")
    conn = connect(target, username, password)
    for info in conn.query("SELECT * FROM Win32_Service"):
        if deep:
            print(info)
        else:
            print(f'\nService:  {info.name}')
            print(f'State:      {info.state}')
            print(f'Start Mode: {info.startmode}')
            print(f'Path:       {info.pathname}')



def list_drives():
    print('***Drives***')
    conn = connect(target, username, password)
    for info in conn.query("SELECT * FROM Win32_LogicalDisk"):
        if deep:
            print(info)
        else:
            print(f'Device ID: {info.deviceid}')
            print(f'Volume Name: {info.volumename}')


def list_nics():
    print("***Network Information***")
    conn = connect(target, username, password)
    for info in conn.query("SELECT * FROM Win32_NetworkAdapterConfiguration"):
        if deep:
            print(info)
        elif info.ipaddress or info.defaultipgateway:
            print(f'IP Address: {info.ipaddress[0]}')
            if info.defaultipgateway:
                print(f'Gateway:    {info.defaultipgateway[0]}')


def list_av():
    av_enabled = {
        0x11: 'Enabled',
        0x10: 'Enabled',
        0x01: 'Disabled',
        0x00: 'Disabled'
        }
    print("***Antivirus Info***")
    conn = connect(target, username, password, namespace=r'root\SecurityCenter')
    query_result = conn.query("SELECT * FROM AntiVirusProduct")
    if query_result == []:
        conn = connect(target, username, password, namespace=r'root\SecurityCenter2')
        query_result = conn.query("SELECT * FROM AntiVirusProduct")
    for info in query_result:
        if deep:
            print(info)
        else:
            state = int(hex(info.productstate),16)
            print(f'{info.displayname}: {state}')

            
def list_files():
    pass


def run_query(commands):
    for command in commands:
        if command == 'basicinfo':
            list_basic_info()
        if command == 'procs':
            list_processes()
        if command == 'services':
            list_services()
        if command == 'drives':
            list_drives()
        if command == 'nics':
            list_nics()
        if command == 'av':
            list_av()
        if command == 'dir':
            pass
        if command == 'cat':
            pass
        if command == 'find':
            pass

