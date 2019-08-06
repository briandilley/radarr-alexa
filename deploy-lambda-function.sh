#!/bin/sh -e -x

rm -rf build

pip install -r requirements.txt --target ./build

cp -Rv radarr_alexa ./build
cp -Rv function.py ./build

cd radarr_alexa && zip -r9 ../function.zip . && cd ..

