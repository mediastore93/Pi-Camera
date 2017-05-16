#!/bin/bash

# Loop through h264 files in current directory
# and using MP4Box create MP4 files using
# specified frame rate.
# MP4Box can be installed using :
# sudo apt-get install gpac

cd ~/vid/raw
FRATE=30

for f in *.h264
do
  echo "Processing $f file..."
  filename=$(basename "$f")
  extension="${filename##*.}"
  filename="${filename%.*}"  
  MP4Box -fps $FRATE -add $f /home/pi/vid/mp4/$filename.mp4
done

# www.RaspberryPi-Spy.co.uk
# November 2014
