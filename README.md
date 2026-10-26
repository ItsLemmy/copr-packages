# COPR Packages

RPM specs for [lemmy/favorites](https://copr.fedorainfracloud.org/coprs/lemmy/favorites/).

```sh
sudo dnf copr enable lemmy/favorites
sudo dnf install <package>
```

## Stable release updates

GitHub Actions workflows for `cava`, `dotter`, `gitcomet`, `lazygit`,
`limine-snapper-sync`, `omp-gui`, `protonplus`, and `tuios` check for stable upstream releases every
6 hours and can also be run manually. They update each package's spec, reset
the RPM release to `1`, commit the change, and trigger a build in
`lemmy/favorites` when its latest successful version differs from upstream.

limine-snapper-sync releases are fetched from GitLab; the others use GitHub.
ProtonPlus and omp-gui updates also refresh the source SHA256 checked by their specs.

These workflows use the existing `COPR_CONFIG` repository secret. Each COPR
package must build from this repository's default branch using its spec.
GitHub Actions must be allowed to push to that branch.

## Umbriel

```sh
sudo dnf install umbriel-git xdg-desktop-portal-umbriel-git
```

Log out and back in to use an updated compositor. Upgrades no longer restart
Umbriel, but upgrading from an older build can still end the session: run that
upgrade from a TTY after logging out.

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
The build adds a Rosé Pine entry to the GUI's built-in themes
(`omp-gui/rose-pine-themes.json`, applied by `omp-gui/add-gui-themes.py`); the
build fails if a new upstream release changes the bundle layout the patch expects.

The update workflow checks every 6 hours and can also be run manually. It waits
until the release's Linux `.deb` asset is available, refreshes its SHA256 and
the spec version, and triggers the `omp-gui` COPR package build. Installed
packages receive new builds through normal DNF updates.
