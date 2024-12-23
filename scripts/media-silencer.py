
import time
from datetime import datetime
import platform
import sys
import os

class WebsiteBlocker():

    def __init__(self):
        if (platform.system() == 'Windows'):
            self.hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
        else:
            self.hosts_path = '/etc/hosts'
        self.blocked_sites = ['www.youtube.com', 'youtube.com', 'www.facebook.com', 'facebook.com', 'www.twitter.com', 'twitter.com', 'www.instagram.com', 'instagram.com', 'www.tiktok.com', 'tiktok.com']
        self.redirect = '127.0.0.1'

    def check_permissions(self):
        try:
            with open(self.hosts_path, 'a') as _:
                pass
            return True
        except PermissionError:
            return False

    def block_websites(self, start_time, end_time):
        print(f'Website blocker activated. Blocking sites from {start_time} to {end_time}')
        while True:
            current_time = datetime.now().strftime('%H:%M')
            if (start_time <= current_time <= end_time):
                print(f'Blocking period active: {current_time}')
                self.update_hosts_file(True)
            else:
                print(f'Blocking period inactive: {current_time}')
                self.update_hosts_file(False)
            time.sleep(60)

    def update_hosts_file(self, block):
        with open(self.hosts_path, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if (not any(((site in line) for site in self.blocked_sites))):
                    file.write(line)
            if block:
                for website in self.blocked_sites:
                    file.write(f'''{self.redirect} {website}
''')
            file.truncate()

def main() -> None:
    if (not (os.geteuid() == 0)):
        print('This script requires administrator privileges to modify the hosts file.')
        print('Please run the script as administrator/root.')
        sys.exit(1)
    blocker = WebsiteBlocker()
    if (not blocker.check_permissions()):
        print('Error: Cannot access hosts file. Please run with administrator privileges.')
        sys.exit(1)
    try:
        start_time = input('Enter start time (24-hour format, e.g., 09:00): ')
        end_time = input('Enter end time (24-hour format, e.g., 17:00): ')
        datetime.strptime(start_time, '%H:%M')
        datetime.strptime(end_time, '%H:%M')
        blocker.block_websites(start_time, end_time)
    except ValueError:
        print('Invalid time format. Please use HH:MM format (e.g., 09:00)')
        sys.exit(1)
if (__name__ == '__main__'):
    main()
