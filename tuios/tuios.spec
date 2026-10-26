%global debug_package %{nil}

Name:       tuios
Version:    0.11.1
Release:    1%{?dist}
Summary:    Terminal multiplexer and window manager with a modal interface

License:    MIT
URL:        https://github.com/Gaurav-Gosain/tuios
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang >= 1.22

%description
TUIOS is a terminal multiplexer and window manager with a vim-like modal
interface, multiple terminal panes, workspaces, BSP tiling, and a command
palette. A daemon keeps terminal sessions alive across client restarts.

%prep
%autosetup

%build
# Allow Go to fetch the toolchain required by upstream, as with lazygit.
export GOSUMDB='sum.golang.org' GOTOOLCHAIN='auto'
export CGO_ENABLED=0 GOWORK=off

go build -trimpath -mod=readonly \
    -ldflags "-s -w -X main.version=%{version} -X main.builtBy=copr" \
    -o _build/%{name} ./cmd/%{name}

%install
install -Dpm 0755 _build/%{name} %{buildroot}%{_bindir}/%{name}

%check
_build/%{name} --version
_build/%{name} --help

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
