#!/usr/bin/env bash

exec 3>&2
exec 2> /dev/null

./MiniZinc/minizinc $1 $2

exec 2>&3
