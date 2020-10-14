%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name pankoclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

Name:             python-pankoclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Panko

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif


%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Panko
%{?python_provide:%python_provide python3-%{pypi_name}}
Obsoletes: python2-%{pypi_name} < %{version}-%{release}


BuildRequires:    git
BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-tools

Requires:         python3-keystoneauth1 >= 3.4.0
Requires:         python3-osc-lib >= 1.8.0
Requires:         python3-oslo-i18n >= 2.1.0
Requires:         python3-oslo-serialization >= 1.10.0
Requires:         python3-oslo-utils >= 3.18.0
Requires:         python3-osprofiler >= 1.4.0
Requires:         python3-pbr
Requires:         python3-requests
Requires:         python3-six >= 1.9.0


%description -n python3-%{pypi_name}
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Panko API Client
Group:            Documentation

BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-osc-lib
# test
BuildRequires:    python3-babel

%description      doc
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool
(panko).

This package contains auto-generated documentation.
%endif

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Panko Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%description
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf pankoclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{py3_build}


%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s panko %{buildroot}%{_bindir}/panko-3

%if 0%{?with_doc}
# Some env variables required to successfully build our doc
export PATH=$PATH:%{buildroot}%{_bindir}
export LANG=en_US.utf8
sphinx-build-3 -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/panko
%{_bindir}/panko-3
# XXX: man page build is broken
#%{_mandir}/man1/panko.1*
%{python3_sitelib}/pankoclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/pankoclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/pankoclient/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog

