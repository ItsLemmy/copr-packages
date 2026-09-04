Name:           umbriel-git
Version:        @VERSION@
Release:        1%{?dist}
Summary:        A Wayland compositor built on wlroots

License:        MIT
URL:            https://github.com/noctalia-dev/umbriel
Source0:        %{url}/archive/@COMMIT@.tar.gz#/umbriel-@COMMIT@.tar.gz

ExclusiveArch:  aarch64 x86_64

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  nlohmann-json-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libinput) >= 1.23
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-server) >= 1.24
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.0
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  systemd-rpm-macros

Requires:       xwayland-satellite
Recommends:     xdg-desktop-portal-umbriel

%description
Umbriel is a Wayland compositor designed for daily use. It supports scrolling,
dwindle, and master layouts, independent output workspaces, window rules,
blur, shadows, and fluid animations.

%prep
%autosetup -n umbriel-@COMMIT@

%build
%meson -Dtests=disabled
%meson_build

%install
%meson_install

%files
%license LICENSE umbrielfx/LICENSE
%doc README.md PACKAGING.md
%{_bindir}/umbriel
%{_bindir}/start-umbriel
%{_datadir}/umbriel/config.toml
%{_datadir}/wayland-sessions/umbriel.desktop
%{_userunitdir}/umbriel.service
%{_userunitdir}/umbriel-session.target
%{_userunitdir}/umbriel-shutdown.target

%post
%systemd_user_post umbriel.service

%preun
%systemd_user_preun umbriel.service

%postun
%systemd_user_postun_with_restart umbriel.service

%changelog
%autochangelog
