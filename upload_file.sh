#!/bin/bash
aws s3 cp data/weather.20160201.csv s3://$1/incoming/
aws s3 cp data/weather.20160301.csv s3://$1/incoming/