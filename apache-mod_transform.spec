%define		mod_name	transform
%define 	apxs		/usr/sbin/apxs
Summary:	Module to serve XML based content
Summary(pl):	Modu³ do udostêpniania dokumentów XML
Name:		apache-mod_%{mod_name}
Version:	0.4.0
Release:	2
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.outoforder.cc/downloads/mod_transform/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	a41ea16eeefb9b798186153b154a1219
Source1:	mod_%{mod_name}.conf
URL:	http://www.outoforder.cc/projects/apache/mod_transform/
BuildRequires:	%{apxs}
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
Requires(post,preun):	%{apxs}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
mod_transform is a filter module that allows Apache 2.0 to do dynamic
XSL Transformations on either static XML documents, or XML documents
generated from another Apache module or CGI program.

%description -l pl
mod_transform to modu³ filtra umo¿liwiaj±cy serwerowi Apache 2.0
wykonywaæ dynamiczne przekszta³cenia XML na statycznych dokumentach
XML lub dokumentach XML generowanych przez inny modu³ Apache'a lub
program CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}

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
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install src/.libs/libmod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/61_mod_transform.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc TODO
%attr(755,root,root) %{_pkglibdir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/*.conf
