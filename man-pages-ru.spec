%define LANG ru

Summary: Russian man (manual) pages from the Linux Documentation Project
Name: man-pages-%LANG
Version: 0.98
Release: %mkrel 1
License: Distributable
Group: System/Internationalization
Source: http://www.linuxshare.ru/projects/trans/manpages-ru-%{version}.tar.bz2  
Source2: man-pages-%LANG-goodies.tar.bz2
URL: http://www.linuxshare.ru/projects/trans/mans.html
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG, man => 1.5j-8mdk
Requires(post): sed grep man
Autoreq: false
BuildArch: noarch
Obsoletes: man-%LANG, manpages-%LANG
Provides: man-%LANG, manpages-%LANG


%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Russian. 

%prep

%setup -q -n manpages-ru-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/%LANG/
mkdir -p $RPM_BUILD_ROOT/var/catman/%LANG/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 5 7 8; do
	cp -adpvrf man$i $RPM_BUILD_ROOT/%_mandir/%LANG/
done

tar jxf %SOURCE2 -C $RPM_BUILD_ROOT/usr/share

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory /%_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
       rm -rf /var/catman/%LANG
   fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755) 
%doc CREDITS FAQ NEWS
%defattr(0644,root,man,755)
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
%_mandir/%LANG/man*
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron

