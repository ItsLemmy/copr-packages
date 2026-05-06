#!/bin/bash
set -euo pipefail

git clone --depth 1 https://github.com/ItsLemmy/copr-packages.git repo
cd repo/fluxer-canary
./generate-srpm.sh "$COPR_RESULTDIR"
