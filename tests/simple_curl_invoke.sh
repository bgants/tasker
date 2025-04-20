#!/usr/bin/bash

set -e

echo "POST test ..."
curl -X POST https://dungeondivinelabs.com/task -H "Content-Type: application/json" -d '{"id": 15, "task": "Do something" }'
sleep 3
echo "\n"
echo "PUT test ..."

curl -X PUT https://dungeondivinelabs.com/task/22
sleep 3
echo "\n"
echo "GET test ..."

curl -X GET https://dungeondivinelabs.com/task/22
sleep 3
echo "\n"
echo "GET test ..."

curl -X GET https://dungeondivinelabs.com/tasks
sleep 3
echo "\n"
echo "DELETE test ..."

curl -X DELETE https://dungeondivinelabs.com/task/22
sleep 3
echo "\n"
