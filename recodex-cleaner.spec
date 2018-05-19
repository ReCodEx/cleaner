%define name recodex-cleaner
%define version 1.1.0
%define unmangled_version 1.1.0
%define unmangled_version 1.1.0
%define release 1

Summary: Clean cache which is used by ReCodEx workers
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: ReCodEx Team <UNKNOWN>
Url: https://github.com/ReCodEx/cleaner

%if 0%{?fedora}
BuildRequires: python3 python3-devel python3-setuptools python3-pip
%endif

%description
ReCodEx cache cleaner which should be deployed with recodex-worker.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%post
#!/bin/sh

CONF_DIR=/etc/recodex
LOG_DIR=/var/log/recodex

# Create 'recodex' user if not exist
id -u recodex > /dev/null 2>&1
if [ $? -eq 1 ]
then
	useradd --system --shell /sbin/nologin recodex
fi

# Create default logging directory and set proper permission
mkdir -p ${LOG_DIR}
chown -R recodex:recodex ${LOG_DIR}

# Change owner of config files
chown -R recodex:recodex ${CONF_DIR}



%files -f INSTALLED_FILES
%defattr(-,root,root)
