#!/bin/sh

# Wait until Kong returns a successful response for a core endpoint
until curl -s http://kong:8001/routes | grep -q "data"; do
  echo "Still waiting for Kong to fully boot..."
  sleep 2
done

echo "Kong is up, syncing config..."
/usr/local/bin/deck gateway sync /config/kong.yaml --kong-addr http://kong:8001
