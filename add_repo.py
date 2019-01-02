#!/usr/bin/env python

import os
from subprocess import call


if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

def query(message):
    a = raw_input(message)
    return a


repo_full_name = ""
repo_root = ""
# Get input for config
while not repo_full_name:
    repo_full_name = query("Full repository name (i.e 'KPassov/deploytoy'):")

while not repo_root:
    repo_root = query("Full path to where I should place the repo? (i.e '/home/ec2-user/')")


# Create and Set Deploy key
if query('Setup deploykey? (y/n)') == 'y':

    print "\n"
    print "Setting up Deployment Key"

    found_key = Popen(['cat ~/.ssh/*.pub'], shell=True, stdout=PIPE).communicate()[0]

    if isinstance(rsa_key, str) and len(rsa_key) > 10:
        print "    found public rsa key \n", rsa_key

    elif query("Could not find key Read rsa key from path? (y/n)") == 'y':
        found_key = call('cat ' + query('rsa public key full path?'))
        print "    found public rsa key \n", found_key

    elif query("Create new key? (y/n)") == 'y':
        call(['ssh-keygen'])
        found_key = call('cat %s' % query('rsa public key full path?'))
        print found_key

    print "Create a deploykey using the key above, at https://github.com/%s/settings/keys/new" % repo_full_name


os.chdir(repo_root)


# Clone Repo
while (not os.path.isdir(repo_root + repo_full_name.split('/')[-1])) and query('Press any key when deploykey is setup and i\'ll try to clone ("n" to cancel)') != 'n':
    call(['git','clone','git@github.com:%s.git'%repo_full_name])


# Update config file
with open('/etc/deploytoy.conf', 'w') as conf_file:
    conf_file.writelines(['repo_full_name %s\nrepo_root %s'%(repo_full_name,repo_root)])

# Create Webhook
print "Create a Webhook with the Json Content type listening for push events, at https://github.com/%s/settings/hooks/new" % repo_full_name
print "For the Payload URL, 'http://<SERVER_IP>:5000'. The deploytoy.py is listening on port 5000, so make sure the server has that port open."