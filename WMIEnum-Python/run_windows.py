import wmi


deep = False


def main(args):
    global deep
    target = args.target if args.target else '127.0.0.1'
    ssl = args.ssl
    proto = args.proto
    command = args.command
    if args.dir:
        dir = args.dir
    if args.file:
        file = args.file
    username = args.username
    password = args.password
    deep = args.deep
    wmi_connection = connect(target, username, password)
    run_query(wmi_connection, command)

def connect(host, user, password):
    if user:
        return wmi.WMI(host, user, password)
    else:
        return wmi.WMI(host)


def run_query(conn, commands):
    for command in commands:
        if command == 'basicinfo':
            print("\n***Basic Info***")
            for info in conn.query("SELECT * FROM Win32_ComputerSystem"):
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

