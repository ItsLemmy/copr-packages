%global         appid dev.faetalize.waytator
%global         SHA256SUM0 834d7af698b579d357dc0a6511aaa28c5bb9a99293edf03c3a5590973bb6d9e9

Name:           waytator
Version:        1.2.4
Release:        1%{?dist}
Summary:        Screenshot annotator and lightweight image editor

License:        GPL-3.0-or-later
URL:            https://github.com/faetalize/waytator
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
