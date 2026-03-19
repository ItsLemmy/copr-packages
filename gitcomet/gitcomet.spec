%global debug_package %{nil}

Name:           gitcomet
Version:        0.1.6
Release:        1%{?dist}
Summary:        A fast Git UI built in Rust with GPUI

License:        AGPL-3.0-only
URL:            https://github.com/Auto-Explore/GitComet
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  cargo
BuildRequires:  rust >= 1.94.0
BuildRequires:  gcc
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  alsa-lib-devel
BuildRequires:  fontconfig-devel
BuildRequires:  glib2-devel
BuildRequires:  libva-devel
BuildRequires:  wayland-devel
BuildRequires:  libxcb-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  openssl-devel
BuildRequires:  libzstd-devel
BuildRequires:  sqlite-devel
BuildRequires:  desktop-file-utils

Requires:       libwayland-client
Requires:       libxcb
Requires:       libxkbcommon-x11
Requires:       mesa-vulkan-drivers
Requires:       fontconfig
Requires:       alsa-lib

%description
GitComet is a fast, free, and familiar Git user interface. Built end-to-end
in Rust using smol, gix, and GPUI, it stays responsive even on huge
repositories like Chromium. Supports staging, commits, branching, worktrees,
inline and side-by-side diffs, and 2-way/3-way merge tools. Can also serve
as a drop-in git difftool and git mergetool replacement.

%prep
%autosetup -n GitComet-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build -p gitcomet --features ui-gpui,gix --release --locked

%install
install -Dpm 0755 target/release/%{name} -t %{buildroot}%{_bindir}/

# Desktop file
install -Dpm644 assets/linux/gitcomet.desktop %{buildroot}%{_datadir}/applications/gitcomet.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/gitcomet.desktop

# Icons
for size in 32x32 48x48 128x128 256x256 512x512; do
    install -Dpm644 assets/linux/hicolor/${size}/apps/gitcomet.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/gitcomet.png
done

%files
%license LICENSE-AGPL-3.0
%doc README.md CONTRIBUTING.md
%{_bindir}/gitcomet
%{_datadir}/applications/gitcomet.desktop
%{_datadir}/icons/hicolor/*/apps/gitcomet.png

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
