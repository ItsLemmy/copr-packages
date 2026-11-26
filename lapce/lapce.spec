%global debug_package %{nil}
%global __strip /bin/true
%global appid dev.lapce.lapce
%global SHA256SUM 7a0945e6862bbe207316ba05ac5d634fc8a55069b61e4ec8989af632250d0984

Name:           lapce
Version:        0.4.6
Release:        1%{?dist}
Summary:        GPU-accelerated code editor written in Rust

License:        Apache-2.0 AND CC-BY-4.0 AND MIT
URL:            https://github.com/lapce/lapce
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-linux-amd64.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
Requires:       fontconfig
Requires:       libwayland-client
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       vulkan-loader
Recommends:     mesa-vulkan-drivers

%description
Lapce is a code editor with modal editing, language-server integration, a
built-in terminal, and remote development support. This package installs
upstream's stable Linux binary; updates are managed by DNF.

%prep
%autosetup
cp -p icons/codicons/LICENSE LICENSE.codicons
printf '%%s  %%s\n' '%{SHA256SUM}' '%{SOURCE1}' | sha256sum -c -
tar -xzf %{SOURCE1}

%build

%install
install -Dpm0755 Lapce/lapce %{buildroot}%{_bindir}/lapce
install -Dpm0644 extra/linux/%{appid}.desktop %{buildroot}%{_datadir}/applications/%{appid}.desktop
install -Dpm0644 extra/linux/%{appid}.metainfo.xml %{buildroot}%{_metainfodir}/%{appid}.metainfo.xml
install -Dpm0644 extra/images/logo.png %{buildroot}%{_datadir}/pixmaps/%{appid}.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
%files
%license LICENSE LICENSE.codicons
%doc README.md
%{_bindir}/lapce
%{_datadir}/applications/%{appid}.desktop
%{_metainfodir}/%{appid}.metainfo.xml
%{_datadir}/pixmaps/%{appid}.png

%changelog
%autochangelog
