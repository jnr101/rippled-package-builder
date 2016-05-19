%define rippled_version %(echo $RIPPLED_RPM_VERSION)
%define rpm_release %(echo $RPM_RELEASE)
%define         debug_package
%define _prefix /opt/ripple
Name:           rippled
# Dashes in Version extensions must be converted to underscores
Version:        %{rippled_version}
Release:        %{rpm_release}%{?dist}
Summary:        rippled daemon

License:        MIT
URL:            http://ripple.com/
Source0:        rippled.tar.gz
Source1:        rippled.service
Source2:        50-rippled.preset
Source3:        update-rippled.sh
Source4:        nofile_limit.conf
Source5:        Manifest
Source6:        configure-validator.sh

BuildRequires:  scons boost-devel protobuf-devel openssl-devel

%description
rippled

%prep
%setup -n rippled

%build
RIPPLED_OLD_GCC_ABI=0 scons %{?_smp_mflags} --static

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}/
echo "Installing to /opt/ripple/"
install -D doc/rippled-example.cfg ${RPM_BUILD_ROOT}%{_prefix}/etc/rippled.cfg
install -d ${RPM_BUILD_ROOT}/etc/opt/ripple
ln -s %{_prefix}/etc/rippled.cfg ${RPM_BUILD_ROOT}/etc/opt/ripple/rippled.cfg
install -D build/gcc.release/rippled ${RPM_BUILD_ROOT}%{_bindir}/rippled
install -D %{SOURCE1} ${RPM_BUILD_ROOT}/usr/lib/systemd/system/rippled.service
install -D %{SOURCE2} ${RPM_BUILD_ROOT}/usr/lib/systemd/system-preset/50-rippled.preset
install -D %{SOURCE3} ${RPM_BUILD_ROOT}%{_bindir}/update-rippled.sh
install -d ${RPM_BUILD_ROOT}/etc/systemd/system/rippled.service.d/
install -D %{SOURCE4} ${RPM_BUILD_ROOT}/etc/systemd/system/rippled.service.d/nofile_limit.conf
install -D %{SOURCE5} ${RPM_BUILD_ROOT}%{_bindir}/manifest
install -D %{SOURCE6} ${RPM_BUILD_ROOT}%{_bindir}/configure-validator.sh

install -d $RPM_BUILD_ROOT/var/log/rippled
install -d $RPM_BUILD_ROOT/var/lib/rippled

%post
USER_NAME=rippled
GROUP_NAME=rippled

getent passwd $USER_NAME &>/dev/null || useradd $USER_NAME
getent group $GROUP_NAME &>/dev/null || groupadd $GROUP_NAME

chown -R $USER_NAME:$GROUP_NAME /var/log/rippled/
chown -R $USER_NAME:$GROUP_NAME /var/lib/rippled/
chown -R $USER_NAME:$GROUP_NAME %{_prefix}/

chmod 755 /var/log/rippled/
chmod 755 /var/lib/rippled/

%files
%doc README.md LICENSE
%{_bindir}/rippled
%{_bindir}/update-rippled.sh
%{_bindir}/manifest
%{_bindir}/configure-validator.sh
%config(noreplace) %{_prefix}/etc/rippled.cfg
%config(noreplace) /etc/opt/ripple/rippled.cfg
%config(noreplace) /usr/lib/systemd/system/rippled.service
%config(noreplace) /usr/lib/systemd/system-preset/50-rippled.preset
%config(noreplace) /etc/systemd/system/rippled.service.d/nofile_limit.conf
%dir /var/log/rippled/
%dir /var/lib/rippled/

%changelog
