%global debug_package %{nil}
%global __strip /bin/true
%global upstream_version 0.2.49-nightly.1
%global SHA256SUM 5897d54fac7ed7a5098ead5280b37ec4362cbeab28e8479f48e66efd5ba87bdb

Name:           ardia
Version:        0.2.49~nightly.1
Release:        1%{?dist}
Summary:        Chromium browser with a sidebar and built-in ad blocking
License:        GPL-3.0-only AND Apache-2.0 AND BSD-3-Clause AND MIT
URL:            https://github.com/ardia-browser/ardia
Source0:        %{url}/releases/download/v%{upstream_version}/Ardia-%{upstream_version}-linux-x64.deb
Source1:        https://raw.githubusercontent.com/ardia-browser/ardia/v%{upstream_version}/LICENSE
Source2:        https://raw.githubusercontent.com/ardia-browser/ardia/v%{upstream_version}/LICENSE.Apache-2.0
Source3:        https://raw.githubusercontent.com/ardia-browser/ardia/v%{upstream_version}/NOTICE
ExclusiveArch:  x86_64
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  desktop-file-utils
BuildRequires:  findutils
Requires:       bash
Requires:       coreutils
Requires:       util-linux
Requires:       grep
Requires:       gtk3
Requires:       nss
Requires:       nspr
Requires:       alsa-lib
Requires:       cups-libs
Requires:       libsecret
Requires:       xdg-utils
Requires:       polkit
Recommends:     vulkan-loader
Recommends:     hicolor-icon-theme

%description
Ardia combines a sidebar interface, split views and built-in ad and tracker
blocking with a Chromium engine. This package installs the upstream Linux
binary, including nightly releases, without disabling Chromium's sandbox.

%prep
%setup -q -c -T
echo '%{SHA256SUM}  %{SOURCE0}' | sha256sum -c -
ar p %{SOURCE0} data.tar.xz | tar -xJ
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build

%install
mkdir -p %{buildroot}%{_prefix}
cp -a usr/lib usr/bin usr/share %{buildroot}%{_prefix}/
# AppArmor integration is Debian-specific; Fedora uses SELinux.
rm -r %{buildroot}%{_datadir}/ardia/apparmor
rmdir %{buildroot}%{_datadir}/ardia
chmod 4755 %{buildroot}/usr/lib/ardia/chrome-sandbox
find %{buildroot}/usr/lib/ardia -mindepth 1 ! -path '*/chrome-sandbox' \
    -printf '/usr/lib/ardia/%%P\n' | while read -r path; do
    if [ -d "%{buildroot}$path" ]; then echo "%%dir $path"; else echo "$path"; fi
done > ardia.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/ardia.desktop

%files -f ardia.files
%license LICENSE LICENSE.Apache-2.0 NOTICE
%doc %{_docdir}/%{name}/
%{_bindir}/ardia
%dir /usr/lib/ardia
%attr(4755,root,root) /usr/lib/ardia/chrome-sandbox
%{_datadir}/applications/ardia.desktop
%{_datadir}/icons/hicolor/256x256/apps/ardia.png
%{_datadir}/polkit-1/actions/dev.ardia.linux.policy

%changelog
%autochangelog
