%global debug_package %{nil}
%global __strip /bin/true
%global SHA256SUM_x64 79b35b62c5b25c3fa20c782d76b9049dd1db33647fa182b3d54f6e7fb8b20ae2
%global SHA256SUM_arm64 fed369f6be3cf46bcfaf4704992e5bb29484d344404bc6b0450d0f232717e3b0
%ifarch x86_64
%global source_file %{SOURCE0}
%global source_sha256 %{SHA256SUM_x64}
%else
%global source_file %{SOURCE1}
%global source_sha256 %{SHA256SUM_arm64}
%endif

Name:           protokol
Version:        0.6.8.141
Release:        2%{?dist}
Summary:        MIDI, OSC, Art-Net and gamepad protocol monitor

# Proprietary freeware; redistribution approved by Hexler support.
License:        LicenseRef-Proprietary
URL:            https://hexler.net/protokol
Source0:        https://hexler.net/pub/protokol/%{name}-%{version}-linux-x64.deb
Source1:        https://hexler.net/pub/protokol/%{name}-%{version}-linux-arm64.deb
ExclusiveArch:  x86_64 aarch64

BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  desktop-file-utils
Requires:       alsa-lib
Requires:       avahi-libs
Requires:       zenity
Recommends:     hicolor-icon-theme

%description
Protokol is Hexler's control protocol test utility for monitoring MIDI, OSC,
Art-Net and gamepad input streams. This package installs the unmodified
upstream prebuilt executable with its application launcher and icons.

%prep
%setup -q -c -T
echo '%{source_sha256}  %{source_file}' | sha256sum -c -
ar p %{source_file} data.tar.gz | tar -xz

%build

%install
install -Dpm 0755 opt/protokol/Protokol %{buildroot}%{_bindir}/protokol
install -Dpm 0644 usr/share/applications/protokol.desktop %{buildroot}%{_datadir}/applications/protokol.desktop
desktop-file-edit --set-key=Exec --set-value=protokol %{buildroot}%{_datadir}/applications/protokol.desktop
for size in 16 32 48 128 256; do
    install -Dpm 0644 usr/share/icons/hicolor/${size}x${size}/apps/protokol.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/protokol.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/protokol.desktop

%files
%{_bindir}/protokol
%{_datadir}/applications/protokol.desktop
%{_datadir}/icons/hicolor/*/apps/protokol.png

%changelog
%autochangelog
