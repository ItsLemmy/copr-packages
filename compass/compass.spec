%global debug_package %{nil}
%global __strip /bin/true
%global SHA256SUM 4ead61e177cb123cf9d573ec341ef93ea09f391162ef15ce43b7ce7a692c2e37

Name:           compass
Version:        20261122.1521
Release:        1%{?dist}
Summary:        Chromium browser with a sidebar of spaces and account-free sync
License:        BSD-3-Clause
URL:            https://github.com/Compass-Browser/Compass
Source0:        %{url}/releases/download/v%{version}/Compass-%{version}-linux-x64.tar.xz
Source1:        https://raw.githubusercontent.com/Compass-Browser/Compass/v%{version}/LICENSE
ExclusiveArch:  x86_64
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  desktop-file-utils
BuildRequires:  findutils
Requires:       gtk3
Requires:       nss
Requires:       nspr
Requires:       alsa-lib
Requires:       cups-libs
Requires:       libsecret
Requires:       xdg-utils
Recommends:     vulkan-loader
Recommends:     hicolor-icon-theme

%description
Compass is an open-source Arc alternative built on Chromium: a sidebar of
spaces, pinned tabs and folders, and end-to-end encrypted sync that needs no
account. This package installs the upstream Linux binary, including
prereleases, without disabling Chromium's sandbox.

%prep
%setup -q -c -T
echo '%{SHA256SUM}  %{SOURCE0}' | sha256sum -c -
tar -xJf %{SOURCE0} --strip-components=1
cp %{SOURCE1} .

%build

%install
mkdir -p %{buildroot}/usr/lib/compass %{buildroot}%{_bindir}
cp -a . %{buildroot}/usr/lib/compass/
rm %{buildroot}/usr/lib/compass/{LICENSE,README,compass.desktop}
ln -s /usr/lib/compass/compass %{buildroot}%{_bindir}/compass
install -Dm644 compass.desktop %{buildroot}%{_datadir}/applications/compass.desktop
for size in 16 24 32 48 64 128 256; do
    install -Dm644 product_logo_$size.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/compass.png
done
chmod 4755 %{buildroot}/usr/lib/compass/chrome-sandbox
find %{buildroot}/usr/lib/compass -mindepth 1 ! -path '*/chrome-sandbox' \
    -printf '/usr/lib/compass/%%P\n' | while read -r path; do
    if [ -d "%{buildroot}$path" ]; then echo "%%dir $path"; else echo "$path"; fi
done > compass.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/compass.desktop

%files -f compass.files
%license LICENSE
%doc README
%{_bindir}/compass
%dir /usr/lib/compass
%attr(4755,root,root) /usr/lib/compass/chrome-sandbox
%{_datadir}/applications/compass.desktop
%{_datadir}/icons/hicolor/*/apps/compass.png

%changelog
%autochangelog
