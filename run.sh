#!/bin/bash
args="";
for arg in "$@"
do
args="$args $arg";
done
docker run -it \
        --rm \
        --net=host \
        -v /home/tester/autotest/autotest-results:/home/tester/autotest/autotest-results \
        -v /home/tester/autotest/allure-results:/home/tester/autotest/allure-results \
        -v /home/tester/autotest/tests/resources:/home/tester/autotest/tests/resources \
        -it \
        -d \
        autotest \
        bash -c \
        "pytest $args"