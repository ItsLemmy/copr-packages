Name:           phinger-cursors
Version:        2.1
Release:        1%{?dist}
Summary:        Most likely the most over engineered cursor theme

License:        CC-BY-SA-4.0
URL:            https://github.com/phisch/phinger-cursors
Source:         %{url}/releases/download/v%{version}/phinger-cursors-variants.tar.bz2

BuildArch:      noarch

%global _description %{expand:
Phinger cursors is a cursor theme for Linux desktop environments supporting
X11 and Wayland. It includes four variants: dark, light, dark-left, and
light-left, with cursor sizes of 24, 32, 48, 64, 96, and 128 pixels.}

%description %{_description}

%prep
%autosetup -c

%install
mkdir -p %{buildroot}%{_datadir}/icons
cp -a phinger-cursors-* %{buildroot}%{_datadir}/icons/

%files
%{_datadir}/icons/phinger-cursors-*

%changelog
%autochangelog
