Name:           noctalia-greeter-git
Version:        @VERSION@
Release:        1%{?dist}
Summary:        A minimal login greeter for greetd that matches the look and feel of Noctalia Shell

# Vendored Wuffs (third_party/wuffs) is Apache-2.0
License:        MIT AND Apache-2.0
URL:            https://github.com/noctalia-dev/noctalia-greeter
Source0:        %{url}/archive/@COMMIT@.tar.gz#/noctalia-greeter-@COMMIT@.tar.gz

ExclusiveArch:  aarch64 x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  stb_image_resize2-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wlroots-0.20)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  /usr/bin/wayland-scanner
BuildRequires:  systemd-rpm-macros

Requires:       greetd
Requires:       dbus-daemon
Recommends:     polkit
Provides:       noctalia-greeter = %{version}-%{release}
Provides:       bundled(wuffs)
Conflicts:      noctalia-greeter

%description
A minimal login greeter for greetd that matches the look and feel of Noctalia
Shell. Ships its own wlroots-based kiosk compositor.

Point greetd at it in /etc/greetd/config.toml:

  [default_session]
  command = "/usr/bin/noctalia-greeter-session"
  user = "greetd"

%prep
%autosetup -n noctalia-greeter-@COMMIT@
# Fedora's greetd package runs the greeter as the "greetd" user
sed -i 's/ greeter greeter / greetd greetd /' data/tmpfiles.d/noctalia-greeter.conf

%build
# meson.build's default c_args would otherwise drop Fedora's hardening CFLAGS (-fPIE)
%meson -Dc_args="%{build_cflags} -Wno-error=switch"
%meson_build

%install
%meson_install

%post
%tmpfiles_create noctalia-greeter.conf

%files
%license LICENSE assets/fonts/tabler-icons-license.txt
%doc README.md PACKAGING.md docs/user examples/greeter.toml
%{_bindir}/noctalia-greeter
%{_bindir}/noctalia-greeter-apply-appearance
%{_bindir}/noctalia-greeter-compositor
%{_bindir}/noctalia-greeter-print-greetd-config
%{_bindir}/noctalia-greeter-session
%{_bindir}/noctalia-greeter-xsession
%{_datadir}/noctalia-greeter/
%{_datadir}/polkit-1/actions/org.noctalia.greeter.apply-appearance.policy
%{_tmpfilesdir}/noctalia-greeter.conf

%changelog
%autochangelog
