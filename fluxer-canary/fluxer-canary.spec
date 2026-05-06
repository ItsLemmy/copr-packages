%global debug_package %{nil}
%global __strip /bin/true
%global __os_install_post %{nil}
%global _build_id_links none

%global SHA256SUM0 @SHA256SUM0@

%global appdir %{_prefix}/lib/%{name}

Name:           fluxer-canary
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Instant messaging and VoIP application (canary build)

License:        AGPL-3.0-or-later
URL:            https://fluxer.app
Source0:        https://api.fluxer.app/dl/desktop/canary/linux/x64/%{version}/tar_gz#/fluxer-canary-%{version}-x64.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils

Requires:       gtk3
Requires:       nss
Requires:       alsa-lib
Requires:       libnotify
Requires:       libXtst
Requires:       libXScrnSaver
Requires:       libsecret
Requires:       libappindicator-gtk3

%description
Fluxer is an open-source, independent instant messaging and VoIP platform
built for friends, groups, and communities. This package provides the
canary (development) channel build of the desktop application.

%prep
echo "%{SHA256SUM0}  %{SOURCE0}" | sha256sum -c -
%setup -q -c -n %{name}-%{version}
mv "Fluxer Canary-%{version}-linux-x64"/* .
mv "Fluxer Canary-%{version}-linux-x64"/.[!.]* . 2>/dev/null || :
rmdir "Fluxer Canary-%{version}-linux-x64"

%build
cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Name=Fluxer Canary
Exec=%{name} %U
Terminal=false
Type=Application
Icon=%{name}
StartupWMClass=fluxer-canary
Comment=Instant messaging and VoIP application
Categories=Network;InstantMessaging;
EOF

%install
install -d %{buildroot}%{appdir}
cp -a . %{buildroot}%{appdir}/

# Drop bundled native modules for foreign architectures so we don't
# pull in cross-arch ld-linux Requires.
find %{buildroot}%{appdir} -name '*_arm64_*.node' -delete

install -d %{buildroot}%{_bindir}
ln -sr %{buildroot}%{appdir}/%{name} %{buildroot}%{_bindir}/%{name}

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{name}.desktop

for size in 16 24 32 48 64 128 256 512; do
    install -Dm644 resources/icons/${size}x${size}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

%post
# Chrome sandbox needs SUID only on kernels without working user namespaces.
if ! { [ -L /proc/self/ns/user ] && unshare --user true >/dev/null 2>&1; }; then
    chmod 4755 %{appdir}/chrome-sandbox || :
else
    chmod 0755 %{appdir}/chrome-sandbox || :
fi

%files
%license LICENSE.electron.txt
%dir %{appdir}
%{appdir}/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
%autochangelog
