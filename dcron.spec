Summary:	Dillon's Cron Daemon
Name:		dcron
Version:	3.2
Release:	%mkrel 4
License:	GPL+
Group:		System/Servers
URL:		http://apollo.backplane.com/FreeSrc/
Source0:	http://apollo.backplane.com/FreeSrc/dcron32.tgz
Source1:	dcron.init.bz2
Source2:	etc-crontab.bz2
Patch0:		dcron-3.2-pid_and_mailer.diff
Patch1:		dcron-3.2-openpkg.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	syslog-daemon
Requires:	sendmail-command
Conflicts:	vixie-cron
Conflicts:	crontabs
Provides:	cron-daemon
#Provides:	crond, crontabs
BuildRequires:	dietlibc-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A multiuser cron written from scratch, dcron is follows concepts
of vixie-cron but has significant differences. Less attention is
paid to feature development in favor of usability and reliability.

%prep

%setup -q -n dcron
%patch0 -p1 -b .pidmailer
%patch1 -p0

perl -pi -e "s|VISUAL|EDITOR|g" crontab.*

bzcat %{SOURCE1} > dcron.init
bzcat %{SOURCE2} > etc-crontab

%build
make CC="diet gcc" CFLAGS="-Os -Wall"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/cron.{hourly,daily,weekly,monthly}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_mandir}/man{1,8}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/spool/dcron/crontabs

install -m0755 crontab %{buildroot}%{_bindir}/
install -m0755 crond %{buildroot}%{_sbindir}/
install -m0644 crontab.1 %{buildroot}%{_mandir}/man1/
install -m0644 crond.8 %{buildroot}%{_mandir}/man8/

install -m0755 dcron.init %{buildroot}%{_initrddir}/dcron
install -m0644 etc-crontab %{buildroot}%{_sysconfdir}/crontab

%post
if [[ -z `crontab -l | grep run-parts` ]]; then
    echo "Adding the \"system crontab\" to emulate vixie-cron"
    /bin/grep "^[0-9]" %{_sysconfdir}/crontab | %{_bindir}/crontab -
fi
%_post_service %{name}
  
%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG README
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/crontab
%attr(0755,root,cron) %{_initrddir}/dcron
%dir %attr(0750,root,root) %{_sysconfdir}/cron.hourly
%dir %attr(0750,root,root) %{_sysconfdir}/cron.daily
%dir %attr(0750,root,root) %{_sysconfdir}/cron.weekly
%dir %attr(0750,root,root) %{_sysconfdir}/cron.monthly
%attr(4750,root,cron) %{_bindir}/crontab
%attr(0755,root,wheel)%{_sbindir}/crond
%{_mandir}/man1/crontab.1*
%{_mandir}/man8/crond.8*
%dir %attr(0755,root,root) /var/spool/dcron/crontabs


%changelog
* Wed Jun 17 2009 Jérôme Brenier <incubusss@mandriva.org> 3.2-4mdv2010.0
+ Revision: 386539
- rediff PO

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 3.2-3mdv2009.0
+ Revision: 266556
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2-2mdv2009.0
+ Revision: 217538
- rebuilt against dietlibc-devel-0.32

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 17 2007 Adam Williamson <awilliamson@mandriva.org> 3.2-1mdv2008.0
+ Revision: 64681
- provide cron-daemon
- use Fedora license policy (GPL+)
- update patch1 from openpkg
- rediff patch0
- new release 3.2


* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9-2mdv2007.0
+ Revision: 101636
- Import dcron

* Wed Sep 13 2006 Oden Eriksson <oeriksson@mandriva.com> 2.9-2mdv2007.0
- rebuild

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.9-1mdk
- initial Mandriva package
- used parts from my first annvix package and also ideas from
  the latest annvix package (thanks vdanen)
- added P0 and P1 which originates from openpkg and FJO

