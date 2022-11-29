#!/bin/bash

for d in */; 
do
    echo "Starting Directory: ${d}";
    for a in $d*.HEIC;
    do 
        echo ${a};
        convert ${a} ${a/HEIC/jpg}; 
    done
done

echo "Removing all .HEIC files"
find . -name "*.HEIC" -type f -delete
echo "Done!"