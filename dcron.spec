Summary:	Dillon's Cron Daemon
Name:		dcron
Version:	2.9
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
URL:		http://apollo.backplane.com/FreeSrc/
Source0:	http://apollo.backplane.com/FreeSrc/dcron29.tar.bz2
Source1:	dcron.init.bz2
Source2:	etc-crontab.bz2
Patch0:		dcron-2.9-pid_and_mailer.diff
Patch1:		dcron-2.9-openpkg.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	syslog-daemon
Requires:	sendmail-command
Conflicts:	vixie-cron
Conflicts:	crontabs
#Provides:	crond, crontabs
BuildRequires:	dietlibc-devel >= 0.20-1mdk
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
A multiuser cron written from scratch, dcron is follows concepts
of vixie-cron but has significant differences. Less attention is
paid to feature development in favor of usability and reliability.

%prep

%setup -q -n dcron
%patch0 -p1
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


