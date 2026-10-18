%global commit @COMMIT@

Name:           strata-git
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Fast, keyboard-first GTK4 file manager with Miller columns (git snapshot)

# Strata itself is MIT; the bundled UnRAR code carries the UnRAR license
License:        MIT AND LicenseRef-UnRAR
URL:            https://github.com/lgse/strata
Source0:        %{url}/archive/%{commit}.tar.gz#/strata-%{commit}.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-app-1.0) >= 1.20

Requires:       gtk4 >= 4.12
Requires:       gtksourceview5
Requires:       poppler-glib
Requires:       fontconfig
Requires:       bubblewrap
Requires:       gstreamer1-plugins-good
Requires:       ffmpegthumbnailer
Requires:       /usr/bin/ffmpeg
Requires:       gvfs
Recommends:     gvfs-smb
Recommends:     hicolor-icon-theme

Provides:       strata = %{version}-%{release}
Conflicts:      strata

%description
Strata is a fast, keyboard-first file manager for Linux built with Rust and
GTK4. It combines Miller-column navigation with icon and list views, recursive
fuzzy search, and rich previews for images, RAW photos, PDFs, code, audio and
video. Native parsers for untrusted files run in Bubblewrap sandboxes. Remote
locations are browsed through GIO/GVfs.

This package is built from the latest upstream main branch. It does not
register Strata as the default file manager or system file chooser.

%prep
%autosetup -n strata-%{commit}
cargo vendor
find vendor -type f -name '*.rs' -perm /111 -exec chmod a-x {} +
%cargo_prep -v vendor

%build
# The source archive has no .git, so build.rs cannot discover the commit itself.
export STRATA_BUILD_COMMIT=%{commit}
%cargo_build

%install
install -Dpm 0755 target/rpm/strata -t %{buildroot}%{_bindir}/
install -Dpm 0644 data/io.github.lgse.Strata.desktop -t %{buildroot}%{_datadir}/applications/
install -Dpm 0644 data/icons/scalable/apps/io.github.lgse.Strata.svg -t %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.lgse.Strata.desktop
# Marks the install as package-managed so the in-app updater defers to dnf
# instead of replacing /usr/bin/strata with a stable release.
install -Dpm 0644 /dev/stdin %{buildroot}%{_datadir}/strata/install-source.toml <<'EOF'
manager = "dnf"
package = "strata-git"
update_command = "sudo dnf upgrade --refresh strata-git"
EOF

%files
%license LICENSE data/licenses/UnRAR.txt THIRD_PARTY_LICENSES.md
%doc README.md docs/portal-file-chooser.md
%{_bindir}/strata
%{_datadir}/applications/io.github.lgse.Strata.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg
%dir %{_datadir}/strata
%{_datadir}/strata/install-source.toml

%post
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :

%changelog
%autochangelog
