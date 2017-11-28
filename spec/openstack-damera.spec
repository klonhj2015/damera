%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service damera


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:		openstack-%{service}
Summary:	Container Management project for OpenStack
Version:	%{?version}
Release:	1%{?dist}
License:	ASL 2.0
URL:		https://github.com/openstack/damera.git

Source0:	http://tarballs.openstack.org/%{service}/%{service}-%{version}%{?milestone}.tar.gz

Source1:	%{service}.logrotate
Source2:	%{name}-api.service
Source3:	%{name}-conductor.service

BuildArch: noarch

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python-pbr
BuildRequires: python-setuptools

BuildRequires: systemd-units

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-conductor = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}

%description
Damera is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

%package -n python-%{service}
Summary: Damera Python libraries


%description -n python-%{service}
Damera is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

%package common
Summary: Damera common

Requires: python-%{service} = %{version}-%{release}

Requires(pre): shadow-utils

%description common
Components common to all OpenStack Damera services

%package conductor
Summary: The Damera conductor

Requires: %{name}-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description conductor
OpenStack Damera Conductor

%package api
Summary: The Damera API

Requires: %{name}-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description api
OpenStack-native ReST API to the Damera Engine

%if 0%{?with_doc}
%package -n %{name}-doc
Summary:    Documentation for OpenStack Damera

Requires:    python-%{service} = %{version}-%{release}

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-stevedore

%description -n %{name}-doc
Damera is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

This package contains documentation files for Damera.
%endif

# tests
%package -n python-%{service}-tests
Summary:          Tests for OpenStack Damera

Requires:        python-%{service} = %{version}-%{release}

%description -n python-%{service}-tests
Damera is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

%prep
%setup -q -n %{service}-%{upstream_version}

# Let's handle dependencies ourselves
rm -rf {test-,}requirements{-bandit,}.txt tools/{pip,test}-requires

# Remove tests in contrib
find contrib -name tests -type d | xargs rm -rf

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif
popd

mkdir -p %{buildroot}%{_localstatedir}/log/%{service}/
mkdir -p %{buildroot}%{_localstatedir}/run/%{service}/
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# install systemd unit files
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-conductor.service

mkdir -p %{buildroot}%{_sharedstatedir}/%{service}/
mkdir -p %{buildroot}%{_sharedstatedir}/%{service}/certificates/
mkdir -p %{buildroot}%{_sysconfdir}/%{service}/

oslo-config-generator --config-file etc/damera/damera-config-generator.conf --output-file %{buildroot}%{_sysconfdir}/%{service}/damera.conf
chmod 640 %{buildroot}%{_sysconfdir}/%{service}/damera.conf
install -p -D -m 640 etc/damera/policy.json %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 etc/damera/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}

%check
%{__python2} setup.py test ||

%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common
%{_bindir}/damera-db-manage
%license LICENSE
%dir %attr(0750,%{service},root) %{_localstatedir}/log/%{service}
%dir %attr(0755,%{service},root) %{_localstatedir}/run/%{service}
%dir %attr(0755,%{service},root) %{_sharedstatedir}/%{service}
%dir %attr(0755,%{service},root) %{_sharedstatedir}/%{service}/certificates
%dir %attr(0755,%{service},root) %{_sysconfdir}/%{service}
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/damera.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/policy.json
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%pre common
# 1870:1870 for damera - rhbz#845078
getent group %{service} >/dev/null || groupadd -r --gid 1870 %{service}
getent passwd %{service}  >/dev/null || \
useradd --uid 1870 -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
-c "OpenStack Damera Daemons" %{service}
exit 0


%files conductor
%doc README.rst
%license LICENSE
%{_bindir}/damera-conductor
%{_unitdir}/%{name}-conductor.service

%post conductor
%systemd_post %{name}-conductor.service

%preun conductor
%systemd_preun %{name}-conductor.service

%postun conductor
%systemd_postun_with_restart %{name}-conductor.service


%files api
%doc README.rst
%license LICENSE
%{_bindir}/damera-api
%{_unitdir}/%{name}-api.service


%if 0%{?with_doc}
%files -n %{name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests


%post api
%systemd_post %{name}-api.service

%preun api
%systemd_preun %{name}-api.service

%postun api
%systemd_postun_with_restart %{name}-api.service

%changelog

* Thu Mar 24 2016 RDO <rdo-list@redhat.com> 2.0.0-0.1
- RC1 Rebuild for Mitaka 
