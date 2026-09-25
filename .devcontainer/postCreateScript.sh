#!/bin/sh

##########################################################################################
# Constants
##########################################################################################
readonly GITHUB_URL="https://raw.githubusercontent.com"
readonly ALIAS_SRC_URL="${GITHUB_URL}/gvatsal60/Linux-Aliases/HEAD/install.sh"

##########################################################################################
# Functions
##########################################################################################
curl_https() {
    if ! command -v curl >/dev/null 2>&1; then
        echo "Error: curl is not installed. Aborting." >&2
        return 1
    fi
    curl -fsSL --proto '=https' "$@"
}

##########################################################################################
# Main Script
##########################################################################################

# Install Linux aliases from external script using curl and execute immediately
# Note: Make sure to review scripts fetched from external sources for security reasons
curl_https "${ALIAS_SRC_URL}" | sh
