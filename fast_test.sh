#!/bin/bash
# Script to test the aplication by sending apks to the server and run the manager

echo 'Starting test, assuming server.py is running on localhost:5000'
echo 'Run with 1 apk only[1] or run with all apks of the list[2]?'
read varoption

file="apks.txt"
# Just sending one apk to test the api
if [ $varoption = "1" ];
then
    firstLine=$(head -n 1 $file)
    echo "Sending $firstLine"
    curl -X POST "http://localhost:5000/apkscan?md5=$line"
    sed -i '1d' $file
    python3 manager.py
fi

# Send all apks in the list
if [ $varoption = "2" ];
then
    n=1
    while read line; do
        echo "$line"
        curl -X POST "http://localhost:5000/apkscan?md5=$line"
        n=$((n+1))
    done < $file
    python3 manager.py
fi

echo 'script completed'
# file='apks.txt'
# n=1
# while read line; do
# echo "LINE No $n : $line"
# n=$((n+1))
# done < $file

# python3 manager.py