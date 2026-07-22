%global debug_package %{nil}

%global commit      c5210b2b1d3f2b7398739ee4dc563a92c9952e9f
%global shortcommit c5210b2
%global commitdate  20260721

Name:           aqueous
Version:        0.4.1^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Single-process Wayland compositor (git snapshot)

License:        GPL-3.0-only AND MIT AND 0BSD AND CC-BY-SA-4.0
URL:            https://github.com/Seafoam-Labs/Aqueous
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz

# Zig package dependencies are listed as sources and unpacked locally so COPR
# builds never need network access. The versions and commit match build.zig.zon.
Source1:        https://codeberg.org/ifreund/zig-pixman/archive/v0.3.0.tar.gz#/zig-pixman-0.3.0.tar.gz
Source2:        https://codeberg.org/ifreund/zig-wayland/archive/v0.6.0.tar.gz#/zig-wayland-0.6.0.tar.gz
Source3:        https://codeberg.org/ifreund/zig-wlroots/archive/v0.20.1.tar.gz#/zig-wlroots-0.20.1.tar.gz
Source4:        https://codeberg.org/ifreund/zig-xkbcommon/archive/v0.4.0.tar.gz#/zig-xkbcommon-0.4.0.tar.gz
Source5:        https://codeberg.org/ziglang/translate-c/archive/57c559cf581b1fcad90494eda219f98abeb155ce.tar.gz#/translate-c-57c559cf581b1fcad90494eda219f98abeb155ce.tar.gz
Patch0:         aqueous-offline-deps.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  llvm
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros
BuildRequires:  tar
BuildRequires:  zig >= 0.16.0
BuildRequires:  wayland-protocols-devel
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(scenefx-0.5) >= 0.5
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20
BuildRequires:  pkgconfig(xkbcommon)

Requires:       grim
Requires:       libdecor
Requires:       libnotify
Requires:       noctalia
Requires:       slurp
Requires:       uwsm
Requires:       wl-clipboard
Requires:       xdg-desktop-portal-gtk
Requires:       xdg-desktop-portal-wlr
Requires:       xorg-x11-server-Xwayland
Recommends:     wireplumber
Suggests:       firefox
Suggests:       ghostty
Suggests:       greetd
Suggests:       nemo
Suggests:       noctalia-greeter
Conflicts:      aqueous-bin
Conflicts:      aqueous-git

%description
Aqueous is a single-process Wayland compositor with integrated window
management. This build enables Xwayland, SceneFX effects, animations, and the
legacy external policy protocol. It also installs a complete UWSM and Noctalia
desktop session with portal routing and sensible defaults.

%prep
%autosetup -n Aqueous-%{commit} -N

mkdir -p compositor/deps/{pixman,wayland,wlroots,xkbcommon,translate-c}
tar -xzf %{SOURCE1} --strip-components=1 -C compositor/deps/pixman
tar -xzf %{SOURCE2} --strip-components=1 -C compositor/deps/wayland
tar -xzf %{SOURCE3} --strip-components=1 -C compositor/deps/wlroots
tar -xzf %{SOURCE4} --strip-components=1 -C compositor/deps/xkbcommon
tar -xzf %{SOURCE5} --strip-components=1 -C compositor/deps/translate-c

%autopatch -p1

%build
cd compositor
export ZIG_GLOBAL_CACHE_DIR="${PWD}/.zig-global-cache"
zig build \
    -Dcpu=baseline \
    -Doptimize=ReleaseSafe \
    -Dpie=true \
    -Dllvm=true \
    -Dxwayland=true \
    -Dscenefx=true \
    -Danimations=true \
    -Dexternal-policy=true \
    -Dman-pages=true \
    --prefix ../aqueous-dist \
    install

%check
cd compositor
export ZIG_GLOBAL_CACHE_DIR="${PWD}/.zig-global-cache"
zig build test \
    -Dcpu=baseline \
    -Doptimize=ReleaseSafe \
    -Dllvm=true \
    -Dxwayland=true \
    -Dscenefx=true \
    -Danimations=true \
    -Dexternal-policy=true

for path in \
    bin/aqueous \
    bin/aqueousctl \
    share/man/man1/aqueous.1 \
    share/man/man1/aqueousctl.1 \
    share/aqueous-protocols/stable/aqueous-window-info-v1.xml; do
    test -e "../aqueous-dist/${path}"
