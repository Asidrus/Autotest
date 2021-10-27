#!/bin/bash
if (($1=="--help")); then
  echo "Scrip runner for docker:"
  echo "bash run.sh pytest --alluredir='/home/tester/autotest/allure-results' test_formSending.py"
  fi
test=$1;
args="";
i=1;
for arg in "$@"
do
  if (($i!=1)); then
    args="$args $arg";
    fi
  i=$((i+1));
done
source /opt/conda/etc/profile.d/conda.sh
conda activate autotest
eval "$1 $args"