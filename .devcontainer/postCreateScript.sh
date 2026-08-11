#!/bin/sh

##########################################################################################
# Constants
##########################################################################################
readonly GITHUB_URL="https://raw.githubusercontent.com"
readonly ALIAS_SRC_URL="${GITHUB_URL}/gvatsal60/Linux-Aliases/HEAD/install.sh"

##########################################################################################
# Main Script
##########################################################################################

# Install Linux aliases from external script using curl and execute immediately
# Note: Make sure to review scripts fetched from external sources for security reasons
if command -v curl >/dev/null 2>&1; then
    curl -fsSL "${ALIAS_SRC_URL}" | sh
else
    echo "Error: curl is not installed. Unable to use Linux aliases"
    exit 1
fi
