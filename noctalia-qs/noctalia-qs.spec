%global forgeurl https://github.com/noctalia-dev/noctalia-qs
%global tag v%{version}

Name:           noctalia-qs
Version:        0.0.2
Release:        1%{?dist}
Summary:        Flexible toolkit for making desktop shells with QtQuick (Noctalia fork)

License:        LGPL-3.0-only AND GPL-3.0-only
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/refs/tags/%{tag}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils

# Qt6 dependencies
BuildRequires:  qt6-qtbase-devel >= 6.6
BuildRequires:  qt6-qtbase-private-devel >= 6.6
BuildRequires:  qt6-qtdeclarative-devel >= 6.6
BuildRequires:  qt6-qtdeclarative-private-devel >= 6.6
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qtsvg-devel

# Build dependencies
BuildRequires:  spirv-tools
BuildRequires:  cli11-devel

# Wayland dependencies
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

# Feature dependencies
BuildRequires:  pipewire-devel
BuildRequires:  libxcb-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  jemalloc-devel
BuildRequires:  polkit-devel
BuildRequires:  glib2-devel
BuildRequires:  pam-devel
BuildRequires:  NetworkManager-libnm-devel
BuildRequires:  bluez-libs-devel

Conflicts:      quickshell
Conflicts:      quickshell-git

%description
Noctalia-qs is a fork of Quickshell, a flexible toolkit for creating custom
desktop shells and widgets using QtQuick/QML. It supports both Wayland and X11
display servers and provides integrations with various desktop services including
system tray, MPRIS, PipeWire, and window managers like Hyprland and i3/Sway.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DDISTRIBUTOR="COPR (Fedora)" \
    -DDISTRIBUTOR_DEBUGINFO_AVAILABLE=YES \
    -DCRASH_REPORTER=OFF

%cmake_build

%install
%cmake_install

desktop-file-validate %{buildroot}%{_datadir}/applications/dev.noctalia.noctalia-qs.desktop

%files
%license LICENSE LICENSE-GPL
%doc README.md BUILD.md
%{_bindir}/qs
%{_datadir}/applications/dev.noctalia.noctalia-qs.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.noctalia.noctalia-qs.svg

%changelog
%autochangelog
