%define LNG ru
%define tarball_version 3.41-2145-1699-20120901

Summary:	Russian man (manual) pages from the Linux Documentation Project
Name:		man-pages-%{LNG}
Version:	3.41
Release:	17
License:	Distributable
Group:		System/Internationalization
Url:		http://www.linuxshare.ru/projects/trans/mans.html
Source0:	http://www.linuxshare.ru/projects/trans/manpages-ru-0.98.tar.bz2  
Source2:	man-pages-%{LNG}-goodies.tar.bz2
Source3:	man-pages-ru_%{tarball_version}.tar.bz2
BuildArch:	noarch
BuildRequires:	man
Requires:	locales-%{LNG}
Requires:	man
Requires(post):	sed grep man
Autoreq:	false

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Russian. 

%prep
%setup -q -n manpages-ru-0.98
cp %{SOURCE3} .
tar xjvf man-pages-ru_%{tarball_version}.tar.bz2
find man-pages-ru_%{tarball_version} -type f -exec gzip {} \;
if [[ -e man3/malloc.3.gz ]]
then
  rm -f man3/malloc.3.bz2
fi

%build

%install
mkdir -p %{buildroot}/%_mandir/%{LNG}/
mkdir -p %{buildroot}/var/catman/%{LNG}/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 3 4 5 6 7 8; do
	cp -adpvrf man$i %{buildroot}/%_mandir/%{LNG}/
	cp man-pages-ru_%{tarball_version}/man$i/* %{buildroot}/%_mandir/%{LNG}/man$i/
done

#tar jxf %SOURCE2 -C %{buildroot}/usr/share

# Drop the files provided by native packages
rm -f %{buildroot}/%{_mandir}/%{LNG}/man1/dosemu*
rm -f %{buildroot}/%{_mandir}/%{LNG}/man1/scmxx*
rm -f %{buildroot}/%{_mandir}/%{LNG}/man3/ipcalc_c*

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%_mandir/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %_mandir/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}

touch %{buildroot}/var/cache/man/%{LNG}/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%{LNG}, if there isn't any man page
   ## directory /%_mandir/%{LNG}
   if [ ! -d %_mandir/%{LNG} ] ; then
       rm -rf /var/catman/%{LNG}
   fi
fi

%post
%create_ghostfile /var/cache/man/%{LNG}/whatis root root 644

%files
%doc CREDITS FAQ NEWS
%dir %_mandir/%{LNG}
%dir /var/cache/man/%{LNG}
%ghost %config(noreplace) /var/cache/man/%{LNG}/whatis
%_mandir/%{LNG}/man*
%_mandir/%{LNG}/cat*
%_mandir/%{LNG}/CACHEDIR.TAG*
%_mandir/%{LNG}/index.db*
%attr(755,root,man) /var/catman/%{LNG}
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

