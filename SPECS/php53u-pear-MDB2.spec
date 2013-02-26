%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_name MDB2
%global prever    b3
%global php_base php53u

Name:           %{php_base}-pear-MDB2
Version:        2.5.0
%if 0%{?prever:1}
Release:        0.1.%{?prever}.ius%{?dist}
%else
Release:        1.ius%{?dist}
%endif
Summary:        Database Abstraction Layer

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/MDB2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{php_base}-pear(PEAR) >= 1.9.1

Requires:       %{php_base}-common >= 5.3.0
Requires:       %{php_base}-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-pear(%{pear_name}) = %{version}-%{release}
Provides:       %{php_base}-pear(%{pear_name}) = %{version}%{?prever}
Provides:       php-pear(%{pear_name}) = %{version}%{?prever}

%description
PEAR::MDB2 is a merge of the PEAR::DB and Metabase php database abstraction
layers.

It provides a common API for all supported RDBMS. The main difference to most
other DB abstraction packages is that MDB2 goes much further to ensure
portability.


%prep
%setup -qc
# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}%{?prever}
# package.xml is V2
sed -e '/LICENSE/s/role="data"/role="doc"/' <../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}%{?prever}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null ||:

%postun
if [ "$1" -eq "0" ]; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null ||:
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/%{pear_name}
%{pear_phpdir}/MDB2.php


%changelog
* Thu May 17 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 2.5.0-0.1.b3
- Ported from Fedora Rawhide
