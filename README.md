# COPR Packages

RPM specs for [lemmy/favorites](https://copr.fedorainfracloud.org/coprs/lemmy/favorites/).

```sh
sudo dnf copr enable lemmy/favorites
sudo dnf install <package>
```

## Stable release updates

GitHub Actions workflows for `cava`, `dotter`, `gitcomet`, `lazygit`,
`limine-snapper-sync`, `omp-gui`, `protonplus`, `rhun`, and `tuios` check for stable upstream releases every
6 hours and can also be run manually. They update each package's spec, reset
the RPM release to `1`, commit the change, and trigger a build in
`lemmy/favorites` when its latest successful version differs from upstream.

limine-snapper-sync releases are fetched from GitLab; the others use GitHub.
ProtonPlus and omp-gui updates also refresh the source SHA256 checked by their specs.

These workflows use the existing `COPR_CONFIG` repository secret. Each COPR
package must build from this repository's default branch using its spec.
GitHub Actions must be allowed to push to that branch.

## Protokol

```sh
sudo dnf install protokol
```

Repackages Hexler's proprietary freeware for x86_64 and aarch64 with upstream
icons and an application-menu entry. Launch with `protokol`. Redistribution
was approved by Hexler support on the condition that updates are automated.

The workflow checks [Hexler's releases](https://hexler.net/protokol/releases)
daily at 05:23 UTC and can also be run manually. It selects the newest Linux
release available for both architectures, verifies upstream SHA256 checksums,
updates the spec and pinned checksums, and triggers the `protokol` package in
`lemmy/favorites` using `COPR_CONFIG`. The RPM version includes Hexler's build
number to detect build-only updates. Configure that COPR package to build from
`protokol/protokol.spec` on this repository's default branch.

The source RPM includes both architecture payloads; binary builds select and
verify the matching one, regardless of the source builder's architecture.

## KodeLife

```sh
sudo dnf install kodelife
```

Repackages [Hexler's KodeLife](https://hexler.net/kodelife), a proprietary
real-time GPU shader editor, for x86_64 and aarch64. Launch with `kodelife`
or the application-menu entry. Includes upstream application and project icons,
the `.klproj` MIME type, and file-opening support. The package does not include
a license key or change the application's licensing.
See the [upstream EULA](https://hexler.net/kodelife/eula).

The GitHub Actions workflow checks Hexler's releases daily at 05:43 UTC and
supports manual runs. Like Protokol, it waits for both Linux architectures,
verifies upstream SHA256 checksums, updates the spec and pinned checksums,
and triggers the `kodelife` package in `lemmy/favorites` using `COPR_CONFIG`.
The RPM version includes the upstream build number. Both payloads are included
in the source RPM to support source builders of either architecture.
The COPR package uses `kodelife/kodelife.spec` on this repository's default branch.

## Umbriel

```sh
sudo dnf install umbriel-git xdg-desktop-portal-umbriel-git
```

Log out and back in to use an updated compositor. Upgrades no longer restart
Umbriel, but upgrading from an older build can still end the session: run that
upgrade from a TTY after logging out.

Umbriel packages are built for Fedora 44 and newer only; Fedora 43 lacks
`wlroots-0.20` and `libdisplay-info >= 0.3.0`.

The snapshot spec declares Umbriel's direct Meson dependencies explicitly,
including `libeis-1.0 >= 1.3`, `libdisplay-info >= 0.3.0`, `libsystemd >= 243`,
and the XCB libraries, rather than relying on transitive wlroots dependencies.

## Noctalia Greeter

```sh
sudo dnf install noctalia-greeter-git
```

Set the session wrapper in `/etc/greetd/config.toml`:

```toml
[default_session]
command = "/usr/bin/noctalia-greeter-session"
user = "greetd"
```

The package creates `/var/lib/noctalia-greeter` for the `greetd` user.

## Building Fluxer Canary

`fluxer-canary/generate-srpm.sh <resultdir>` generates the spec from the latest
canary release.

## Strata

```sh
sudo dnf install strata
```

Repackages upstream prebuilt binaries, including alpha, beta, RC, and nightly
prereleases. A GitHub Actions workflow checks every 6 hours for the most recently
published release, verifies its archive checksum when updating, bumps
`strata/strata.spec`, and triggers the COPR build. RPM prerelease versions use `~`
so the final stable release sorts newer than its prereleases.

It does not set Strata as the default file manager or system file chooser;
see `strata --help` for those options.

## rhun

```sh
sudo dnf install rhun
```

Repackages the stable upstream Linux x86_64 release of
[rhun](https://github.com/vshvedov/rhun), a code editor written in assembly
(static binary, desktop entry, `rhun://` link handler, icons). The workflow
checks for a new tagged release daily at 05:17 UTC and can also be run
manually; it bumps `rhun/rhun.spec` and triggers the `rhun` COPR package.

## TUIOS

```sh
sudo dnf install tuios
```

Builds the stable upstream release from source with the default pure-Go terminal
backend. Requires a true-color terminal; run `tuios` to start a session.

## omp GUI

```sh
sudo dnf install omp-gui
```

Repackages the stable upstream Linux x86_64 release, including Electron and the
bundled omp agent; no separate omp, Bun, or Node installation is required.
Launch `omp-gui` or use the application-menu entry, with the upstream icon and
`omp://` link handling. The package does not replace the `omp` CLI.
Rosé Pine is included in upstream releases starting with 0.9.30; the package
ships the upstream themes without modifying the application bundle.

The update workflow checks every 6 hours and can also be run manually. It waits
until the release's Linux `.deb` asset is available, refreshes its SHA256 and
the spec version, and triggers the `omp-gui` COPR package build. Installed
packages receive new builds through normal DNF updates.
