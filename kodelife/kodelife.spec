%global debug_package %{nil}
%global __strip /bin/true
%global SHA256SUM_x64 2f119fbf1c48f402eb0a55a37795d40b1ce448030cd82c47bd7d748ce1785156
%global SHA256SUM_arm64 14b276a59c94cf63d3bb381a86acf20c685e98ee0da165c2dcf78123b54d7772
%ifarch x86_64
%global source_file %{SOURCE0}
%global source_sha256 %{SHA256SUM_x64}
%else
%global source_file %{SOURCE1}
%global source_sha256 %{SHA256SUM_arm64}
%endif

Name:           kodelife
Version:        1.2.9.212
Release:        1%{?dist}
Summary:        Real-time GPU shader editor

# Proprietary software; redistribution approved by Hexler support.
License:        LicenseRef-Proprietary
URL:            https://hexler.net/kodelife
# Both payloads must be present regardless of the source builder's architecture.
Source0:        https://hexler.net/pub/kodelife/%{name}-%{version}-linux-x64.deb
Source1:        https://hexler.net/pub/kodelife/%{name}-%{version}-linux-arm64.deb
ExclusiveArch:  x86_64 aarch64

BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  desktop-file-utils
BuildRequires:  shared-mime-info
Requires:       alsa-lib
Requires:       avahi-libs
Requires:       zenity
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Recommends:     hicolor-icon-theme
Recommends:     gstreamer1-plugins-good

%description
KodeLife is Hexler's real-time GPU shader editor for live coding and
prototyping visual effects. This package installs the unmodified upstream
prebuilt executable with its application launcher, icons and project MIME
type. KodeLife is proprietary commercial software; this package does not
include a license key. See https://hexler.net/kodelife/eula for license terms.

%prep
%setup -q -c -T
echo '%{source_sha256}  %{source_file}' | sha256sum -c -
ar p %{source_file} data.tar.gz | tar -xz

%build

%install
install -Dpm 0755 opt/kodelife/KodeLife %{buildroot}%{_bindir}/kodelife
install -Dpm 0644 usr/share/applications/kodelife.desktop %{buildroot}%{_datadir}/applications/kodelife.desktop
desktop-file-edit --set-key=Exec --set-value='kodelife %%F' %{buildroot}%{_datadir}/applications/kodelife.desktop
install -Dpm 0644 usr/share/mime/packages/kodelife.xml %{buildroot}%{_datadir}/mime/packages/kodelife.xml
for size in 16 32 48 128 256; do
    install -Dpm 0644 usr/share/icons/hicolor/${size}x${size}/apps/kodelife.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/kodelife.png
    install -Dpm 0644 usr/share/icons/hicolor/${size}x${size}/mimetypes/application-x-kodelife-project.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/mimetypes/application-x-kodelife-project.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/kodelife.desktop
mkdir -p mime-check/packages
cp %{buildroot}%{_datadir}/mime/packages/kodelife.xml mime-check/packages/
update-mime-database mime-check

%files
%{_bindir}/kodelife
%{_datadir}/applications/kodelife.desktop
%{_datadir}/icons/hicolor/*/apps/kodelife.png
%{_datadir}/icons/hicolor/*/mimetypes/application-x-kodelife-project.png
%{_datadir}/mime/packages/kodelife.xml

%changelog
%autochangelog
