#!/bin/bash
echo 'check ip is alive begin...'
for i in `seq 1 254`; do
    ping -c 1 -W 1 192.168.1.$i > /dev/null
    if [ $? -eq 0 ]; then
       echo "192.168.1.$i is alive."
    else
       echo "192.168.1.$i is dead."
    fi
done
