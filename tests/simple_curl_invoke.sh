#!/usr/bin/bash

set -e

curl -X POST https://dungeondivinelabs.com/items -H "Content-Type: application/json" -d '{"item_id": 15, "item": "item15" }'
curl -X PUT https://dungeondivinelabs.com/items/22
curl -X DELETE https://dungeondivinelabs.com/items/22
curl -X GET https://dungeondivinelabs.com/items/22
curl -X GET https://dungeondivinelabs.com/items
