#!/bin/bash

/usr/sbin/sshd -D &
mongod --bind_ip_all --fork --logpath /var/log/mongodb/mongod.log
sleep 5
nohup ./start_webui.sh > webui.log &
nohup /usr/bin/open5gs-mmed -c /etc/open5gs/mme.yaml > mmed.log &
nohup /usr/bin/open5gs-sgwcd -c /etc/open5gs/sgwc.yaml > sgwc.log &
nohup /usr/bin/open5gs-smfd -c /etc/open5gs/smf.yaml > smfd.log &
nohup /usr/bin/open5gs-amfd -c /etc/open5gs/amf.yaml > amfd.log &
nohup /usr/bin/open5gs-sgwud -c /etc/open5gs/sgwu.yaml > sgwud.log &
nohup /usr/bin/open5gs-upfd -c /etc/open5gs/upf.yaml > upfd.log &
nohup /usr/bin/open5gs-hssd -c /etc/open5gs/hss.yaml > hssd.log &
nohup /usr/bin/open5gs-pcrfd -c /etc/open5gs/pcrf.yaml > pcrfd.log &
nohup /usr/bin/open5gs-nrfd -c /etc/open5gs/nrf.yaml > nrfd.log &
nohup /usr/bin/open5gs-scpd -c /etc/open5gs/scp.yaml > scpd.log &
nohup /usr/bin/open5gs-seppd -c /etc/open5gs/sepp1.yaml > seppd.log &
nohup /usr/bin/open5gs-ausfd -c /etc/open5gs/ausf.yaml > ausfd.log &
nohup /usr/bin/open5gs-udmd -c /etc/open5gs/udm.yaml > udmd.log &
nohup /usr/bin/open5gs-pcfd -c /etc/open5gs/pcf.yaml > pcfd.log &
nohup /usr/bin/open5gs-nssfd -c /etc/open5gs/nssf.yaml > nssfd.log &
nohup /usr/bin/open5gs-bsfd -c /etc/open5gs/bsf.yaml > bsfd.log &
nohup /usr/bin/open5gs-udrd -c /etc/open5gs/udr.yaml > udrd.log &
tail -f /dev/null