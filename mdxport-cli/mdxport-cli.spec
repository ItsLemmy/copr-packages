%global debug_package %{nil}

Name:    mdxport-cli
Version: 0.2.11
Release: 1%{?dist}
Summary: Convert Markdown documents to PDF using Typst
License: MIT
URL:     https://github.com/cosformula/mdxport-cli
Source0: https://github.com/cosformula/mdxport-cli/archive/refs/tags/v%{version}.tar.gz
Source1: https://github.com/ItsLemmy/copr-packages/releases/download/mdxport-cli-%{version}/mdxport-cli-%{version}-vendor.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
mdxport is a command-line tool that converts Markdown documents into PDF files
using Typst as the rendering engine. It operates as a single, self-contained
binary with no external dependencies.

Features:
- LaTeX mathematical notation support
- Built-in and customizable templates
- YAML frontmatter configuration
- File watching mode for automatic recompilation
- CJK (Chinese/Japanese/Korean) language support

%prep
%autosetup -n mdxport-cli-%{version}
tar xf %{SOURCE1}
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --offline

%install
install -Dpm 0755 target/release/mdxport -t %{buildroot}%{_bindir}/

%files
%license LICENSE
%doc README.md
%{_bindir}/mdxport
