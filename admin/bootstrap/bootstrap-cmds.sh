#!/bin/sh

poetry run bootstrap-cli diagram --cdf-project=pemex-dev /Users/jason.dressel/Code/cog-jasond-cdf/admin/bootstrap/bootstrap-cli-config-pemex-dev.yml > diagram.txt

poetry run bootstrap-cli prepare --idp-source-id 8cbe6405-dfbe-4fb2-99d3-76d2032a1c08 /Users/jason.dressel/Code/cog-jasond-cdf/admin/bootstrap/bootstrap-cli-config-pemex-dev.yml

poetry run bootstrap-cli deploy /Users/jason.dressel/Code/cog-jasond-cdf/admin/bootstrap/bootstrap-cli-config-pemex-dev.yml