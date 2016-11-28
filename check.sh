#!/usr/bin/env sh
for i in input/*.in; do
    ./proj3 $i > aux.out;
    ./vmc-checker $i aux.out;
    rm aux.out;
done
