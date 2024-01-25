import sys
import os
import requests
from bs4 import BeautifulSoup
import re

def check_platform():
    if os.geteuid() != 0:
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            print('Please run with sudo')
            sys.exit(1)
        elif sys.platform.startswith('win'):
            print('Please run with administrator')
            sys.exit(1)
        else:
            print('Cannot detect your platform')
            sys.exit(1)

def get_ip_address(url, name):
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
        for line in lines:
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} github.com', line):
                continue
            elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} github.global.ssl.fastly.net', line):
                continue
            elif line == '\n':
                continue
            else:
                f.write(line)

def prepend_to_hosts(content, hosts_path):
    clean_hosts(hosts_path)
    with open(hosts_path, 'r+') as f:
        original_content = f.read()
        f.seek(0)
        f.write(content + original_content)
        print('Done')

check_platform()

ip_addresses = ''
ip_addresses += get_ip_address('https://sites.ipaddress.com/github.com', 'github.com')
ip_addresses += get_ip_address('https://sites.ipaddress.com/github.global.ssl.fastly.net', 'github.global.ssl.fastly.net')

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    prepend_to_hosts(ip_addresses, '/etc/hosts')
elif sys.platform.startswith('win'):
    prepend_to_hosts(ip_addresses, 'C:\\Windows\\System32\\drivers\\etc\\hosts')
    os.system('ipconfig /flushdns')
