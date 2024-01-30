import itertools
import threading
import sys
import os
import requests
import re
from bs4 import BeautifulSoup
import time

done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rUpdating hosts file ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
t = threading.Thread(target=animate)

def is_admin():
    if os.name == 'nt':
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return os.geteuid() == 0

def get_ip_address(name):
    url = 'https://sites.ipaddress.com/' + name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    pattern = re.compile(r'https://www.ipaddress.com/ipv4/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    for link in links:
        href = link.get('href')
        if href and pattern.match(href):
            ip_address = pattern.match(href).group(1)
            return ip_address + ' ' + name + '\n'
    return ''

def clean_hosts(hosts_path):
    with open(hosts_path,'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        preserved_lines = [line for line in lines if not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+(github.com|github.global.ssl.fastly.net|assets-cdn.github.com)', line) and line != '\n']
        f.writelines(preserved_lines)

def prepend_to_hosts(content, hosts_path):
    clean_hosts(hosts_path)
    with open(hosts_path, 'r+') as f:
        original_content = f.read()
        f.seek(0)
        f.write(content + original_content)
        print('\n---------------------Done!--------------------')
        print('Your hosts file has been updated as below:\n')
        print(content + original_content)
        print('Your hosts file is located at: ' + hosts_path + '.  You can restore it manually if you want to.')

if not is_admin():
    print("please use 'administrator privileges' or 'sudo' to run this script")
    input("Press Enter to exit...")
    sys.exit(0)
hosts_path = '/etc/hosts' if sys.platform.startswith('linux') or sys.platform.startswith('darwin') else 'C:\\Windows\\System32\\drivers\\etc\\hosts'
t.start()
ip_addresses = ''
ip_addresses += get_ip_address('github.com')
ip_addresses += get_ip_address('github.global.ssl.fastly.net')
if sys.platform.startswith('win'):
    ip_addresses += get_ip_address('assets-cdn.github.com')
prepend_to_hosts(ip_addresses, hosts_path)
if sys.platform.startswith('win'):
    os.system('ipconfig /flushdns')
done = True
input("Press Enter to exit...")
sys.exit(0)
