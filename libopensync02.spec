#
# Conditional build:
%bcond_without	python		# don't build python binding
%bcond_without	static_libs	# don't build static library
#
Summary:	Data synchronization framework
Summary(pl.UTF-8):	Szkielet do synchronizacji danych
Name:		libopensync02
Version:	0.22
Release:	13
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://opensync.org/download/releases/%{version}/libopensync-%{version}.tar.bz2
# Source0-md5:	f563ce2543312937a9afb4f8445ef932
Patch0:		%{name}-py-m4.patch
Patch1:		%{name}-swig.patch
Patch2:		%{name}-memset.patch
Patch3:		%{name}-link.patch
Patch4:		includes.patch
URL:		http://www.opensync.org/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
BuildRequires:	check-devel >= 0.9.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
%if %{with python}
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-modules >= 2.2
BuildRequires:	swig-python >= 1.3.17
%endif
# no such opensync plugins (yet?)
Obsoletes:	multisync-ldap
Obsoletes:	multisync-opie
Obsoletes:	libopensync < 0.33
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
Obsoletes:	libopensync-devel < 0.33
Conflicts:	libopensync-devel >= 0.33

%description devel
Header files for opensync library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki opensync.

%package static
Summary:	Static opensync library
Summary(pl.UTF-8):	Statyczna biblioteka opensync
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libopensync-static < 0.33

%description static
Static opensync library.

%description static -l pl.UTF-8
Statyczna biblioteka opensync.

%package -n python-opensync02
Summary:	Python bindings for opensync library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki opensync
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	python-opensync < 0.33
%pyrequires_eq	python-libs

%description -n python-opensync02
Python bindings for opensync library.

%description -n python-opensync02 -l pl.UTF-8
Wiązania Pythona do biblioteki opensync.

%prep
%setup -q -n libopensync-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

[ -x "%{_bindir}/python%{py_ver}-config" ] && sed -i -e 's#python-config#%{_bindir}/python%{py_ver}-config#g' acinclude.m4

# avoid errors on glib deprecation warnings
%{__sed} -i -e 's#-Werror##g' opensync/Makefile.am osengine/Makefile.am tools/Makefile.am \
	formats/Makefile.am formats/vformats-xml/Makefile.am osplugin/Makefile.am wrapper/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?debug:--disable-debug --disable-tracing} \
	%{?with_static_libs:--enable-static} \
	--enable-python%{!?with_python:=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/opensync/plugins \
	$RPM_BUILD_ROOT%{_datadir}/opensync/defaults

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

for bin in osyncbinary osyncdump osyncplugin osyncstress osynctest; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${bin}{,02}
done

%{__rm} $RPM_BUILD_ROOT%{_libdir}/opensync/formats/*.la
%{?with_static_libs:%{__rm} $RPM_BUILD_ROOT%{_libdir}/opensync/formats/*.a}
%if %{with python}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%{?with_static_libs:%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/osyncbinary02
%attr(755,root,root) %{_bindir}/osyncdump02
%attr(755,root,root) %{_bindir}/osyncplugin02
%attr(755,root,root) %{_bindir}/osyncstress02
%attr(755,root,root) %{_bindir}/osynctest02
%attr(755,root,root) %{_libdir}/libopensync.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopensync.so.0
%attr(755,root,root) %{_libdir}/libopensync-xml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopensync-xml.so.0
%attr(755,root,root) %{_libdir}/libosengine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosengine.so.0
%attr(755,root,root) %{_libexecdir}/osplugin
%dir %{_libdir}/opensync
%dir %{_libdir}/opensync/formats
%attr(755,root,root) %{_libdir}/opensync/formats/*.so
%dir %{_libdir}/opensync/plugins
%dir %{_datadir}/opensync
%dir %{_datadir}/opensync/defaults

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopensync.so
%attr(755,root,root) %{_libdir}/libopensync-xml.so
%attr(755,root,root) %{_libdir}/libosengine.so
%{_libdir}/libopensync.la
%{_libdir}/libopensync-xml.la
%{_libdir}/libosengine.la
%{_includedir}/opensync-1.0
%{_pkgconfigdir}/opensync-1.0.pc
%{_pkgconfigdir}/osengine-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopensync.a
%{_libdir}/libopensync-xml.a
%{_libdir}/libosengine.a
%endif

%if %{with python}
%files -n python-opensync02
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_opensync.so
%{py_sitedir}/opensync.py[co]
%endif
