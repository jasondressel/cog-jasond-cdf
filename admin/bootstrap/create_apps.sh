#!/bin/sh

#az login --tenant $TENANT_ID --allow-no-subscriptions

az login --tenant 35be0c51-a048-4a15-9f92-33302755860f --allow-no-subscriptions

# user_names=(all jason kiran hector)
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
#
echo "${names[*]}"

permissions=(
    read
    owner
)

echo "${permissions[*]}"

prefix=cdf-bsee

apps=()

function create_app {
    echo "# $name's apps"

    for p in "${permissions[@]}"
    do
        cdf_app_name="$prefix-$name-$p-app"
        echo "- cdf-app: $cdf_app_name"

        app_id=$(az ad app create --display-name $cdf_app_name | jq -r '.appId')
        apps+="$app_id "
        echo "CLIENT_ID=$app_id"

        secret=$(az ad app credential reset --id $app_id | jq -r '.password')
        echo "CLIENT_SECRET=$secret"

        # Create the service principle
        sp_id=$(az ad sp create --id $app_id | jq -r '.id')
        
        # Add sp to group
        group_name="cdf-bsee-$name-$p"
        az ad group member add --group $group_name --member-id $sp_id

    done
}

for name in "${user_names[@]}"
do
    create_app
done

prefix="cdf"
name="all"
create_app

echo "${apps[*]}"