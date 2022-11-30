#!/bin/bash

for d in */; 
do
    echo "Starting HEIC photos in Directory: ${d}";
    for a in $d*.HEIC;
    do 
        echo ${a};
        convert ${a} ${a/HEIC/jpg}; 
    done
    echo "Starting MOV video files in Directory: ${d}";
    for i in $d*.MOV;
    do 
        echo ${i};
        ffmpeg -i "$i" "${i%.*}.mp4";
    done
done

echo "Removing all .HEIC files"
find . -name "*.HEIC" -type f -delete
echo "Removing all .MOV files"
find . -name "*.MOV" -type f -delete
echo "Done!"