done

%install
install -Dpm0755 aqueous-dist/bin/aqueous %{buildroot}%{_bindir}/aqueous
install -Dpm0755 aqueous-dist/bin/aqueousctl %{buildroot}%{_bindir}/aqueousctl

cp -a aqueous-dist/share/. %{buildroot}%{_datadir}/
sed -i 's|^prefix=.*|prefix=%{_prefix}|' \
    %{buildroot}%{_datadir}/pkgconfig/aqueous-protocols.pc

install -Dpm0755 packaging/aqueous-init %{buildroot}%{_bindir}/aqueous-init
install -Dpm0755 packaging/aqueous-wm.sh %{buildroot}%{_bindir}/aqueous-wm
install -Dpm0644 aqueous.desktop \
    %{buildroot}%{_datadir}/wayland-sessions/aqueous.desktop

install -Dpm0644 packaging/uwsm/env-aqueous \
    %{buildroot}%{_sysconfdir}/uwsm/env-aqueous
install -Dpm0644 packaging/aqueous-portals.conf \
    %{buildroot}%{_datadir}/xdg-desktop-portal/aqueous-portals.conf
install -Dpm0644 wm.toml %{buildroot}%{_sysconfdir}/xdg/aqueous/wm.toml
install -Dpm0644 wm.toml %{buildroot}%{_datadir}/aqueous/wm.toml

install -Dpm0644 packaging/aqueous-session.target \
    %{buildroot}%{_userunitdir}/aqueous-session.target
install -Dpm0644 packaging/noctalia.service \
    %{buildroot}%{_userunitdir}/noctalia.service
mkdir -p %{buildroot}%{_userunitdir}/graphical-session.target.wants
ln -s ../noctalia.service \
    %{buildroot}%{_userunitdir}/graphical-session.target.wants/noctalia.service

install -Dpm0644 packaging/aqueous.tmpfiles \
    %{buildroot}%{_user_tmpfilesdir}/aqueous.conf
install -Dpm0644 packaging/udev/70-aqueous-uaccess.rules \
    %{buildroot}%{_udevrulesdir}/70-aqueous-uaccess.rules

install -Dpm0644 packaging/noctalia/config.toml \
    %{buildroot}%{_datadir}/aqueous/noctalia/config.toml
install -d %{buildroot}%{_datadir}/aqueous/wallpapers
install -pm0644 packaging/wallpapers/*.avif \
    %{buildroot}%{_datadir}/aqueous/wallpapers/

install -Dpm0644 packaging/greetd/config.toml.example \
    %{buildroot}%{_docdir}/%{name}/greetd-config.toml.example
install -Dpm0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -d %{buildroot}%{_licensedir}/%{name}/compositor
install -pm0644 compositor/LICENSES/* \
    %{buildroot}%{_licensedir}/%{name}/compositor/

%post
%systemd_user_post aqueous-session.target noctalia.service

%preun
%systemd_user_preun aqueous-session.target noctalia.service

%postun
%systemd_user_postun aqueous-session.target noctalia.service

%files
%license %{_licensedir}/%{name}/compositor/*
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/greetd-config.toml.example
%{_bindir}/aqueous
%{_bindir}/aqueousctl
%{_bindir}/aqueous-init
%{_bindir}/aqueous-wm
%{_mandir}/man1/aqueous.1*
%{_mandir}/man1/aqueousctl.1*
%{_datadir}/pkgconfig/aqueous-protocols.pc
%{_datadir}/aqueous-protocols/
%{_datadir}/aqueous/
%{_datadir}/wayland-sessions/aqueous.desktop
%{_datadir}/xdg-desktop-portal/aqueous-portals.conf
%{_sysconfdir}/uwsm/env-aqueous
%config(noreplace) %{_sysconfdir}/xdg/aqueous/wm.toml
%{_userunitdir}/aqueous-session.target
%{_userunitdir}/noctalia.service
%{_userunitdir}/graphical-session.target.wants/noctalia.service
%{_user_tmpfilesdir}/aqueous.conf
%{_udevrulesdir}/70-aqueous-uaccess.rules

%changelog
%autochangelog
