%global debug_package %{nil}

Name:       glow
Version:    2.1.1
Release:    1%{?dist}
Summary:    Render markdown on the CLI, with pizzazz!

License:    MIT
URL:        https://github.com/charmbracelet/glow
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# 1.22 is the version where they introduced the `GOTOOLCHAIN=auto`
BuildRequires: golang >= 1.22

%description
Glow is a terminal based markdown reader designed from the ground up to bring
out the beauty--and power--of the CLI. Use it to discover markdown files, read
documentation directly on the command line and stash markdown files to your own
private collection so you can read them anywhere. Glow will find local markdown
files in subdirectories or a local Git repository.

%prep
#####

%autosetup -p1

%build
######

# Most Fedora and its derivatives do not have up-to-date version of the "golang" package, so
# we need to tell Go to get the latest toolchain.
#
# Note: Some build environments export GOSUMDB=off, which prevents the toolchain download.
# Override it here to allow verification against the public checksum DB.
export GOSUMDB='sum.golang.org' GOTOOLCHAIN='auto'

go get
go build \
    -ldflags "-X main.Version=v%{version}" \
    -o _build/%{name}

# Man page
./_build/%{name} man > %{name}.1

# Shell completions
./_build/%{name} completion bash > %{name}.bash
./_build/%{name} completion zsh > _%{name}
./_build/%{name} completion fish > %{name}.fish


%install
########

install -Dpm 0755 _build/%{name} %{buildroot}%{_bindir}/%{name}

# Man page
install -Dpm 0644 %{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1

# Shell completions
install -Dpm 0644 %{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dpm 0644 _%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dpm 0644 %{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish


%files
######

%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*.1*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
