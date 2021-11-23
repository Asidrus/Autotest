#!/bin/bash
args="";
for arg in "$@"
do
args="$args $arg";
done
docker run \
        --rm \
        --net=host \
        -v /home/tester/autotest-results:/home/tester/autotest-results \
        -v /home/tester/allure-results:/home/tester/allure-results \
        -v /etc/localtime:/etc/localtime:ro \
        autotest \
        bash -c \
        "pytest tests/$args"