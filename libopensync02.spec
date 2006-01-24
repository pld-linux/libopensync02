Summary:	Data synchronization framework
Summary(pl):	Szkielet do synchronizacji danych
Name:		libopensync
Version:	0.18
Release:	0.2
License:	LGPL
Group:		Libraries
Source0:	http://www.opensync.org/attachment/wiki/download/%{name}-%{version}.tar.gz?format=raw
# Source0-md5:	ce94a69fb7ae7533d1f8828b6402cec8
URL:		http://www.opensync.org/
Patch0:		%{name}-python.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	swig-python
# no such opensync plugins (yet?)
Obsoletes:	multisync-ldap
Obsoletes:	multisync-opie
Obsoletes:	multisync-syncml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSync is a synchronization framework that is platform and
distribution independent.

It consists of several plugins that can be used to connect to devices,
a powerful sync-engine and the framework itself.

The synchronization framework is kept very flexible and is capable of
synchronizing any type of data, including contacts, calendar, tasks,
notes and files. 

%description -l pl
OpenSync to niezale¿ny od platformy i dystrybucji szkielet do
synchronizacji danych.

Sk³ada siê z kilku wtyczek, których mo¿na u¿ywaæ do ³±czenia siê z
urz±dzeniami, potê¿nego silnika synchronizuj±cego i samego szkieletu.

Szkielet do synchronizacji jest utrzymywany jako bardzo elastyczny i
potrafi±cy synchronizowaæ dowolny rodzaj danych, w³±cznie z
kontaktami, kalendarzem, zadaniami, notatkami i plikami.

%package devel
Summary:	Header files for opensync library
Summary(pl):	Pliki nag³ówkowe biblioteki opensync
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	multisync-devel

%description devel
Header files for opensync library.

%description devel -l pl
Pliki nag³ówkowe biblioteki opensync.

%package static
Summary:	Static opensync library
Summary(pl):	Statyczna biblioteka opensync
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static opensync library.

%description static -l pl
Statyczna biblioteka opensync.

%package -n python-opensync
Summary:	Python bindings for opensync library
Summary(pl):	Wi±zania Pythona do biblioteki opensync
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-opensync
Python bindings for opensync library.

%description -n python-opensync -l pl
Wi±zania Pythona do biblioteki opensync.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/opensync/plugins \
    $RPM_BUILD_ROOT%{_datadir}/opensync/defaults

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{py,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
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

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-opensync
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]
