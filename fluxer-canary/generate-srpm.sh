#!/bin/bash
set -euo pipefail

API_URL="https://api.fluxer.app/dl/desktop/canary/linux/x64/latest"
SPEC_TEMPLATE="fluxer-canary.spec"

resultdir="${1:-.}"

# Fetch latest release metadata
metadata=$(curl -sf "$API_URL")
version=$(echo "$metadata" | jq -r '.version')
sha256=$(echo "$metadata" | jq -r '.files.tar_gz.sha256')
tar_url=$(echo "$metadata" | jq -r '.files.tar_gz.url')

if [ -z "$version" ] || [ -z "$sha256" ] || [ -z "$tar_url" ]; then
    echo "ERROR: Failed to parse release metadata" >&2
    exit 1
fi

echo "Latest version: $version (sha256: $sha256)"

# Fill in template
scriptdir="$(cd "$(dirname "$0")" && pwd)"
sed -e "s/@VERSION@/$version/g" \
    -e "s/@SHA256SUM0@/$sha256/g" \
    "$scriptdir/$SPEC_TEMPLATE" > "$resultdir/fluxer-canary.spec"

# Download source tarball
curl -sfL "$tar_url" -o "$resultdir/fluxer-canary-${version}-x64.tar.gz"

echo "Done — spec and source in $resultdir"
