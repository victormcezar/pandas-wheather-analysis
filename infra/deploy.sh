#!/bin/bash
set -e

rm -rf .aws-sam


yapf --in-place --recursive lambdas
flake8 lambdas


sam build
sam package \
    --output-template-file .aws-sam/packaged.yaml \
    --s3-bucket $1
sam deploy \
    --template-file .aws-sam/packaged.yaml \
    --stack-name weather-analysis \
    --capabilities CAPABILITY_IAM \
    --s3-bucket $1 \
    --parameter-overrides RootBucket=$1 $(cat $2.properties)

rm -rf .aws-sam    