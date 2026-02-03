%global forgeurl https://git.outfoxxed.me/quickshell/quickshell
%global branch master

Name:           quickshell-git
Version:        0.2.1
Release:        1%{?dist}
Summary:        Flexible toolkit for making desktop shells with QtQuick

License:        LGPL-3.0-only AND GPL-3.0-only
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/%{branch}.tar.gz#/quickshell-%{branch}.tar.gz

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
BuildRequires:  qt6-qtwayland-private-devel
BuildRequires:  qt6-qtsvg-devel

# Build dependencies
BuildRequires:  spirv-tools
BuildRequires:  cli11-devel
BuildRequires:  breakpad-devel

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
BuildRequires:  systemd-devel
BuildRequires:  NetworkManager-libnm-devel
BuildRequires:  bluez-libs-devel

# Conflict with non-git package
Conflicts:      quickshell

Provides:       quickshell = %{version}-%{release}

%description
Quickshell is a flexible toolkit for creating custom desktop shells and
widgets using QtQuick/QML. It supports both Wayland and X11 display servers
and provides integrations with various desktop services including system
tray, MPRIS, PipeWire, and window managers like Hyprland and i3/Sway.

%prep
%autosetup -n quickshell

%build
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DDISTRIBUTOR="COPR (Fedora)" \
    -DDISTRIBUTOR_DEBUGINFO_AVAILABLE=YES \
    -DINSTALL_QML_PREFIX=%{_libdir}/qt6/qml

%cmake_build

%install
%cmake_install

# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/org.quickshell.desktop

%files
%license LICENSE LICENSE-GPL
%doc README.md BUILD.md
%{_bindir}/quickshell
%{_bindir}/qs
%{_libdir}/qt6/qml/Quickshell/
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg

%changelog
%autochangelog
