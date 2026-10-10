Name:           xdg-desktop-portal-umbriel-git
Version:        @VERSION@
Release:        1%{?dist}
Summary:        XDG desktop portal backend for Umbriel

License:        MIT
URL:            https://github.com/noctalia-dev/xdg-desktop-portal-umbriel
Source0:        %{url}/archive/@COMMIT@.tar.gz#/xdg-desktop-portal-umbriel-@COMMIT@.tar.gz

ExclusiveArch:  aarch64 x86_64

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39
BuildRequires:  /usr/bin/wayland-scanner
BuildRequires:  systemd-rpm-macros

Requires:       xdg-desktop-portal
Requires:       pipewire
Provides:       xdg-desktop-portal-umbriel = %{version}-%{release}
Conflicts:      xdg-desktop-portal-umbriel

%description
An XDG desktop portal backend for the Umbriel Wayland compositor, implementing
ScreenCast and Screenshot. Includes the GTK4 screen and window share picker.

%prep
%autosetup -n xdg-desktop-portal-umbriel-@COMMIT@

%build
%meson -Dpicker=enabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-umbriel
%{_libexecdir}/umbriel-share-picker
%{_datadir}/xdg-desktop-portal/portals/umbriel.portal
%{_datadir}/xdg-desktop-portal/umbriel-portals.conf
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.umbriel.service
%{_userunitdir}/xdg-desktop-portal-umbriel.service

%post
%systemd_user_post xdg-desktop-portal-umbriel.service

%preun
%systemd_user_preun xdg-desktop-portal-umbriel.service

%postun
%systemd_user_postun_with_restart xdg-desktop-portal-umbriel.service

%changelog
%autochangelog
