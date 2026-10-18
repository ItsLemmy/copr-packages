# COPR Packages

RPM specs for [lemmy/favorites](https://copr.fedorainfracloud.org/coprs/lemmy/favorites/).

```sh
sudo dnf copr enable lemmy/favorites
sudo dnf install <package>
```

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

Repackages the upstream prebuilt release binary. A GitHub Actions workflow
checks for new releases every 6 hours, bumps `strata/strata.spec`, and
triggers the COPR build. It does not set Strata as the default file manager or
system file chooser; see `strata --help` for those options.

### strata-git

```sh
sudo dnf swap strata strata-git
```

Builds the latest upstream `main` from source. A GitHub Actions workflow checks
daily and submits a COPR build when `main` has a new commit. It conflicts with
`strata` and marks itself as dnf-managed so the in-app updater does not replace
the binary with a stable release.
