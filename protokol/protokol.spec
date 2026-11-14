%global debug_package %{nil}
%global __strip /bin/true
%global SHA256SUM_x64 0aea2de4a316f70f73cf909df82b35e73f6b1a0d5051571d516e202165452cd8
%global SHA256SUM_arm64 56c6a74a9ca0c7be12e4cdcdd3dacea0626c354d9eb17f9a8ed0e9967d5b8c97
%ifarch x86_64
%global source_file %{SOURCE0}
%global source_sha256 %{SHA256SUM_x64}
%else
%global source_file %{SOURCE1}
%global source_sha256 %{SHA256SUM_arm64}
%endif

Name:           protokol
Version:        0.6.9.142
Release:        1%{?dist}
Summary:        MIDI, OSC, Art-Net and gamepad protocol monitor

# Proprietary freeware; redistribution approved by Hexler support.
License:        LicenseRef-Proprietary
URL:            https://hexler.net/protokol
Source0:        https://downloads.hexler.net/protokol/%{name}-%{version}-linux-x64.deb
Source1:        https://downloads.hexler.net/protokol/%{name}-%{version}-linux-arm64.deb
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
