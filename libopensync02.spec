#
# Conditional build:
%bcond_without	python		# don't build python binding
%bcond_without	static_libs	# don't build static library
#
Summary:	Data synchronization framework
Summary(pl.UTF-8):	Szkielet do synchronizacji danych
Name:		libopensync
# WARNING: don't go for 0.3x line - it's DEVELopment series
Version:	0.22
Release:	4
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	f563ce2543312937a9afb4f8445ef932
Patch0:		%{name}-py-m4.patch
URL:		http://www.opensync.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libxml2-devel
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	swig-python
%endif
BuildRequires:	sqlite3-devel
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	sqlite3-devel
Obsoletes:	multisync-devel

%description devel
Header files for opensync library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki opensync.

%package static
Summary:	Static opensync library
Summary(pl.UTF-8):	Statyczna biblioteka opensync
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static opensync library.

%description static -l pl.UTF-8
Statyczna biblioteka opensync.

%package -n python-opensync
Summary:	Python bindings for opensync library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki opensync
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-opensync
Python bindings for opensync library.

%description -n python-opensync -l pl.UTF-8
Wiązania Pythona do biblioteki opensync.

%prep
%setup -q
%patch0 -p1

[ -x "%{_bindir}/python%{py_ver}-config" ] && sed -i -e 's#python-config#%{_bindir}/python%{py_ver}-config#g' acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?debug:--disable-debug --disable-tracing} \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	--%{?with_python:en}%{!?with_python:dis}able-python

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/opensync/plugins \
    $RPM_BUILD_ROOT%{_datadir}/opensync/defaults

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{py,la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/opensync/formats/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/osplugin
%dir %{_libdir}/opensync
%dir %{_libdir}/opensync/formats
%dir %{_libdir}/opensync/plugins
%dir %{_datadir}/opensync
%dir %{_datadir}/opensync/defaults
%attr(755,root,root) %{_libdir}/opensync/formats/*.so
%{_libdir}/opensync/formats/*.la

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/opensync*
%{_pkgconfigdir}/*.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%if %{with python}
%files -n python-opensync
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]
%endif
