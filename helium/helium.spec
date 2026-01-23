Name:           helium
Version:        0.8.3.1
Release:        1%{?dist}
Summary:        Helium Browser - Privacy-focused Chromium fork

License:        GPL-3.0
URL:            https://github.com/imputnet/helium
Source0:        https://github.com/imputnet/helium-linux/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz

ExclusiveArch:  x86_64

Requires:       desktop-file-utils
Requires:       gtk3
Requires:       libX11
Requires:       libdrm
Requires:       mesa-libGL

# Disable debug package
%define debug_package %{nil}
%define __strip /bin/true

%description
Helium Browser – A fast, privacy-focused Chromium fork based on ungoogled-chromium.
Best privacy by default, unbiased ad-blocking, no bloat and no noise.

%prep
%setup -q -n helium-%{version}-x86_64_linux

%build


%install
# Create directories
mkdir -p %{buildroot}/usr/share/helium
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps

# Copy all extracted files to /usr/share/helium
cp -r * %{buildroot}/usr/share/helium/

# Find and link the main executable
# The executable might be named 'helium' or 'chrome' in the extracted files
if [ -f chrome ]; then
    cp chrome %{buildroot}/usr/share/helium/
    ln -sf /usr/share/helium/chrome %{buildroot}/usr/bin/helium
elif [ -f helium ]; then
    cp helium %{buildroot}/usr/share/helium/
    ln -sf /usr/share/helium/helium %{buildroot}/usr/bin/helium
fi

# Create desktop file
cat > %{buildroot}/usr/share/applications/helium.desktop << EOF
[Desktop Entry]
Version=1.0
Name=Helium Browser
Comment=Privacy-focused Chromium fork
Exec=/usr/bin/helium %U
Icon=helium
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;video/webm;application/x-xpinstall;
Actions=new-window;new-private-window;

[Desktop Action new-window]
Name=New Window
Exec=/usr/bin/helium

[Desktop Action new-private-window]
Name=New Private Window
Exec=/usr/bin/helium --incognito
EOF

# Use the product logo as icon
if [ -f product_logo_256.png ]; then
    cp product_logo_256.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/helium.png
else
    # Create a simple placeholder icon if logo not found
    touch %{buildroot}/usr/share/icons/hicolor/256x256/apps/helium.png
fi

%files
/usr/share/helium/
/usr/bin/helium
/usr/share/applications/helium.desktop
/usr/share/icons/hicolor/256x256/apps/helium.png

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%changelog
* Mon Jan 05 2026 Lemmy <studio@quadbyte.net> - 0.7.9.1
- Update to 0.7.9.1

* Wed Dec 31 2025 Lemmy <studio@quadbyte.net> - 0.7.7.1
- Initial package using extracted tar.xz binaries
