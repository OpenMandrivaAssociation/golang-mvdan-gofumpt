%global debug_package %{nil}

# Run tests in check section
%bcond_with check

# https://github.com/mvdan/gofumpt
%global goipath		mvdan.cc/gofumpt
%global forgeurl	https://github.com/mvdan/gofumpt
Version:		0.7.0

%gometa

Summary:	A stricter gofmt
Name:		golang-github-mvdan-gofumpt

Release:	1
Source0:	https://github.com/mvdan/gofumpt/archive/v%{version}/gofumpt-%{version}.tar.gz
URL:		https://github.com/mvdan/gofumpt
License:	BSD with advertising
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang(github.com/google/go-cmp/cmp)
BuildRequires:	golang(golang.org/x/mod/module)
BuildRequires:	golang(golang.org/x/mod/semver)
BuildRequires:	golang(golang.org/x/sync/semaphore)
BuildRequires:	golang(golang.org/x/tools/go/ast/astutil)

%description
The tool is a fork of gofmt as of Go 1.22.  It can be used
as a drop-in replacement to format your Go code, and running
gofmt after gofumpt should produce no changes. 

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n gofumpt-%{version}

%build
%gobuildroot
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done


%check
%if %{with check}
%gochecks
%endif

