#!/bin/bash
# https://www.reddit.com/r/ipv6/comments/txgof1/hook_ipv6_prefix_change_in_linux
# https://unix.stackexchange.com/questions/552258/ip-monitor-responding-to-events

# Event during prefix change example
# Deleted default via <::1> proto ra metric 1024 expires 1518sec hoplimit 64 pref medium
# default via <::1> proto ra metric 1024 pref medium
# <::1/64> proto kernel metric 256 expires 86400sec pref medium
# local <::1> table local proto kernel metric 0 pref medium
# local <::1> table local proto kernel metric 0 pref medium
ip monitor route dev eth0 | while read event; do
    if [[ $event == *'/'* ]] && [[ $event == *'proto kernel'* ]]; then
        python3 main.py -p "$event" -a eth0
        echo 'Done main.py'
    fi
done
