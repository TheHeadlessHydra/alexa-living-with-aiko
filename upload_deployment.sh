#!/usr/bin/env bash


cd lambda
zip -r alexa-living-with-aiko.zip ./*
mv alexa-living-with-aiko.zip ../
cd ../


aws s3 cp ./alexa-living-with-aiko.zip s3://crossfade-alexa-deployment/living-with-aiko-v2/  --profile=crossfade

aws lambda update-function-code --function-name AlexaLivingWithAikoV2 --s3-bucket crossfade-alexa-deployment --s3-key living-with-aiko-v2/alexa-living-with-aiko.zip --publish --profile=crossfade --region us-east-1
