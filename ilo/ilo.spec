%global debug_package %{nil}
%global __strip /bin/true
# Bundled Chromium, ANGLE/SwiftShader, Vulkan and optional Qt shim libraries must not satisfy or demand system sonames.
%global __provides_exclude_from ^/usr/lib/ilo/.*$
%global __requires_exclude ^lib(Browser|EGL|GLESv2|Qt5|Qt6|qt5_shim|qt6_shim|vk_swiftshader|vulkan).*\\.so
%global SHA256SUM f7beeffee774c175c54ca700a3f14f27bb3cd37b23ca405e1f95f3246a025a31

Name:           ilo
Version:        0.3.0
Release:        1%{?dist}
Summary:        Open-source Chromium browser with a GPUI sidebar, Spaces and MCP agent support
License:        GPL-3.0-or-later AND Apache-2.0 AND BSD-3-Clause AND MIT AND ISC AND MPL-2.0 AND Unicode-3.0 AND Zlib AND OFL-1.1
URL:            https://ilobrowser.com
Source0:        https://github.com/MartinPTielemans/ilo/releases/download/v%{version}/ilo-linux-x86_64.flatpak
ExclusiveArch:  x86_64
BuildRequires:  flatpak
BuildRequires:  ostree-libs
BuildRequires:  python3-gobject-base
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
ilo is an open-source web browser built on ungoogled-chromium with a GPUI
interface: a sidebar of Spaces, pinned and today's tabs, split views, a
command bar, built-in uBlock Origin ad blocking, and an MCP server so AI
agents can work in your browser. This package extracts the upstream Linux
x86_64 Flatpak bundle into /usr/lib/ilo with its desktop entry, icon and
AppStream metadata, using Chromium's native namespace sandbox; updates arrive
through DNF.

%prep
%setup -q -c -T
echo '%{SHA256SUM}  %{SOURCE0}' | sha256sum -c -
python3 -c '
import gi
gi.require_version("OSTree", "1.0")
from gi.repository import OSTree, Gio
repo = OSTree.Repo.new(Gio.File.new_for_path("repo"))
repo.create(OSTree.RepoMode.ARCHIVE, None)
'
flatpak build-import-bundle --no-update-summary repo %{SOURCE0}
python3 -c '
import os, gi
gi.require_version("OSTree", "1.0")
from gi.repository import OSTree, Gio
repo = OSTree.Repo.new(Gio.File.new_for_path("repo"))
repo.open(None)
_, refs = repo.list_refs(None, None)
rev = next(iter(refs.values()))
for sub, dst in [("/files/ilo", "ilo"), ("/export/share", "share")]:
    opts = OSTree.RepoCheckoutAtOptions()
    opts.mode = OSTree.RepoCheckoutMode.USER
    opts.subpath = sub
    repo.checkout_at(opts, -1, os.path.abspath(dst), rev, None)
'
rm -rf repo ilo/extensions

%build

%install
mkdir -p %{buildroot}/usr/lib/ilo %{buildroot}%{_bindir} %{buildroot}%{_sysconfdir}/ilo
cp -a ilo/. %{buildroot}/usr/lib/ilo/
ln -s /usr/lib/ilo/chrome %{buildroot}%{_bindir}/ilo
ln -s /usr/lib/ilo/policies %{buildroot}%{_sysconfdir}/ilo/policies
desktop-file-install --dir=%{buildroot}%{_datadir}/applications share/applications/app.ilo.browser.desktop
install -Dm644 share/icons/hicolor/scalable/apps/app.ilo.browser.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/app.ilo.browser.svg
install -Dm644 share/metainfo/app.ilo.browser.metainfo.xml \
    %{buildroot}%{_datadir}/metainfo/app.ilo.browser.metainfo.xml
find %{buildroot}/usr/lib/ilo -mindepth 1 \
    -printf '/usr/lib/ilo/%%P\n' | while read -r path; do
    if [ -d "%{buildroot}$path" ]; then echo "%%dir $path"; else echo "$path"; fi
done > ilo.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/app.ilo.browser.desktop

%files -f ilo.files
%license ilo/LICENSE ilo/NOTICE ilo/THIRD-PARTY.txt
%{_bindir}/ilo
%dir %{_sysconfdir}/ilo
%{_sysconfdir}/ilo/policies
%dir /usr/lib/ilo
%{_datadir}/applications/app.ilo.browser.desktop
%{_datadir}/icons/hicolor/scalable/apps/app.ilo.browser.svg
%{_datadir}/metainfo/app.ilo.browser.metainfo.xml

%changelog
%autochangelog
