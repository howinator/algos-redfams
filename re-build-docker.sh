#!/usr/bin/env bash

docker stop algos-red-container
docker rm algos-red-container
docker rmi algos-red-image

./build-pg-docker.sh
