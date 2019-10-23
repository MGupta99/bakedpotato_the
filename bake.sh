#!/bin/bash

cwd=$(pwd)

cd "~/Documents/Go\ Blue/Freshman/Winter\ Term/EECS\ 183/Projects/Creative_AI_317_Repository/"
python generate.py < OneTweet.txt

cd $cwd
