#!/bin/bash

for f in data/tri_*.txt; do 
    echo $f; 
    timeout 180 ./build/dlx -pv < $f > sol/${f}; 
    exit_status=$?
    if [[ $exit_status -eq 124 ]]; then
        echo timeout > sol/${f};
    fi
    echo; 
done 



