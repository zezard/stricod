#!/bin/bash

BASE_URL="http://localhost:9000"
API_SUFFIX="/user/geodata"

prompt_and_exit()
{
    echo $1 >&2
    exit 1
}
[ $STRICOD_TOKEN ] || prompt_and_exit "No active user session"

curl -vvv "${BASE_URL}${API_SUFFIX}" \
    --header 'userToken: $STRICOD_TOKEN' \
    || prompt_and_exit "Failed to fetch data"

