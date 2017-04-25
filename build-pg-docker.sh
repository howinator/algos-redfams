#!/usr/bin/env bash

docker build -t algos-red-image .
docker run -d --name algos-red-container -p 32768:5432 algos-red-image
