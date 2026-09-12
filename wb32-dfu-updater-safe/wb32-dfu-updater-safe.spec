Name:           wb32-dfu-updater-safe
Version:        1.0.0
Release:        2%{?dist}
Summary:        Read-protection-safe USB firmware updater for WB32 chips

License:        Apache-2.0
URL:            https://github.com/WestberryTech/wb32-dfu-updater
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/wb32-dfu-updater-%{version}.tar.gz
Source1:        60-wb32-dfu-updater.rules
Patch0:          0001-refuse-read-protection-removal.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libusb-1.0) >= 1.0.0
Requires:       udev
Conflicts:      wb32-dfu-updater

%description
A command-line USB firmware updater for WB32 chips. Unlike the upstream
utility, this build refuses to disable MCU read protection. It installs a udev
rule that grants the active local user access to WB32 DFU devices.

%prep
%autosetup -n wb32-dfu-updater-%{version} -p1

%build
%cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5
%cmake_build

%install
%cmake_install
install -Dpm 0644 %{SOURCE1} %{buildroot}/usr/lib/udev/rules.d/60-wb32-dfu-updater.rules

%files
%license LICENSE
%doc README.md
%{_bindir}/wb32-dfu-updater_cli
/usr/lib/udev/rules.d/60-wb32-dfu-updater.rules

%changelog
%autochangelog
