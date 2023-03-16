#!/bin/sh

#az login --tenant $TENANT_ID --allow-no-subscriptions

az login --tenant 35be0c51-a048-4a15-9f92-33302755860f --allow-no-subscriptions

    # all
    # jason
    # kiran
    # hector  
user_names=(

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

permissions=(read owner)
echo "${permissions[*]}"


function create_group {
    echo "# $name's groups"

    for p in "${permissions[@]}"
    do
        cdf_group_name="cdf:bsee:$name:$p"
        echo "- cdf-group: $cdf_group_name"

        group_name="cdf-bsee-$name-$p"
        echo "  idp-source-name: $group_name"

        object_id=$(az ad group create --display-name $group_name --mail-nickname $group_name --force false | jq -r '.id')
        echo "  idp-source-id: $object_id"
    done
}

for name in "${user_names[@]}"
do
    create_group
done
