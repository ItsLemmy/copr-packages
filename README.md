# COPR Packages

A repository for all the RPM .spec files that I maintain on Fedora COPR.

## Fluxer Canary

`fluxer-canary/generate-srpm.sh <resultdir>` downloads the latest canary
release and generates its RPM spec. The source generator and scheduled
update check follow redirects from Fluxer's download API to its package
host; without this, metadata retrieval fails before the RPM build starts.

## XDG Desktop Portal Umbriel Git

`xdg-desktop-portal-umbriel-git/xdg-desktop-portal-umbriel-git.spec` packages
upstream git snapshots, including the GTK4 share picker. The matching GitHub
Actions workflow checks upstream daily and submits new snapshots to the existing
`lemmy/favorites` COPR project using the `COPR_CONFIG` secret.

```sh
sudo dnf copr enable lemmy/favorites
sudo dnf install xdg-desktop-portal-umbriel-git
```

The package provides `xdg-desktop-portal-umbriel`, satisfying `umbriel-git`'s
recommendation. Portal selection and D-Bus/systemd user activation files are
installed automatically.
