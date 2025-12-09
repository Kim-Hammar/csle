#!/bin/bash

echo "Initializing Open5GS WebUI Database..."
mongosh open5gs /usr/lib/node_modules/open5gs/mongo-init.js

echo "Starting Open5GS WebUI..."
cd /usr/lib/node_modules/open5gs
export NODE_ENV=production

exec /usr/bin/node server/index.js