%global debug_package %{nil}

%global baseversion 0.4.4
%global commit      334cc0605674e08184bc0e66ee813f919555649c
%global shortcommit 334cc06
%global commitdate  20260726
%global commitcount 2

Name:           aqueous
Version:        %{baseversion}^%{commitdate}.%{commitcount}.git%{shortcommit}
Release:        1%{?dist}
Summary:        Single-process Wayland compositor (git snapshot)

License:        GPL-3.0-only AND MIT AND 0BSD AND CC-BY-SA-4.0 AND Unicode-3.0
URL:            https://github.com/Seafoam-Labs/Aqueous
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz

# Zig package dependencies are listed as sources and unpacked locally so COPR
# builds never need network access. The versions and commit match build.zig.zon.
Source1:        https://codeberg.org/ifreund/zig-pixman/archive/v0.3.0.tar.gz#/zig-pixman-0.3.0.tar.gz
Source2:        https://codeberg.org/ifreund/zig-wayland/archive/v0.6.0.tar.gz#/zig-wayland-0.6.0.tar.gz
Source3:        https://codeberg.org/ifreund/zig-wlroots/archive/v0.20.1.tar.gz#/zig-wlroots-0.20.1.tar.gz
Source4:        https://codeberg.org/ifreund/zig-xkbcommon/archive/v0.4.0.tar.gz#/zig-xkbcommon-0.4.0.tar.gz
Source5:        https://codeberg.org/ziglang/translate-c/archive/57c559cf581b1fcad90494eda219f98abeb155ce.tar.gz#/translate-c-57c559cf581b1fcad90494eda219f98abeb155ce.tar.gz
# Aqueous applies its in-tree Vulkan render-hook patches to this archive.
# compositor/scripts/build-wlroots-render-hook.sh verifies its SHA-256 digest.
Source6:        https://src.fedoraproject.org/repo/pkgs/rpms/wlroots/wlroots-0.20.2.tar.gz/sha512/634345e23d0b6c28cb501c0dd0ef9c50d529a92ae5c8455e99e876f3f37ee244ac19dd097f76416b2ae4fd7c3f02e39a92a9322cf5a0caf8da21c31cd900e508/wlroots-0.20.2.tar.gz
# translate-c dependency pinned by its build.zig.zon.
Source7:        https://github.com/Vexu/arocc/archive/5f5a050569a95ecc40a426f0c3666ae7ef987ede.tar.gz#/arocc-5f5a050569a95ecc40a426f0c3666ae7ef987ede.tar.gz
Patch0:         aqueous-offline-deps.patch
Patch1:         aqueous-wlroots-release-tarball.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  binutils
BuildRequires:  clang
BuildRequires:  coreutils
BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  glslang
BuildRequires:  jq
BuildRequires:  lld
BuildRequires:  llvm
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  patch
BuildRequires:  patchelf
BuildRequires:  pkgconfig
BuildRequires:  scdoc
BuildRequires:  ripgrep
BuildRequires:  systemd-rpm-macros
BuildRequires:  tar
BuildRequires:  vulkan-headers
BuildRequires:  zig >= 0.16.0
BuildRequires:  pkgconfig(gbm) >= 21.1
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdisplay-info) >= 0.2
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput) >= 1.21
BuildRequires:  pkgconfig(libliftoff) >= 0.4
BuildRequires:  pkgconfig(libseat) >= 0.2
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) >= 0.46
BuildRequires:  pkgconfig(vulkan) >= 1.2.182
BuildRequires:  pkgconfig(wayland-client) >= 1.24
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.24
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xkbcommon) >= 1.8
BuildRequires:  pkgconfig(xwayland)

Requires:       grim
Requires:       libdecor
Requires:       libnotify
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
Conflicts:      aqueous-bin
Conflicts:      aqueous-git

%description
Aqueous is a single-process Wayland compositor with integrated window
management. This build enables Xwayland, Vulkan effects, animations, and the
legacy external policy protocol. It also installs a complete UWSM desktop
session with portal routing and sensible defaults.

%prep
%autosetup -n Aqueous-%{commit} -N

mkdir -p compositor/deps/{arocc,pixman,wayland,wlroots,xkbcommon,translate-c}
tar -xzf %{SOURCE7} --strip-components=1 -C compositor/deps/arocc
tar -xzf %{SOURCE1} --strip-components=1 -C compositor/deps/pixman
tar -xzf %{SOURCE2} --strip-components=1 -C compositor/deps/wayland
tar -xzf %{SOURCE3} --strip-components=1 -C compositor/deps/wlroots
tar -xzf %{SOURCE4} --strip-components=1 -C compositor/deps/xkbcommon
tar -xzf %{SOURCE5} --strip-components=1 -C compositor/deps/translate-c
mkdir -p compositor/deps/wlroots-render-hook-license
tar -xzf %{SOURCE6} --strip-components=1 \
    -C compositor/deps/wlroots-render-hook-license \
    wlroots-0.20.2/LICENSE

