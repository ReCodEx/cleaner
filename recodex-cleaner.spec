%define name recodex-cleaner
%define short_name cleaner
%define version 1.3.0
%define unmangled_version bcb9308ac903ed94313ec8436ead5cbfee12363d
%define release 1

Summary: Clean cache which is used by ReCodEx workers
Name: %{name}
Version: %{version}
Release: %{release}
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: ReCodEx Team <UNKNOWN>
Url: https://github.com/ReCodEx/cleaner

BuildRequires: systemd
%{?fedora:BuildRequires: python3 python3-devel python3-pip python3-wheel}
%{?rhel:BuildRequires: python3 python3-devel python3-pip python3-wheel}
# Modern Python build tools for pyproject.toml
BuildRequires: python3dist(build)
BuildRequires: python3dist(setuptools) >= 61.0
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%{?fedora:Requires: python3-PyYAML}
%{?rhel:Requires: python3-PyYAML}

Source0: https://github.com/ReCodEx/%{short_name}/archive/%{unmangled_version}.tar.gz#/%{short_name}-%{unmangled_version}.tar.gz

%description
ReCodEx cache cleaner which should be deployed with recodex-worker.

%prep
%setup -n %{short_name}-%{unmangled_version}

%build
# Build using modern Python build system with pyproject.toml
# This replaces the legacy setup.py build process
%{python3} -m build --wheel --no-isolation

%install
# Install the wheel using pip (modern approach)
%{python3} -m pip install --no-deps --no-index --find-links dist/ --root=%{buildroot} recodex-cleaner

# Create log directory
mkdir -p %{buildroot}/var/log/recodex

# Install system files manually (replaces setup.py data_files)
# These files are no longer installed automatically with pyproject.toml
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}%{_sysconfdir}/recodex/cleaner
install -m 644 cleaner/install/recodex-cleaner.service %{buildroot}/lib/systemd/system/
install -m 644 cleaner/install/recodex-cleaner.timer %{buildroot}/lib/systemd/system/
install -m 644 cleaner/install/config.yml %{buildroot}%{_sysconfdir}/recodex/cleaner/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group recodex >/dev/null || groupadd -r recodex
getent passwd recodex >/dev/null || useradd -r -g recodex -d %{_sysconfdir}/recodex -s /sbin/nologin -c "ReCodEx Code Examiner" recodex
exit 0

%post
%systemd_post 'recodex-cleaner.service'

%preun
%systemd_preun 'recodex-cleaner.service'

%postun
%systemd_postun 'recodex-cleaner.service'

%files
%defattr(-,root,root)
%dir %attr(-,recodex,recodex) %{_sysconfdir}/recodex/cleaner
%dir %attr(-,recodex,recodex) /var/log/recodex

%{python3_sitelib}/cleaner/
%{python3_sitelib}/recodex_cleaner-%{version}.dist-info/
%{_bindir}/recodex-cleaner
%config(noreplace) %attr(-,recodex,recodex) %{_sysconfdir}/recodex/cleaner/config.yml
/lib/systemd/system/recodex-cleaner.service
/lib/systemd/system/recodex-cleaner.timer

