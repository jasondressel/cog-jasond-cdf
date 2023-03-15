#!/bin/sh

poetry add msal
poetry add cognite-sdk
poetry add cognite-sdk-experimental
poetry add cognite-extractor-utils
poetry add cognite-wells-sdk
poetry add --dev ipykernel
poetry add --dev flake8
poetry add --dev black --allow-prereleases
poetry install
