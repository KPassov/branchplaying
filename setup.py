#!/usr/bin/env python

from shutil import copyfile
import os
from subprocess import Popen, PIPE


if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")


# Create deploytoy.py
toy_path = raw_input('full path to deploytoy.py? (default is "/home/ec2-user/deploytoy.py")')
toy_path = toy_path if toy_path else '/home/ec2-user/deploytoy.py'

copyfile('deploytoy.py', toy_path)


# Add websocket file to reboot
crontab_line = '@reboot (python %s &)' % toy_path

if crontab_line not in Popen(["crontab -l"], shell=True, stdout=PIPE).communicate()[0]:

    os.system("crontab -l > /tmp/cronaddition.txt")

    os.system("echo '%s' >> /tmp/cronaddition.txt"%crontab_line)

    os.system("crontab < /tmp/cronaddition.txt")

    os.system("rm /tmp/cronaddition.txt")
    print "Added reboot to crontab"

else:
    print "crontab already exists"


# Create config file
if not os.path.isfile('/etc/deploytoy.conf'):
    open('/etc/deploytoy.conf', 'w+')
    print "created: /etc/deploytoy.conf"

print "python " + toy_path + ' > /dev/null 2> /dev/null &'

process = Popen("sudo python " + toy_path + ' > /dev/null 2> /dev/null &', shell=False)

print "Deploytoy installed and running with pid %s! use the add_repo.py to add additional repos" % process.pid+1#pid hack

# Start websocket
