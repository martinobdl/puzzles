#!/usr/bin/bash

ENC_FLAG="U2FsdGVkX1/andRK+WVfKqJILMVdx/69xjAzW4KUqsjr98GqzFR793lfNHrw1Blc8UZHWOBrRhtLx3SM38R1MpRegLTHgHzf0EAa3oUeWcQ="

cat all_keys.txt | while read line; do
    
    echo $line > /tmp/plain.key; xxd -r -p /tmp/plain.key > /tmp/enc.key

    echo $ENC_FLAG | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key 2> /dev/null | grep "CTF{"

done
