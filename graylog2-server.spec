# TODO
# - run as dedicated user
Summary:	A syslog implementation that stores logs in MongoDB
Name:		graylog2-server
Version:	0.9.6p1
Release:	0.2
License:	GPL v3
Group:		Daemons
URL:		http://www.graylog2.org/
Source0:	https://github.com/downloads/Graylog2/graylog2-server/%{name}-%{version}.tar.gz
# Source0-md5:	499ae16dcae71eeb7c3a30c75ea7a1a6
Source1:	%{name}.init
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	jre >= 1.6
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Graylog2 is an open source syslog implementation that stores logs in
MongoDB. It consists of a server written in Java that accepts syslog
messages via TCP or UDP and stores them in the database.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_javadir},%{_initrddir}}
# Install the application
cp -p %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Install the config file
cp -p graylog2.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/graylog2.conf

# Install the init script
install -d $RPM_BUILD_ROOT
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# Create the log directory
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = 0 ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README graylog2.conf.example build_date
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/graylog2.conf
%attr(754,root,root) /etc/rc.d/init.d/graylog2-server
%{_javadir}/graylog2-server*.jar
%dir %{_localstatedir}/log/%{name}
