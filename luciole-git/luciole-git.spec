Name:           luciole-git
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Native Wayland file manager with fast previews, tabs and split view

License:        MIT
URL:            https://github.com/noctalia-dev/luciole
Source0:        %{url}/archive/@COMMIT@.tar.gz#/luciole-@COMMIT@.tar.gz

ExclusiveArch:  aarch64 x86_64

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.1
BuildRequires:  ninja-build
BuildRequires:  stb_image_resize2-devel
BuildRequires:  /usr/bin/wayland-scanner
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.44
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.76
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(glycin-2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(pango) >= 1.50
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(tomlplusplus) >= 3.4
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(xkbcommon)

# Trash, network locations and device mounting go through GVfs
Requires:       gvfs
Requires:       shared-mime-info
Requires:       gsettings-desktop-schemas
Requires:       dconf
Recommends:     adwaita-icon-theme
Recommends:     hicolor-icon-theme
Recommends:     glycin-loaders
Recommends:     glib-networking
Suggests:       ffmpeg-free
Suggests:       ffmpegthumbnailer
Suggests:       poppler-utils
Suggests:       7zip
Suggests:       gvfs-smb
Suggests:       udisks2
Suggests:       xdg-terminal-exec
Suggests:       xdg-desktop-portal
Provides:       luciole = %{version}-%{release}
Conflicts:      luciole
# Terra
Conflicts:      luciole-nightly

%description
Luciole is a native Wayland file manager using Noctalia rendering and
controls, with fast previews, tabs, split view and Miller columns. It also
provides an org.freedesktop.FileManager1 service and an xdg-desktop-portal
FileChooser backend.

%prep
%autosetup -n luciole-@COMMIT@

%build
%meson -Db_ndebug=true -Dtests=disabled -Dnative_optimizations=false -Dbuild_revision=@COMMIT@
%meson_build

%install
%meson_install

%files
%license %{_datadir}/licenses/luciole/LICENSE
%license %{_datadir}/luciole/assets/fonts/tabler-icons-license.txt
%doc README.md PACKAGING.md docs/user
%{_bindir}/luciole
%{_datadir}/luciole/
%{_datadir}/applications/dev.noctalia.luciole.desktop
%{_datadir}/applications/dev.noctalia.luciole-chooser.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.noctalia.luciole.svg
%{_datadir}/dbus-1/services/dev.noctalia.luciole.FileManager1.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.luciole.service
%{_datadir}/xdg-desktop-portal/portals/luciole.portal
%{_datadir}/bash-completion/completions/luciole
%{_datadir}/zsh/site-functions/_luciole
%{_datadir}/fish/vendor_completions.d/luciole.fish

%changelog
%autochangelog
