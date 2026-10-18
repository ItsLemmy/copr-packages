# COPR Packages

RPM specs for [lemmy/favorites](https://copr.fedorainfracloud.org/coprs/lemmy/favorites/).

```sh
sudo dnf copr enable lemmy/favorites
sudo dnf install <package>
```

## Lazygit

The `lazygit update check` GitHub Actions workflow checks for new stable upstream
releases every 6 hours and can also be run manually. It updates
`lazygit/lazygit.spec`, resets the RPM release to `1`, commits the change, and
triggers a build in `lemmy/favorites` when the latest successful COPR build is
behind upstream.

It uses the existing `COPR_CONFIG` repository secret. The COPR `lazygit` package
must build from this repository's default branch with
`lazygit/lazygit.spec` as its spec file. GitHub Actions must be allowed to push
to that branch.

## Umbriel

```sh
sudo dnf install umbriel-git xdg-desktop-portal-umbriel-git
```

Log out and back in to use an updated compositor. Upgrades no longer restart
Umbriel, but upgrading from an older build can still end the session: run that
upgrade from a TTY after logging out.

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
