#!/bin/bash

# Script for automatically updating the DNS records using the DirectAdmin API.
# Requires you to have curl, dig and json installed.
#
# By Daniël van de Giessen, 2018-09-10
# https://gist.github.com/DvdGiessen/b4203c69bf0c92f153ea05ed54d804c4

# Get current external IP address of this machine
CURRENT_IP="$(dig +short myip.opendns.com @resolver1.opendns.com)"

IFS=',' read -r -a DOMAINS <<< "${DOMAINNAMES}"

for DOMAINNAME in "${DOMAINS[@]}"
do
    # Get the currently configured IP address from the authoritive nameserver
    CONFIGURED_IP="$(dig +short "${DOMAINNAME}" A @$(dig +short "${DOMAINNAME}" NS | head -n1))"

    # Check if the IP needs to be updated
    if [[ "${CONFIGURED_IP}" != "${CURRENT_IP}" ]] ; then
        # Change the IP through the DA API
        # Note: Used --insecure because our DA instance doesn't return the complete intermediate certificate.
        # If yours does, it is probably a good idea to remove the --insecure flag
        # Browsers deal with this fine since they have the intermediate in their store. curl does not.
        RESULT="$(curl -sS --insecure -u "${DA_USERNAME}:${DA_PASSWORD}" "${DA_URL}/CMD_API_DNS_CONTROL?domain=${DOMAINNAME}&action=edit&arecs0=name%3D${DOMAINNAME}.%26value%3D${CONFIGURED_IP}&type=A&name=${DOMAINNAME}.&value=${CURRENT_IP}&json=yes")"
        if [[ "$(echo "${RESULT}" | jq -r '.success')" == "record added" ]] ; then
            echo "Updated IP address for ${DOMAINNAME} on DirectAdmin from ${CONFIGURED_IP} to ${CURRENT_IP}! :)"
        else
            echo "Failed to update IP address for ${DOMAINNAME} on DirectAdmin from ${CONFIGURED_IP} to ${CURRENT_IP}! :(" >&2
            echo "${RESULT}" >&2
        fi
    fi
done
