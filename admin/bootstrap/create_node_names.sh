#!/bin/sh
 
user_names=(
    jason
    kiran
    hector 
    salvador
    omar
    victor
    luis
    otoniel
    vruiz
    emamani
    sroque
    cespinosa
    jmartinez
    nramirez
    svasquez
    mbenites
    ecabrera
    frodriguez
)

echo "${names[*]}"

for name in "${user_names[@]}"
do
    echo "            - node-name: bsee:$name"
    echo "              description: $name"
    echo "              shared-access:"
    echo "                read:"
    echo "                  - node-name: bsee:timeseries"

done