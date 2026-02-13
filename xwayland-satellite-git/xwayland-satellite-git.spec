%global debug_package %{nil}

%global forgeurl https://github.com/Supreeeme/xwayland-satellite
%global branch main

Name:           xwayland-satellite-git
Version:        0.8
Release:        1%{?dist}
Summary:        Rootless Xwayland integration for Wayland compositors

License:        MPL-2.0
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/refs/heads/%{branch}.tar.gz#/xwayland-satellite-%{branch}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust >= 1.85.0
BuildRequires:  clang
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-cursor)
BuildRequires:  pkgconfig(systemd)

Requires:       xorg-x11-server-Xwayland >= 23.1

# Conflict with stable package
Conflicts:      xwayland-satellite

Provides:       xwayland-satellite = %{version}-%{release}

%description
xwayland-satellite grants rootless Xwayland integration to any Wayland
compositor implementing xdg_wm_base and viewporter. It is designed for
compositors that prefer not to implement Xwayland support directly, allowing
legacy X11 applications to function alongside native Wayland programs.

%prep
%autosetup -n xwayland-satellite-%{branch}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked -F systemd

%install
install -Dpm 0755 target/release/xwayland-satellite -t %{buildroot}%{_bindir}/

# Install systemd user service
install -Dpm 0644 resources/xwayland-satellite.service %{buildroot}%{_userunitdir}/xwayland-satellite.service
# Fix ExecStart path
sed -i 's|/usr/local/bin/|%{_bindir}/|' %{buildroot}%{_userunitdir}/xwayland-satellite.service

%post
%systemd_user_post xwayland-satellite.service

%preun
%systemd_user_preun xwayland-satellite.service

%postun
%systemd_user_postun_with_restart xwayland-satellite.service

%files
%license LICENSE
%doc README.md
%{_bindir}/xwayland-satellite
%{_userunitdir}/xwayland-satellite.service

%changelog
%autochangelog
