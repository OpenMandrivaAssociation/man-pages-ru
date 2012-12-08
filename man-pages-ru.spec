%define LNG ru

Summary: Russian man (manual) pages from the Linux Documentation Project
Name: man-pages-%LNG
Version: 0.98
Release: 14
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

#Some hacks
rm -f %{buildroot}/%{_mandir}/%LNG/man1/dosemu*

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


%changelog
* Sun Aug 14 2011 Александр Казанцев <kazancas@mandriva.org> 0.98-10mdv2011.0
+ Revision: 694452
- add new ru manpages.

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.98-9
+ Revision: 666376
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.98-8mdv2011.0
+ Revision: 609327
- rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.98-7mdv2011.0
+ Revision: 609310
- fix build
- fix typos
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.98-5mdv2009.1
+ Revision: 351585
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.98-4mdv2009.0
+ Revision: 223194
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.98-3mdv2008.1
+ Revision: 152996
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Apr 23 2007 Thierry Vignaud <tv@mandriva.org> 0.98-1mdv2008.0
+ Revision: 17425
- kill icon
- new release


* Wed May 10 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.97-3mdk
- fix post scripts (thx gwenole)

* Wed May 10 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.97-2mdk
- use %%mkrel
- rpmlint cleanups

* Thu Jul 29 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.97-1mdk
- new release

* Thu Jul 24 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 0.7-2mdk
- rebuild

