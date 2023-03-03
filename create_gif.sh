#!/bin/bash
: << 'FILE HEADER'
Name: Alexander Zsikla
Date: March 2023

Takes a video file named demo.mov or demo.mp4 and creates a gif out of it
FILE HEADER

if [ -e demo.mov ]; then
    FILENAME=demo.mov
elif [ -e demo.mp4 ]; then
    FILENAME=demo.mp4
else
    echo "Error: no file named demo.{mov|mp4}"
    exit 1
fi

ffmpeg -i $FILENAME -vf "fps=15,scale=500:-1:flags=lanczos" -loop 0 demo.gif
rm $FILENAME
