%global debug_package %{nil}
%global __strip /bin/true

Name:           rhun
Version:        0.19.2
Release:        1%{?dist}
Summary:        Small and fast code editor written in assembly

License:        MIT
URL:            https://github.com/vshvedov/rhun
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}-linux-x86_64.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils

Recommends:     hicolor-icon-theme

%description
rhun is a small and fast code editor written in assembly. It provides tabs,
syntax highlighting, find and replace, optional Vim mode, a built-in terminal,
Git staging and history, fuzzy file and project search, an agents panel and
native extensions.

This package installs the unmodified upstream statically linked release binary.

%prep
%setup -q

%build

%install
install -Dpm 0755 bin/%{name} -t %{buildroot}%{_bindir}/
install -Dpm 0644 share/applications/rhun.desktop -t %{buildroot}%{_datadir}/applications/
install -Dpm 0644 share/applications/rhun-url-handler.desktop -t %{buildroot}%{_datadir}/applications/
install -Dpm 0644 share/icons/hicolor/scalable/apps/rhun.svg -t %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
for size in 256x256 512x512; do
    install -Dpm 0644 share/icons/hicolor/${size}/apps/rhun.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/rhun.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/rhun.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/rhun-url-handler.desktop

%files
%license LICENSE LICENSE-Unicode.txt
%{_bindir}/rhun
%{_datadir}/applications/rhun.desktop
%{_datadir}/applications/rhun-url-handler.desktop
%{_datadir}/icons/hicolor/scalable/apps/rhun.svg
%{_datadir}/icons/hicolor/*/apps/rhun.png

%post
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :

%changelog
%autochangelog
