#!/usr/bin/env python
import subprocess
import socket
import json
import os
import threading

ADDR = '0.0.0.0'
PORT = 5000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ADDR, PORT))
s.listen(10)


# Read config
config = {}
for c in open('/etc/deploytoy.conf', 'r').readlines():
    key, value = c.replace('\n','').split(' ')
    config[key] = value

def pull_repo(repo_path):
    os.chdir(repo_path)
    subprocess.call(['git','pull'])
    subprocess.call(['sh','deploy.sh'])

print config
while True:
    conn, addr = s.accept()
    try:
        data = json.loads(conn.recv(20000))
        if data['repository']['full_name'] == config['repo_full_name']:
            thread = threading.Thread(target = pull_repo, args=(config['repo_root'], ) )
            thread.run()
    except Exception as e: # Die gracefully
        print "failed :(", e




# deploytoy_socket.py:

#     read /etc/deploytoy.conf
#     setup socket to 0.0.0.0:5000

#     on ping
#         check repo name against conf
#         check payload origin is github

#         cd into
#         pull repo

#         run deploy.sh