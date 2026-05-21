%global         appid dev.faetalize.waytator
%global         SHA256SUM0 ffe12c551ad806c1a5510bcebd709ad4fe37eb31f044cd41d319ff3d3c0473ac

Name:           waytator
Version:        1.3.1
Release:        1%{?dist}
Summary:        Screenshot annotator and lightweight image editor

License:        GPL-3.0-or-later
URL:            https://github.com/ItsLemmy/waytator
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.6

Recommends:     tesseract
Recommends:     wl-clipboard

%description
Waytator is a screenshot annotator and lightweight image editor for Wayland.
It supports reading images from stdin, opening existing files, and includes
optional OCR capabilities via Tesseract.

%prep
echo "%SHA256SUM0 %{SOURCE0}" | sha256sum -c -
%autosetup -n %{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/waytator
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{appid}.png
%{_datadir}/icons/hicolor/256x256/apps/%{appid}.png
%{_datadir}/icons/hicolor/512x512/apps/%{appid}.png

%changelog
%autochangelog
