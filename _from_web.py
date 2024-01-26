import sys
import os
import requests
from bs4 import BeautifulSoup
import re
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.geteuid() == 0
    except:
        return False

def get_ip_address(url, name):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', {'id': 'tabpanel-dns-a'})
        if div:
            pattern = re.compile(r'https://www.ipaddress.com/ipv4/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            link = div.find('a', href=pattern)
            if link:
                ip_address = pattern.match(link['href']).group(1)
                return ip_address + ' ' + name + '\n'
    except Exception as e:
        print(f"Error occurred while getting IP address: {e}")
    return ''

def clean_hosts(hosts_path):
    try:
        with open(hosts_path,'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            preserved_lines = [line for line in lines if not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+(github.com|github.global.ssl.fastly.net|assets-cdn.github.com)', line) and line != '\n']
            f.writelines(preserved_lines)
    except Exception as e:
        print(f"Error occurred while cleaning hosts: {e}")

def prepend_to_hosts(content, hosts_path):
    try:
        clean_hosts(hosts_path)
        with open(hosts_path, 'r+') as f:
            original_content = f.read()
            f.seek(0)
            f.write(content + original_content)
            print('---------------------Done!--------------------')
            print('Your hosts file has been updated as below:')
            print(content + original_content)
            print('Your hosts file is located at: ' + hosts_path + '.  You can restore it manually if you want to')
    except Exception as e:
        print(f"Error occurred while updating hosts: {e}")

if not is_admin():
    print("please use 'administrator privileges' or 'sudo' to run this script")
    sys.exit(1)

while True:
    choice = input("Please choose to clean previous hosts file settings or update hosts file (C/U): ")
    if choice not in ['C', 'U']:
        print('Invalid input, please try again')
        continue
    hosts_path = '/etc/hosts' if sys.platform.startswith('linux') or sys.platform.startswith('darwin') else 'C:\\Windows\\System32\\drivers\\etc\\hosts'
    if choice == 'C':
        clean_hosts(hosts_path)
        if sys.platform.startswith('win'):
            os.system('ipconfig /flushdns')
        print('---------------------Done!--------------------')
        print('Your hosts file has been cleaned up successfully')
        input("Press Enter to exit...")
        sys.exit(0)
    elif choice == 'U':
        ip_addresses = ''
        ip_addresses += get_ip_address('https://sites.ipaddress.com/github.com', 'github.com')
        ip_addresses += get_ip_address('https://sites.ipaddress.com/github.global.ssl.fastly.net', 'github.global.ssl.fastly.net')
        if sys.platform.startswith('win'):
            ip_addresses += get_ip_address('https://sites.ipaddress.com/assets-cdn.github.com', 'assets-cdn.github.com')
        prepend_to_hosts(ip_addresses, hosts_path)
        if sys.platform.startswith('win'):
            os.system('ipconfig /flushdns')
        input("Press Enter to exit...")
        break
