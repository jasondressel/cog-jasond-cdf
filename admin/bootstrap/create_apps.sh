#!/bin/sh

#az login --tenant $TENANT_ID --allow-no-subscriptions

#az login --tenant 35be0c51-a048-4a15-9f92-33302755860f --allow-no-subscriptions

user_names=(all jason kiran hector)
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
        echo "    client-id: $app_id"

        secret=$(az ad app credential reset --id $app_id | jq -r '.password')
        echo "    client-secret: $secret"

        # Create the service principle
        result=$(az ad sp create --id $app_id)
        
        # Add app to group - THERE ARE 2 F'ing Object Id's the One in the UI is different!
        #sleep 5
        #group_name="cdf-bsee-$name-$p"
        #az ad group member add --group $group_name --member-id $app_id

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