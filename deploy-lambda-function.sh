#!/bin/sh -e -x

rm -rf build

pip install -r requirements.txt --target ./build

cp -Rv radarr_alexa ./build

cd build && zip -r9 ../function.zip . && cd ..

aws --profile=radarr-alexa lambda update-function-code --function-name radarrAlexaSkill --zip-file fileb://function.zip
