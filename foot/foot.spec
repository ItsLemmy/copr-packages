Name:           foot
Version:        1.26.0
Release:        1%{?dist}
Summary:        Fast, lightweight and minimalistic Wayland terminal emulator

License:        MIT
URL:            https://codeberg.org/dnkl/foot
Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  meson >= 0.58
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  scdoc

BuildRequires:  pkgconfig(fcft) >= 3.0.0
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(tllist) >= 1.1.0
BuildRequires:  pkgconfig(libutf8proc)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

BuildRequires:  ncurses
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros

Requires:       ncurses-base

%description
Foot is a fast, lightweight and minimalistic Wayland terminal emulator.
Features include sixel image support, scrollback search, font
configuration with fallback, DPI awareness, and more.

%package        terminfo
Summary:        Terminfo files for %{name}
BuildArch:      noarch

%description    terminfo
This package contains the terminfo files for the foot terminal emulator.

%prep
%autosetup -n %{name} -p1

%build
%meson -Dwerror=false
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/foot.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/footclient.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/foot-server.desktop

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_docdir}/foot/LICENSE
%{_bindir}/foot
%{_bindir}/footclient
%dir %{_sysconfdir}/xdg/foot
%config(noreplace) %{_sysconfdir}/xdg/foot/foot.ini
%{_datadir}/applications/foot.desktop
%{_datadir}/applications/footclient.desktop
%{_datadir}/applications/foot-server.desktop
%{_datadir}/icons/hicolor/48x48/apps/foot.png
%{_datadir}/icons/hicolor/scalable/apps/foot.svg
%{_datadir}/foot/
%{_datadir}/bash-completion/completions/foot
%{_datadir}/bash-completion/completions/footclient
%{_datadir}/fish/vendor_completions.d/foot.fish
%{_datadir}/fish/vendor_completions.d/footclient.fish
%{_datadir}/zsh/site-functions/_foot
%{_datadir}/zsh/site-functions/_footclient
%{_mandir}/man1/foot.1*
%{_mandir}/man1/footclient.1*
%{_mandir}/man5/foot.ini.5*
%{_mandir}/man7/foot-ctlseqs.7*

%files terminfo
%{_datadir}/terminfo/f/foot
%{_datadir}/terminfo/f/foot-direct

%changelog
%autochangelog
