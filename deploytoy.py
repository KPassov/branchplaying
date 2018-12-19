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

def pull_repo(repo_path):
    os.chdir(repo_path)
    subprocess.call(['git','pull'])
    subprocess.call(['sh','deploy.sh'])

config = {}

while True:
    conn, addr = s.accept()

    for c in open('/etc/deploytoy.conf', 'r').readlines():
        key, value = c.replace('\n','').split(' ')
        config[key] = value

    try:
        data = json.loads(conn.recv(20000))
        if data['repository']['full_name'] == config['repo_full_name']:
            thread = threading.Thread(target = pull_repo, args=(config['repo_root'] + config['repo_full_name'].split('/')[-1], ) )
            thread.run()
    except Exception as e: # Die gracefully
        print "failed :(", e
