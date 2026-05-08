Name:           gradia
Version:        1.13.0
Release:        1%{?dist}
Summary:        Make your screenshots ready for the world

License:        GPL-3.0-only
URL:            https://github.com/AlexanderVanhee/Gradia
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Patch0:         gradia_ocr.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  blueprint-compiler
BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libportal-devel
BuildRequires:  gtksourceview5-devel

Requires:       python3
Requires:       python3-gobject
Requires:       python3-pillow
Requires:       python3-cairo
Requires:       python3-pytesseract
Requires:       gtk4
Requires:       libadwaita
Requires:       libportal
Requires:       gtksourceview5
Requires:       dconf
Requires:       graphene
Requires:       libsoup3
Requires:       hicolor-icon-theme
Requires:       pango
Requires:       gdk-pixbuf2
Requires:       glib2

Recommends:     xdg-desktop-portal

%global _description %{expand:
Gradia is a GNOME application that helps you quickly edit and enhance
screenshots for sharing. It handles transparency, sizing, and overall
appearance to make your screenshots ready for the world.}

%description %{_description}

%prep
%autosetup -n Gradia-%{version} -p1

%build
%meson -Docr_tesseract_cmd=%{_bindir}/tesseract -Docr_original_tessdata_dir=%{_datadir}/tessdata
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop || :
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml || :

%files
%license COPYING
%doc README.md
%{_bindir}/gradia
%{_datadir}/applications/*.desktop
%{_datadir}/gradia/
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.metainfo.xml
%{_datadir}/locale/
%{_datadir}/fonts/Caveat-VariableFont_wght.ttf
%{_datadir}/fonts/LICENSE-OFL.txt

%changelog
%autochangelog
