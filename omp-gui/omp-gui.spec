%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none
%global appdir /opt/omp-gui
%global SHA256SUM0 8f4f8379a5947ee56650119749687b1e1b886b34aaf369745bbda5af19264b2a

# Bundled Electron libraries are private, not system library providers.
%global __provides_exclude_from ^%{appdir}/.*$
%global __requires_exclude ^(libEGL|libGLESv2|libffmpeg|libvk_swiftshader|libvulkan)\\.so.*\\(64bit\\)$

Name:           omp-gui
Version:        0.9.28
Release:        1%{?dist}
Summary:        Desktop GUI for the omp coding agent

# Application license; bundled Electron/Chromium notices are shipped alongside it.
License:        MIT
URL:            https://github.com/nornzach/oh-my-pi-gui
Source0:        %{url}/releases/download/v%{version}/omp_%{version}_amd64.deb
Source1:        https://raw.githubusercontent.com/nornzach/oh-my-pi-gui/v%{version}/LICENSE

ExclusiveArch:  x86_64
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  desktop-file-utils
Requires:       gtk3
Requires:       nss
Requires:       alsa-lib
Requires:       mesa-libgbm
Requires:       xdg-utils
Requires:       hicolor-icon-theme
Recommends:     git
Recommends:     openssh-clients

%description
Desktop interface for the omp coding agent with parallel sessions, visual
tool calls, model and provider management, and usage analytics.

This package repackages the upstream Linux release, including Electron and
its bundled agent. No separate omp, Bun, or Node installation is required.

%prep
echo "%{SHA256SUM0}  %{SOURCE0}" | sha256sum -c -
%setup -q -c -T
ar p %{SOURCE0} data.tar.xz | tar -xJ
cp %{SOURCE1} LICENSE

%build

%install
install -d %{buildroot}%{appdir}
cp -a opt/omp/. %{buildroot}%{appdir}/
# Keep Chromium's sandbox usable without disabling it in the launcher.
chmod 4755 %{buildroot}%{appdir}/chrome-sandbox
# The upstream payload is a Debian package; identify the installed format correctly.
printf 'rpm\n' > %{buildroot}%{appdir}/resources/package-type
install -d %{buildroot}%{_bindir}
ln -s ../../opt/omp-gui/omp-gui %{buildroot}%{_bindir}/omp-gui

desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    --set-key=Exec --set-value='omp-gui %U' \
    usr/share/applications/omp-gui.desktop
cp -a usr/share/icons %{buildroot}%{_datadir}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/omp-gui.desktop
test -x %{buildroot}%{appdir}/omp-gui
test -x %{buildroot}%{appdir}/resources/omp
test -f %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/omp-gui.png

%files
%license LICENSE
%dir %{appdir}
%{appdir}/*
%{_bindir}/omp-gui
%{_datadir}/applications/omp-gui.desktop
%{_datadir}/icons/hicolor/*/apps/omp-gui.png

%changelog
%autochangelog
