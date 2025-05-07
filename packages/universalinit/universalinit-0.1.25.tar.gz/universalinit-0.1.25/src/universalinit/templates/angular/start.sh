#!/bin/bash

PORT=3000

while lsof -iTCP:$PORT -sTCP:LISTEN -n -P >/dev/null
do
  echo "Port $PORT is in use. Trying $((PORT+1))..."
  PORT=$((PORT+1))
done

echo "Found free port: http://localhost:$PORT"

npm start -- --port $PORT
