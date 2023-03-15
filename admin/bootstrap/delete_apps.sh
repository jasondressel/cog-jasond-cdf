#!/bin/sh

#az login --tenant $TENANT_ID --allow-no-subscriptions

#az login --tenant 35be0c51-a048-4a15-9f92-33302755860f --allow-no-subscriptions

apps=(
7ec89708-c293-4931-b8e4-7825ed648254 969ae7d3-eb87-4229-9e6e-215971603bd8 e562f798-a4a5-4f9e-8901-a1eba4aaebc2 043a7652-cc7c-4b76-966f-ed2b66d33d88 bddb1b7e-7eb7-4531-b232-7a80c308241e a789f763-cbc4-44f5-9b36-b92722f0d16d 61c478db-0f31-471a-adc0-49bd0ee2de92 e0996edf-847f-4609-9690-53c0b83fec87 cf16c19a-ddf8-4b08-a561-e04c15f92a6b ff3d8b20-11f7-4d73-a936-6c522e1091ac 
)

for a in "${apps[@]}"
do
    az ad app delete --id $a
done