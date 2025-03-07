#!/bin/bash
# wait-for-it.sh

#!/bin/bash
# Wait for db to be available

until curl --silent db:3306; do
  echo "Waiting for db:3306..."
  sleep 2
done

echo "db:3306 is available. Starting the server..."
exec "$@"