%autopatch -p1

%build
cd compositor
export ZIG_GLOBAL_CACHE_DIR="${PWD}/.zig-global-cache"
export AQUEOUS_WLROOTS_CACHE_DIR="%{_sourcedir}"
scripts/build-wlroots-render-hook.sh
export PKG_CONFIG_PATH="${PWD}/.deps/wlroots-render-hook/lib/pkgconfig"
zig build \
    -Dcpu=baseline \
    -Doptimize=ReleaseSafe \
    -Dpie=true \
    -Dllvm=true \
    -Dxwayland=true \
    -Danimations=true \
    -Dexternal-policy=true \
    -Dman-pages=true \
    --prefix ../aqueous-dist \
    install

patchelf --set-rpath '$ORIGIN/../lib/aqueous' \
    ../aqueous-dist/bin/aqueous

%check
cd compositor
export ZIG_GLOBAL_CACHE_DIR="${PWD}/.zig-global-cache"
export PKG_CONFIG_PATH="${PWD}/.deps/wlroots-render-hook/lib/pkgconfig"
export LD_LIBRARY_PATH="${PWD}/.deps/wlroots-render-hook/lib"
zig build test \
    -Dcpu=baseline \
    -Doptimize=ReleaseSafe \
    -Dllvm=true \
    -Dxwayland=true \
    -Danimations=true \
    -Dexternal-policy=true

for path in \
    bin/aqueous \
    bin/aqueousctl \
    lib/aqueous/libwlroots-0.20.so \
    share/man/man1/aqueous.1 \
    share/man/man1/aqueousctl.1 \
    share/aqueous-protocols/stable/aqueous-window-info-v1.xml; do
    test -e "../aqueous-dist/${path}"
done

cmp ../aqueous-dist/lib/aqueous/libwlroots-0.20.so \
    .deps/wlroots-render-hook/lib/libwlroots-0.20.so
test "$(patchelf --print-rpath ../aqueous-dist/bin/aqueous)" = \
    '$ORIGIN/../lib/aqueous'
if readelf -d ../aqueous-dist/bin/aqueous | grep -qi scenefx; then
    echo "aqueous unexpectedly links SceneFX" >&2
    exit 1
fi

%install
install -Dpm0755 aqueous-dist/bin/aqueous %{buildroot}%{_bindir}/aqueous
install -Dpm0755 aqueous-dist/bin/aqueousctl %{buildroot}%{_bindir}/aqueousctl
install -Dpm0755 aqueous-dist/lib/aqueous/libwlroots-0.20.so \
    %{buildroot}%{_prefix}/lib/aqueous/libwlroots-0.20.so

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

install -Dpm0644 packaging/aqueous.tmpfiles \
    %{buildroot}%{_user_tmpfilesdir}/aqueous.conf
install -Dpm0644 packaging/udev/70-aqueous-uaccess.rules \
    %{buildroot}%{_udevrulesdir}/70-aqueous-uaccess.rules

install -d %{buildroot}%{_datadir}/aqueous/wallpapers
install -pm0644 packaging/wallpapers/*.avif \
    %{buildroot}%{_datadir}/aqueous/wallpapers/

install -Dpm0644 packaging/greetd/config.toml.example \
    %{buildroot}%{_docdir}/%{name}/greetd-config.toml.example
install -Dpm0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -d %{buildroot}%{_licensedir}/%{name}/compositor
install -pm0644 compositor/LICENSES/* \
    %{buildroot}%{_licensedir}/%{name}/compositor/
install -Dpm0644 compositor/deps/wlroots-render-hook-license/LICENSE \
    %{buildroot}%{_licensedir}/%{name}/wlroots/LICENSE
install -d %{buildroot}%{_licensedir}/%{name}/arocc
install -pm0644 compositor/deps/arocc/LICENSE* \
    %{buildroot}%{_licensedir}/%{name}/arocc/

%post
%systemd_user_post aqueous-session.target

%preun
%systemd_user_preun aqueous-session.target

%postun
%systemd_user_postun aqueous-session.target

%files
%license %{_licensedir}/%{name}/arocc/LICENSE*
%license %{_licensedir}/%{name}/compositor/*
%license %{_licensedir}/%{name}/wlroots/LICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/greetd-config.toml.example
%{_bindir}/aqueous
%{_bindir}/aqueousctl
%{_bindir}/aqueous-init
%{_bindir}/aqueous-wm
%{_prefix}/lib/aqueous/libwlroots-0.20.so
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
%{_user_tmpfilesdir}/aqueous.conf
%{_udevrulesdir}/70-aqueous-uaccess.rules

%changelog
%autochangelog
