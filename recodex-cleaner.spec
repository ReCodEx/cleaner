%define name recodex-cleaner
%define short_name cleaner
%define version 1.2.0
%define unmangled_version e4b11359097d870d6c741911036d4c3797ce64c4
%define release 8

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
%{?fedora:BuildRequires: python3 python3-devel python3-setuptools}
%{?rhel:BuildRequires: python3 python3-devel python3-setuptools}
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
%py3_build

%install
%py3_install
mkdir -p %{buildroot}/var/log/recodex

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
%{python3_sitelib}/recodex_cleaner-%{version}-py?.?.egg-info/
%{_bindir}/recodex-cleaner
%config(noreplace) %attr(-,recodex,recodex) %{_sysconfdir}/recodex/cleaner/config.yml
/lib/systemd/system/recodex-cleaner.service
/lib/systemd/system/recodex-cleaner.timer

