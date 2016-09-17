#!/bin/bash

BASE_URL="http://localhost:9000"
AUTH_SUFFIX="/user/auth"

[ "${BASH_SOURCE[0]}" = "${0}" ] && echo "This script must be sourced" && exit 1

read -p "Username: " USERNAME
read -s -p "Password: " PASSWORD
echo

read -d '' AUTH_REQUEST <<EOF
{
    "username": "$USERNAME",
    "password": "$PASSWORD"
}
EOF

TOKEN=$(curl -vvv "${BASE_URL}${AUTH_SUFFIX}" \
    -X POST --header 'content-type: application/json' \
    --data "$AUTH_REQUEST" 2> /dev/null \
    | jq -r '.token' 2> /dev/null )

echo "The token: $TOKEN"
export STRICOD_TOKEN=\"$TOKEN\"

