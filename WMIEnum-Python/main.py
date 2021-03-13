import argparse


def main():
    args = args()


def args():
    parser = argparse.ArgumentParser(description='Enumerate Windows Server using WMIEnum')
    
    parser.add_argument('-u', '--user', required=False, type=str, nargs=1, help='Username to login as. Leave blank for local enum.')
    parser.add_argument('-p', '--pass', required=False, type=str, nargs=1, help='Password to login with. Leave blank for local enum.')
    parser.add_argument('-t', '--target', required=False, default=None, nargs=1, help='Target to run command on. Leave blank for local enum.')
    parser.add_argument('--ssl', reqiured=False, default=True, action='store_false', help='Encrypt the traffic. Only applicable if using WinRM. Default is enable SSL.')
    parser.add_argument('--proto', required=False, default='winrm', type=str, nargs=1, help='Protocol to use (WinRM or DCOM). Default is WinRM.')
    parser.add_argument('--dir', required=False, default=None, type=str, nargs='+', help='Directory(s) for dir command.')
    parser.add_argument('--file', required=False, default=None, type=str, nargs='+', help='Filename(s) for cat and file clist.')
    parser.add_argument('command', required=True, type=str, nargs=1,
                        choices=['basicinfo', 'procs', 'services', 'drives', 'nics', 'av', 'dir', 'cat', 'find'],
                        help='basicinfo: Hostname and domain\n' +
                        'procs: Running processes.\n' +
                        'services: All services, state, start mode, and service path.\n' +
                        'drives: Local and remote system drives.\n' +
                        'nics: Active NICs, IP address, and gateway.\n' +
                        'av: AV products that write to root\\SecurityCenter2, whether they are enabled, and if they are updated.\n' +
                        'dir: Directory contents.\n' +
                        'cat: File contents.\n' +
                        'find: Location of file on disk.\n')


    return parser.parse_args()

if __name__ == '__main__':
    main()