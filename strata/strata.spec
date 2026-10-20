%global debug_package %{nil}
%global __strip /bin/true
%global triple x86_64-unknown-linux-gnu
%global upstream_version 1.1.0-rc.2

Name:           strata
Version:        1.1.0~rc.2
Release:        1%{?dist}
Summary:        Fast, keyboard-first GTK4 file manager with Miller columns

# Strata itself is MIT; the bundled UnRAR code carries the UnRAR license
License:        MIT AND LicenseRef-UnRAR
URL:            https://github.com/lgse/strata
Source0:        %{url}/releases/download/v%{upstream_version}/%{name}-%{upstream_version}-%{triple}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils

Requires:       gtk4 >= 4.12
Requires:       gtksourceview5
Requires:       poppler-glib
Requires:       fontconfig
Requires:       bubblewrap
Requires:       gstreamer1-plugins-good
Requires:       ffmpegthumbnailer
Requires:       /usr/bin/ffmpeg
Requires:       gvfs
Recommends:     gvfs-smb
Recommends:     hicolor-icon-theme

%description
Strata is a fast, keyboard-first file manager for Linux built with Rust and
GTK4. It combines Miller-column navigation with icon and list views, recursive
fuzzy search, and rich previews for images, RAW photos, PDFs, code, audio and
video. Native parsers for untrusted files run in Bubblewrap sandboxes. Remote
locations are browsed through GIO/GVfs.

This package installs the upstream prebuilt release binary. It does not
register Strata as the default file manager or system file chooser.

%prep
%setup -q -n %{name}-%{upstream_version}-%{triple}

%build

%install
install -Dpm 0755 %{name} -t %{buildroot}%{_bindir}/
install -Dpm 0644 io.github.lgse.Strata.desktop -t %{buildroot}%{_datadir}/applications/
install -Dpm 0644 io.github.lgse.Strata.svg -t %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.lgse.Strata.desktop

%files
%license LICENSE UnRAR.txt THIRD_PARTY_LICENSES.md
%doc README.md docs/portal-file-chooser.md
%{_bindir}/strata
%{_datadir}/applications/io.github.lgse.Strata.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg

%post
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :

%changelog
%autochangelog
