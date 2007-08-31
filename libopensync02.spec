# TODO
# - CFLAGS not passed from spec
# - buildfail:
#wrapper/opensync_wrap.c: In function `GroupEnv_add_group':
#wrapper/opensync_wrap.c:3559: error: too few arguments to function `osync_group_env_add_group'
#scons: *** [wrapper/opensync_wrap.os] Error 1
#
# Conditional build:
%bcond_without	python		# don't build python binding
#
Summary:	Data synchronization framework
Summary(pl.UTF-8):	Szkielet do synchronizacji danych
Name:		libopensync
Version:	0.31
Release:	0.1
License:	LGPL
Group:		Libraries
Source0:	http://www.opensync.org/attachment/wiki/download/%{name}-%{version}.tar.bz2?format=raw
# Source0-md5:	caf4fd1b174f4863ba79ab074a29b054
URL:		http://www.opensync.org/
Patch0:		%{name}-opt.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.10
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	scons
BuildRequires:	sqlite3-devel >= 3.3
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	swig-python
%endif
# no such opensync plugins (yet?)
Obsoletes:	multisync-ldap
Obsoletes:	multisync-opie
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSync is a synchronization framework that is platform and
distribution independent.

It consists of several plugins that can be used to connect to devices,
a powerful sync-engine and the framework itself.

The synchronization framework is kept very flexible and is capable of
synchronizing any type of data, including contacts, calendar, tasks,
notes and files.

%description -l pl.UTF-8
OpenSync to niezależny od platformy i dystrybucji szkielet do
synchronizacji danych.

Składa się z kilku wtyczek, których można używać do łączenia się z
urządzeniami, potężnego silnika synchronizującego i samego szkieletu.

Szkielet do synchronizacji jest utrzymywany jako bardzo elastyczny i
potrafiący synchronizować dowolny rodzaj danych, włącznie z
kontaktami, kalendarzem, zadaniami, notatkami i plikami.

%package devel
Summary:	Header files for opensync library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki opensync
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libopensync-static
Obsoletes:	multisync-devel

%description devel
Header files for opensync library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki opensync.

%package -n python-opensync
Summary:	Python bindings for opensync library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki opensync
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-opensync
Python bindings for opensync library.

%description -n python-opensync -l pl.UTF-8
Wiązania Pythona do biblioteki opensync.

%prep
%setup -q
%patch0 -p1

%build
%scons \
	prefix=%{_prefix} \
	%{?with_python:enable_python=1}

%install
rm -rf $RPM_BUILD_ROOT
%scons install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/opensync/plugins \
    $RPM_BUILD_ROOT%{_datadir}/opensync/defaults

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/opensync
%dir %{_libdir}/opensync/formats
%dir %{_libdir}/opensync/plugins
%dir %{_datadir}/opensync
%dir %{_datadir}/opensync/defaults
%{_datadir}/opensync/capabilities
%{_datadir}/opensync/descriptions
%attr(755,root,root) %{_libdir}/opensync/formats/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/opensync*
%{_pkgconfigdir}/*.pc

%if %{with python}
%files -n python-opensync
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]
%endif
