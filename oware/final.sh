#!/usr/bin/env bash
rm -rf agents3/__pycache__

python3 ./oware.py -n 5 -T agents3/* > turnaj.txt
rm -rf agents3/__pycache__

for i in agents3/* ; do
    rm -rf orgAI/__pycache__
    python3 ./oware.py -n 5 -T -C "$i" orgAI/* > "odmena${i}.txt"
done
