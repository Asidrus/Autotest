#!/bin/bash
args="";
for arg in "$@"
do
args="$args $arg";
done
docker-compose run \
  --rm \
  autotest \
  bash \
  -c \
  "pytest $args"