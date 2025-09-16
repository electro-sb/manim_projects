#!/bin/bash
# A script to convert all mp4 files in a directory to jpg images using ffmpeg.
FILE_NAME=$1
if [ -z "$FILE_NAME" ]; then
  echo "Please provide the base name of the mp4 file (without extension)."
  exit 1
fi
cd ./media/videos/1080p60
ffmpeg -i ${FILE_NAME}.mp4 -vf "fps=20,scale=640:-1:flags=lanczos" -loop 0 ${FILE_NAME}.gif
echo "Conversion complete: ${FILE_NAME}.gif created."
mv ${FILE_NAME}.gif ../../../README_gif_assets/
cd ../../../
echo "Moved ${FILE_NAME}.gif to README_gif_assets directory."
