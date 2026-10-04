# COPR Packages

A repository for all the RPM .spec files that I maintain on Fedora COPR.

## Fluxer Canary

`fluxer-canary/generate-srpm.sh <resultdir>` downloads the latest canary
release and generates its RPM spec. The source generator and scheduled
update check follow redirects from Fluxer's download API to its package
host; without this, metadata retrieval fails before the RPM build starts.
