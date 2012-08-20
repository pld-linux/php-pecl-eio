%define		modname	eio
Summary:	Extension to provide interface to the libeio library
Name:		php-pecl-%{modname}
Version:	1.2.0
Release:	0.1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	18505c41fb1ca2a2b5024c50c0de719f
URL:		http://pecl.php.net/package/eio
BuildRequires:	libeio-devel
BuildRequires:	php-devel >= 4:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.519
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides interface to the libeio library.

Libeio is a an asynchronous I/O library. Features basically include
asynchronous versions of POSIX API(read, write, open, close, stat, unlink,
fdatasync, mknod, readdir etc.); sendfile (native on Solaris, Linux, HP-UX,
FreeBSD); readahead. libeio itself emulates the system calls, if they are not
available on specific(UNIX-like) platform.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
