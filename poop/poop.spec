%global debug_package %{nil}

Name:       poop
Version:    0.5.0
Release:    1%{?dist}
Summary:    Performance Optimizer Observation Platform

License:    MIT
URL:        https://github.com/andrewrk/poop

Source0:    https://github.com/andrewrk/poop/releases/download/%{version}/x86_64-linux-poop
Source1:    https://raw.githubusercontent.com/andrewrk/poop/%{version}/LICENSE

ExclusiveArch: x86_64

%description
poop (Performance Optimizer Observation Platform) is a command line
benchmarking tool that uses Linux's perf_event_open functionality to
compare the performance of multiple commands with a colorful terminal
user interface.

%prep
cp %{SOURCE1} LICENSE

%build
# pre-built binary

%install
install -Dpm 0755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/poop

%changelog
%autochangelog
