#!/usr/bin/env bash
# this script merges the env variables from the environment and the .env.example file into the .env file
# the appended variables take precedence over the .env.example variables (if both are set)

# Usage in a github action:
# - name: Generate .env
#   run: ./scripts/merge-env.sh

set -e

cp .env.example .env
echo >> .env
printenv | awk -F= '{print $1"=\""substr($0, index($0,$2))"\""}' >> .env