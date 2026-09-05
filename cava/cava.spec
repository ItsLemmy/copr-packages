Name:           cava
Version:        1.0.0
Release:        1%{?dist}
Summary:        Cross-platform Audio Visualizer

License:        MIT
URL:            https://github.com/karlstav/cava
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  fftw-devel
BuildRequires:  ncurses-devel
BuildRequires:  iniparser-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pipewire-devel
BuildRequires:  portaudio-devel

%description
CAVA is a bar spectrum audio visualizer for terminal or desktop (SDL).
It works on Linux, FreeBSD, macOS, and Windows.

%prep
%autosetup -n %{name}-%{version} -p1

%build
./autogen.sh
%configure
%make_build

%install
%make_install

%files
%license LICENSE
%doc README.md
%{_bindir}/cava
%{_datadir}/consolefonts/cava.psf

%changelog
%autochangelog
