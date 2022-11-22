%global debug_package %{nil}
%global package_name opc
%global product_name OpenShift Pipelines
%global golang_version 1.18.5
%global opc_version 1.0.0
%global opc_release 1
%global opc_cli_version v%{opc_version}
%global repo github.com/rupalibehera/opc
%global source_dir opc-client-%{opc_version}-%{opc_release}
%global source_tar %{source_dir}.tar.gz

Name:           %{package_name}
Version:        %{opc_version}
Release:        %{opc_release}
Summary:        A command line tool to enhance users productivity for working with %{product_name}
License:        ASL 2.0
URL:            https://%{repo}/releases/tag/v%{opc_version}

Source0:        %{source_tar}
BuildRequires:  golang >= %{golang_version}
Provides:       %{package_name}
Obsoletes:      %{package_name}

%description
The OpenShift Pipelines client is a CLI tool to work effectively with OpenShift pipelines

%prep
%setup -q -n %{source_dir}

%build
export CGO_ENABLED=0
RELEASE_VERSION=%{opc_version} make amd64

%install
mkdir -p %{buildroot}/%{_bindir}
install -D -m 0755 bin/tkn-linux-amd64 %{buildroot}%{_bindir}/tkn

install -d %{buildroot}%{_datadir}/bash-completion/completions
%{buildroot}%{_bindir}/tkn completion bash > %{buildroot}%{_datadir}/bash-completion/completions/_tkn

install -d %{buildroot}%{_datadir}/zsh/site-functions
%{buildroot}%{_bindir}/tkn completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_tkn

install -d %{buildroot}%{_mandir}/man1
cp -a docs/man/man1/* %{buildroot}%{_mandir}/man1

install -d %{buildroot}%{_datadir}/%{name}-redistributable/{linux,macos,windows}
install -p -m 755 bin/tkn-linux-amd64 %{buildroot}%{_datadir}/%{name}-redistributable/linux/tkn-linux-amd64
install -p -m 755 bin/tkn-darwin-amd64 %{buildroot}/%{_datadir}/%{name}-redistributable/macos/tkn-darwin-amd64
install -p -m 755 bin/tkn-windows-amd64 %{buildroot}/%{_datadir}/%{name}-redistributable/windows/tkn-windows-amd64.exe

%files
%doc *.md
%license LICENSE
%{_bindir}/tkn
%{_datadir}/zsh/site-functions/*
%{_datadir}/bash-completion/completions/*
%{_mandir}/*

%package redistributable
Summary:        %{product_name} CLI binaries for Linux, macOS and Windows
BuildRequires:  golang >= %{golang_version}

%description redistributable
%{product_name} CLI cross platform binaries for Linux, macOS and Windows.

%files redistributable
%license LICENSE
%dir %{_datadir}/%{name}-redistributable/linux/
%dir %{_datadir}/%{name}-redistributable/macos/
%dir %{_datadir}/%{name}-redistributable/windows/
%{_datadir}/%{name}-redistributable/linux/tkn-linux-amd64
%{_datadir}/%{name}-redistributable/macos/tkn-darwin-amd64
%{_datadir}/%{name}-redistributable/windows/tkn-windows-amd64.exe

