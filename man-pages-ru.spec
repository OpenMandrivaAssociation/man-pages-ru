%define LNG ru

Summary: Russian man (manual) pages from the Linux Documentation Project
Name: man-pages-%LNG
Version: 0.98
Release: %mkrel 8
License: Distributable
Group: System/Internationalization
Source: http://www.linuxshare.ru/projects/trans/manpages-ru-%{version}.tar.bz2  
Source2: man-pages-%LNG-goodies.tar.bz2
URL: http://www.linuxshare.ru/projects/trans/mans.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LNG, man => 1.5j-8mdk
Requires(post): sed grep man
Autoreq: false
BuildArch: noarch
Obsoletes: man-%LNG, manpages-%LNG
Provides: man-%LNG, manpages-%LNG


%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Russian. 

%prep

%setup -q -n manpages-ru-%version

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/%LNG/
mkdir -p %{buildroot}/var/catman/%LNG/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 5 7 8; do
	cp -adpvrf man$i %{buildroot}/%_mandir/%LNG/
done

tar jxf %SOURCE2 -C %{buildroot}/usr/share

LANG=%LNG DESTDIR=%{buildroot} %{_sbindir}/makewhatis %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_sbindir}/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       rm -rf /var/catman/%LNG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755) 
%doc CREDITS FAQ NEWS
%defattr(0644,root,man,755)
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%_mandir/%LNG/whatis
%attr(755,root,man) /var/catman/%LNG
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
