#!/bin/sh

user_names=(all jason kiran hector)
echo "${names[*]}"

for name in "${user_names[@]}"
do
    echo "- node-name: bsee:$name"
    echo "  description: $name"
done