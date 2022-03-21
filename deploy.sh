#!/bin/sh

if [ "$1" = "local" ]; then
    # remove image
    echo "=> Remove previous image..."
    docker rmi -f jiho5993/movchatbot

    # new-build/re-build docker image
    echo "=> Build new image..."
    docker build -t jiho5993/movchatbot .

    # push image
    echo "=> Push image..."
    docker push jiho5993/movchatbot
else
    # remove container
    echo "=> Remove previous container..."
    docker rm -f movchatbot

    # pull image
    echo "=> Pull image..."
    docker pull jiho5993/movchatbot

    # run container
    echo "=> Run container..."
    docker run -d -p 80:3000 --name movchatbot jiho5993/movchatbot

    # prune image
    echo "=> Prune previous image..."
    docker image prune -af
fi