#!/bin/bash
# This script downloads redis-server
# if redis has not already been downloaded
if [ ! -d redis-4.0.10/src ]; then
    wget http://download.redis.io/releases/redis-4.0.10.tar.gz
    tar xzf redis-4.0.10.tar.gz
    rm redis-4.0.10.tar.gz
    cd redis-4.0.10
    make
else
    cd redis-4.0.10
fi