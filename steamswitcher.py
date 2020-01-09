import sys
import os
import shutil
from modules.update import start_checkupdate
from modules.ui import MainApp
from modules.reg import fetch_reg
from modules.account import acc_getlist

print('App Start')

BRANCH = 'master'
__VERSION__ = '1.9'
URL = ('https://raw.githubusercontent.com/sw2719/steam-account-switcher/%s/version.yml' % BRANCH)


if getattr(sys, 'frozen', False):
    print('Running in a bundle')
    BUNDLE = True
    if os.path.isdir('updater'):
        try:
            shutil.rmtree('updater')
        except OSError:
            pass
else:
    print('Running in a Python interpreter')
    BUNDLE = False

print('Running on', os.getcwd())


def afterupdate():
    if os.path.isfile('update.zip'):
        try:
            os.remove('update.zip')
        except OSError:
            pass


print('Fetching registry values...')

if fetch_reg('autologin') != 2:
    print('Autologin value is ' + str(fetch_reg('autologin')))
else:
    print('ERROR: Could not fetch autologin status!')
if fetch_reg('autologin'):
    print('Current autologin user is ' + str(fetch_reg('username')))
else:
    print('ERROR: Could not fetch current autologin user!')


print('Init complete. Main app starting.')
root = MainApp(__VERSION__, URL, BUNDLE)
root.draw_button()
root.after(100, lambda: start_checkupdate(root, __VERSION__, URL, BUNDLE))

if os.path.isfile(os.path.join(os.getcwd(), 'update.zip')):
    root.after(150, afterupdate)
if not acc_getlist():
    root.after(200, root.importwindow)

root.mainloop()
