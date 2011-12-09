%define		mod_name	transform
%define 	apxs		/usr/sbin/apxs
Summary:	Module to serve XML based content
Summary(pl.UTF-8):	Moduł do udostępniania dokumentów XML
Name:		apache-mod_%{mod_name}
Version:	0.6.0
Release:	1
License:	GPL v2+
Group:		Networking/Daemons/HTTP
Source0:	http://www.outoforder.cc/downloads/mod_transform/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	8b27adea2536f105470b4bedc418ab3b
Source1:	%{name}.conf
URL:		http://www.outoforder.cc/projects/apache/mod_transform/
BuildRequires:	%{apxs}
BuildRequires:	apr-devel >= 1:1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_transform is a filter module that allows Apache 2.0 to do dynamic
XSL Transformations on either static XML documents, or XML documents
generated from another Apache module or CGI program.

%description -l pl.UTF-8
mod_transform to moduł filtra umożliwiający serwerowi Apache 2.0
wykonywać dynamiczne przekształcenia XML na statycznych dokumentach
XML lub dokumentach XML generowanych przez inny moduł Apache'a lub
program CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}
sed -i -e "s:apr-config:apr-1-config:g" aclocal.m4 m4/apache.m4
sed -i -e "s:apu-config:apu-1-config:g" aclocal.m4 m4/apache.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install -p src/.libs/libmod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/61_mod_transform.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc TODO
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
