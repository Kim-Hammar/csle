#!/bin/bash

/usr/sbin/sshd -D &
mongod --bind_ip_all --fork --logpath /var/log/mongodb/mongod.log
sleep 5
nohup ./start_webui.sh > webui.log &
tail -f /dev/null