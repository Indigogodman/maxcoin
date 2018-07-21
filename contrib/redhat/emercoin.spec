Name:           supermaxcoin
Version:        0.6.3
Release:        1%{?dist}
Summary:        supermaxcoin Wallet
Group:          Applications/Internet
Vendor:         supermaxcoin
License:        GPLv3
URL:            https://www.supermaxcoin.com
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  autoconf automake libtool gcc-c++ openssl-devel >= 1:1.0.2d libdb4-devel libdb4-cxx-devel miniupnpc-devel boost-devel boost-static
Requires:       openssl >= 1:1.0.2d libdb4 libdb4-cxx miniupnpc logrotate

%description
supermaxcoin Wallet

%prep
%setup -q

%build
./autogen.sh
./configure
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/etc/supermaxcoin $RPM_BUILD_ROOT/etc/ssl/emc $RPM_BUILD_ROOT/var/lib/emc/.supermaxcoin $RPM_BUILD_ROOT/usr/lib/systemd/system $RPM_BUILD_ROOT/etc/logrotate.d
%{__install} -m 755 src/supermaxcoind $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 src/supermaxcoin-cli $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 600 contrib/redhat/supermaxcoin.conf $RPM_BUILD_ROOT/var/lib/emc/.supermaxcoin
%{__install} -m 644 contrib/redhat/supermaxcoind.service $RPM_BUILD_ROOT/usr/lib/systemd/system
%{__install} -m 644 contrib/redhat/supermaxcoind.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/supermaxcoind
%{__mv} -f contrib/redhat/emc $RPM_BUILD_ROOT%{_bindir}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pretrans
getent passwd emc >/dev/null && { [ -f /usr/bin/supermaxcoind ] || { echo "Looks like user 'emc' already exists and have to be deleted before continue."; exit 1; }; } || useradd -r -M -d /var/lib/emc -s /bin/false emc

%post
[ $1 == 1 ] && {
  sed -i -e "s/\(^rpcpassword=MySuperPassword\)\(.*\)/rpcpassword=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)/" /var/lib/emc/.supermaxcoin/supermaxcoin.conf
  openssl req -nodes -x509 -newkey rsa:4096 -keyout /etc/ssl/emc/supermaxcoin.key -out /etc/ssl/emc/supermaxcoin.crt -days 3560 -subj /C=US/ST=Oregon/L=Portland/O=IT/CN=supermaxcoin.emc
  ln -sf /var/lib/emc/.supermaxcoin/supermaxcoin.conf /etc/supermaxcoin/supermaxcoin.conf
  ln -sf /etc/ssl/emc /etc/supermaxcoin/certs
  chown emc.emc /etc/ssl/emc/supermaxcoin.key /etc/ssl/emc/supermaxcoin.crt
  chmod 600 /etc/ssl/emc/supermaxcoin.key
} || exit 0

%posttrans
[ -f /var/lib/emc/.supermaxcoin/addr.dat ] && { cd /var/lib/emc/.supermaxcoin && rm -rf database addr.dat nameindex* blk* *.log .lock; }
sed -i -e 's|rpcallowip=\*|rpcallowip=0.0.0.0/0|' /var/lib/emc/.supermaxcoin/supermaxcoin.conf
systemctl daemon-reload
systemctl status supermaxcoind >/dev/null && systemctl restart supermaxcoind || exit 0

%preun
[ $1 == 0 ] && {
  systemctl is-enabled supermaxcoind >/dev/null && systemctl disable supermaxcoind >/dev/null || true
  systemctl status supermaxcoind >/dev/null && systemctl stop supermaxcoind >/dev/null || true
  pkill -9 -u emc > /dev/null 2>&1
  getent passwd emc >/dev/null && userdel emc >/dev/null 2>&1 || true
  rm -f /etc/ssl/emc/supermaxcoin.key /etc/ssl/emc/supermaxcoin.crt /etc/supermaxcoin/supermaxcoin.conf /etc/supermaxcoin/certs
} || exit 0

%files
%doc COPYING
%attr(750,emc,emc) %dir /etc/supermaxcoin
%attr(750,emc,emc) %dir /etc/ssl/emc
%attr(700,emc,emc) %dir /var/lib/emc
%attr(700,emc,emc) %dir /var/lib/emc/.supermaxcoin
%attr(600,emc,emc) %config(noreplace) /var/lib/emc/.supermaxcoin/supermaxcoin.conf
%attr(4750,emc,emc) %{_bindir}/supermaxcoin-cli
%defattr(-,root,root)
%config(noreplace) /etc/logrotate.d/supermaxcoind
%{_bindir}/supermaxcoind
%{_bindir}/emc
/usr/lib/systemd/system/supermaxcoind.service

%changelog
* Thu Aug 31 2017 Aspanta Limited <info@aspanta.com> 0.6.3
- There is no changelog available. Please refer to the CHANGELOG file or visit the website.
