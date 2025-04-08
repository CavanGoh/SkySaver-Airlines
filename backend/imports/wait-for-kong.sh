#!/bin/sh
# Wait until Kong Admin API is ready
until curl -s http://kong:8001/routes | grep -q "data"; do
  echo "Waiting for Kong to be fully ready..."
  sleep 2
done

# Proceed with deck sync
/usr/local/bin/deck gateway sync /config/kong.yaml --kong-addr http://kong:8001
