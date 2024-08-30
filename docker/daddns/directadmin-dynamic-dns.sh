#!/bin/bash

# Script for automatically updating the DNS records using the DirectAdmin API.
# Requires you to have curl, dig and jq installed.
#
# Inspired by
# https://gist.github.com/DvdGiessen/b4203c69bf0c92f153ea05ed54d804c4

# Get current external IP address of this machine
CURRENT_IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

IFS=',' read -r -a RECORDS <<< "${A_RECORDS}"

for RECORD in "${RECORDS[@]}"
do
    # Get the currently configured IP address from the authoritive nameserver
    CONFIGURED_IP="$(dig +short "${RECORD}.${ROOT_DOMAIN_NAME}" A @$(dig +short "${ROOT_DOMAIN_NAME}" NS | head -n1))"

    echo "Current DNS record for ${RECORD}.${ROOT_DOMAIN_NAME} is ${CONFIGURED_IP}. Current IP is ${CURRENT_IP}."

    # Check if the IP needs to be updated
    if [[ "${CONFIGURED_IP}" != "${CURRENT_IP}" ]] ; then
        # Change the IP through the DA API
        # Note: Used --insecure because our DA instance doesn't return the complete intermediate certificate.
        # If yours does, it is probably a good idea to remove the --insecure flag
        # Browsers deal with this fine since they have the intermediate in their store. curl does not.
        RESULT="$(curl -sS --insecure -u "${DA_USERNAME}:${DA_PASSWORD}" "${DA_URL}/CMD_API_DNS_CONTROL?domain=${ROOT_DOMAIN_NAME}&action=edit&arecs0=name%3D${RECORD}%26value%3D${CONFIGURED_IP}&type=A&name=${RECORD}&value=${CURRENT_IP}&json=yes")"
        if [[ "$(echo "${RESULT}" | jq -r '.success')" == "Record Edited" ]] ; then
            echo "Updated IP address for ${RECORD}.${ROOT_DOMAIN_NAME} on DirectAdmin from ${CONFIGURED_IP} to ${CURRENT_IP}! :)"
        else
            echo "Failed to update IP address for ${RECORD}.${ROOT_DOMAIN_NAME} on DirectAdmin from ${CONFIGURED_IP} to ${CURRENT_IP}! :(" >&2
            echo "${RESULT}" >&2
        fi
    fi
done
