%global debug_package %{nil}
%global __strip /bin/true
# Bundled Electron, Vulkan and Tor libraries must not satisfy or demand system sonames.
%global __provides_exclude_from ^/usr/lib/acira-browser/.*$
%global __requires_exclude ^lib(ffmpeg|vk_swiftshader|vulkan|ssl|crypto|event-2\\.1)\\.so
%global upstream_version 0.1.0-beta.14.6
%global upstream_tag v0.1.0-beta.14.6-linux-04fd9323
%global SHA256SUM acd7f7be08a838f9029ddb5a96748cc29be119c90d6ffa2f0d9dee0f356e660a
%global SETUP_SHA256SUM cf19a643d7a3faac3943a85c1bbdab7d8c493932c2b76fcf216c6fe0a8b6e2b5

Name:           acira-browser
Version:        0.1.0~beta.14.6
Release:        1%{?dist}
Summary:        Calm Electron browser with private and Tor tabs, workspaces and ad blocking
License:        AGPL-3.0-only AND GPL-3.0-only AND MPL-2.0 AND MIT AND BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND ISC AND CC-BY-3.0
URL:            https://acirabrowser.com
Source0:        https://github.com/Acira-dev/AciraBrowserUpdates/releases/download/%{upstream_tag}/AciraBrowser-%{upstream_version}-linux-x86_64.AppImage
Source1:        https://github.com/Acira-dev/AciraBrowserUpdates/releases/download/%{upstream_tag}/AciraBrowser-Linux-SetupFiles.zip
ExclusiveArch:  x86_64
BuildRequires:  unzip
BuildRequires:  desktop-file-utils
BuildRequires:  findutils
Requires:       gtk3
Requires:       nss
Requires:       nspr
Requires:       alsa-lib
Requires:       cups-libs
Requires:       libsecret
Requires:       xdg-utils
Requires:       polkit
Recommends:     hicolor-icon-theme

%description
Acira is an independent desktop browser built on Electron/Chromium with
private and Tor tabs, workspaces and built-in ad blocking. This package
installs the upstream Linux AppImage contents, including beta releases,
with its desktop entry, icon and password reauthentication policy, without
disabling Chromium's sandbox. Acira's self-updater is inactive outside the
AppImage; updates arrive through DNF.

%prep
%setup -q -c -T
echo '%{SHA256SUM}  %{SOURCE0}' | sha256sum -c -
echo '%{SETUP_SHA256SUM}  %{SOURCE1}' | sha256sum -c -
install -m755 %{SOURCE0} acira.AppImage
./acira.AppImage --appimage-extract >/dev/null
rm acira.AppImage
unzip -q %{SOURCE1} -d setup

%build

%install
cd squashfs-root
mkdir -p %{buildroot}/usr/lib/acira-browser %{buildroot}%{_bindir}
# AppRun, its bundled usr/lib copies of system libraries and AppImage metadata are not needed outside the AppImage.
cp -a $(ls -A | grep -vxE 'AppRun|usr|\.DirIcon|AciraBrowser\.png|acira-browser\.desktop') \
    %{buildroot}/usr/lib/acira-browser/
ln -s /usr/lib/acira-browser/AciraBrowser %{buildroot}%{_bindir}/acira-browser
sed -i -e 's|^Exec=AppRun --no-sandbox|Exec=acira-browser|' -e 's|^Icon=AciraBrowser$|Icon=acira-browser|' \
    -e '/^X-AppImage-Version=/d' acira-browser.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications --add-category=WebBrowser acira-browser.desktop
install -Dm644 usr/share/icons/hicolor/512x512/apps/AciraBrowser.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/acira-browser.png
install -Dm644 ../setup/computer.acira.browser.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/computer.acira.browser.policy
# The AppImage ships 0700 directories (resources, locales); users must be able to read them.
chmod -R go+rX %{buildroot}/usr/lib/acira-browser
chmod 4755 %{buildroot}/usr/lib/acira-browser/chrome-sandbox
find %{buildroot}/usr/lib/acira-browser -mindepth 1 ! -path '*/chrome-sandbox' \
    -printf '/usr/lib/acira-browser/%%P\n' | while read -r path; do
    if [ -d "%{buildroot}$path" ]; then echo "%%dir $path"; else echo "$path"; fi
done > ../acira-browser.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/acira-browser.desktop
grep -qx 'Exec=acira-browser --acira-new-private-window' %{buildroot}%{_datadir}/applications/acira-browser.desktop

%files -f acira-browser.files
%license setup/LICENSE setup/THIRD_PARTY_NOTICES.md
%{_bindir}/acira-browser
%dir /usr/lib/acira-browser
%attr(4755,root,root) /usr/lib/acira-browser/chrome-sandbox
%{_datadir}/applications/acira-browser.desktop
%{_datadir}/icons/hicolor/512x512/apps/acira-browser.png
%{_datadir}/polkit-1/actions/computer.acira.browser.policy

%changelog
%autochangelog
