Name:           vsftpd-ext
Version:        2.2.2
Release:        0.1.ext3%{?dist}
Epoch:		1
Summary:        Extended Very Secure Ftp Daemon

Group:          System Environment/Daemons
License:        GPLv2 with exceptions
URL:            http://vsftpd.devnet.ru/rus/
Source0:	http://vsftpd.devnet.ru/files/2.2.2/ext.3/vsFTPd-%{version}-ext3.tgz
Source1:        vsftpd.xinetd
Source2:        vsftpd.pam
Source3:        vsftpd.ftpusers
Source4:        vsftpd.user_list
Source5:        vsftpd.init
Source6:        vsftpd_conf_migrate.sh
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pam-devel
BuildRequires: libcap-devel
BuildRequires: openssl-devel
BuildRequires: tcp_wrappers-devel
Requires: logrotate
Requires (preun): /sbin/chkconfig
Requires (preun): /sbin/service
Requires (post): /sbin/chkconfig

Conflicts:	vsftpd

%description
vsftpd is a Very Secure FTP daemon. It was written completely from
scratch.


%prep
%setup -q -n vsFTPd-2.2.2-ext.3
cp %{SOURCE1} .

%build
%ifarch s390x sparcv9 sparc64
make CFLAGS="$RPM_OPT_FLAGS -fPIE -pipe -Wextra -Werror" \
%else
make CFLAGS="$RPM_OPT_FLAGS -fpie -pipe -Wextra -Werror" \
%endif
        LINK="-pie -lssl" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{vsftpd,pam.d,logrotate.d,rc.d/init.d}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{5,8}
install -m 755 vsftpd  $RPM_BUILD_ROOT%{_sbindir}/vsftpd
install -m 600 vsftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd.conf
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 RedHat/vsftpd.log $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/vsftpd
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vsftpd
install -m 600 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/ftpusers
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/user_list
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/vsftpd
install -m 744 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh

mkdir -p $RPM_BUILD_ROOT/%{_var}/ftp/pub


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add vsftpd


%preun
if [ $1 = 0 ]; then
 /sbin/service vsftpd stop > /dev/null 2>&1
 /sbin/chkconfig --del vsftpd
fi


%files
%defattr(-,root,root,-)
%{_sbindir}/vsftpd
%{_sysconfdir}/rc.d/init.d/vsftpd
%dir %{_sysconfdir}/vsftpd
%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh
%config(noreplace) %{_sysconfdir}/vsftpd/ftpusers
%config(noreplace) %{_sysconfdir}/vsftpd/user_list
%config(noreplace) %{_sysconfdir}/vsftpd/vsftpd.conf
%config(noreplace) %{_sysconfdir}/pam.d/vsftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/vsftpd
%doc FAQ INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD
%doc SPEED TODO BENCHMARKS COPYING SECURITY/ EXAMPLE/ TUNING SIZE vsftpd.xinetd
%{_mandir}/man5/vsftpd.conf.*
%{_mandir}/man8/vsftpd.*
%{_var}/ftp


%changelog
* Mon Nov 15 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.2-0.1.ext3
- do not Conflicts with vsftpd, only provides
- downgrade to 2.2.2 ext3. It must work

* Thu Oct 14 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.3.2-1
- rename package to vsftpd-ext

* Sat Aug 21 2010 Frolov Denis <d.frolov81@mail.ru> - 2.3.2-1
- Update to 2.3.2-ext1

* Sat Aug 14 2010 Frolov Denis <d.frolov81@mail.ru> - 2.3.0-1
- Update to 2.3.0-ext1

* Thu Apr 06 2010 Frolov Denis <d.frolov81@mail.ru> - 2.2.2-2
- Update to 2.2.2-ext1 patch

* Mon Jan 04 2010 Frolov Denis <d.frolov81@mail.ru> - 2.2.2-1
- Update to 2.2.2-1

* Mon Jul 06 2009 Frolov Denis <d.frolov81@mail.ru> - 2.1.2-1
- Update to 2.1.2

* Wed Apr 07 2009 Frolov Denis <d.frolov81@mail.ru> - 2.1.0-2
- Rebuild with http://vsftpd.devnet.ru/
