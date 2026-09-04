Name:           swash
Version:        1.5.1
Release:        1%{?dist}
Summary:        Screenshot annotator and lightweight image editor

License:        GPL-3.0-or-later
URL:            https://github.com/ItsLemmy/swash
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/swash-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Recommends:     tesseract

%description
Swash is a fast screenshot annotator and lightweight image editor for Linux,
built with GTK 4 and libadwaita. It supports drawing, shapes, text, image
cropping and transformations, and optional OCR through Tesseract.

%prep
%autosetup -n %{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install
desktop-file-validate %{buildroot}%{_datadir}/applications/dev.lemmy.swash.desktop

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_bindir}/swash
%{_datadir}/applications/dev.lemmy.swash.desktop
%{_datadir}/icons/hicolor/*/apps/dev.lemmy.swash.png

%changelog
%autochangelog
