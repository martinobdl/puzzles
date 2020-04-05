#!/bin/bash

for f in ./dlx/data/tri_*.txt; do 
    echo $f; 
    timeout 30 ./dlx/build/dlx -pv < $f > ./dlx/sol/${f//[!0-9]/}.txt; 
    exit_status=$?
    if [[ $exit_status -eq 124 ]]; then
        echo timeout > ./dlx/sol/${f//[!0-9]/}.txt;
    fi
    echo; 
done 



