#
#   RPM spec: buildpy, 2018 Sept 18
#
%define name        buildpy
%define version     MAJOR_VERSION
%define release     MINOR_VERSION
%define _bindir     usr/local/bin
%define _libdir     usr/local/lib/buildpy
%define _compdir    etc/bash_completion.d
%define _yumdir     etc/yum.repos.d
%define _logdir     var/log
%define _topdir     /home/DOCKERUSER/rpmbuild
%define buildroot   %{_topdir}/%{name}-%{version}

BuildRoot:      %{buildroot}
Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A Utility for Compiling and Installing Python3 on Linux

Group:          Development/Tools
BuildArch:      noarch
License:        GPL
URL:            https://buildpy.readthedocs.io
Source:         %{name}-%{version}.%{release}.tar.gz
Prefix:         /usr
Requires:      DEPLIST

%if 0%{?rhel}%{?amzn2}
Requires: bash-completion procps-ng
%endif

%if 0%{?amzn1}
Requires: epel-release procps
%endif

%description
Utility for compiling and installing any Python version
from source.
Supports Amazon Linux v1, Amazon Linux v2 (2018+),
CentOS 7, Redhat Enterprise Linux 6 and 7


%prep


%setup -q

%build


%install
install -m 0755 -d $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 -d $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 -d $RPM_BUILD_ROOT/%{_logdir}
install -m 0755 -d $RPM_BUILD_ROOT/%{_compdir}
install -m 0755 -d $RPM_BUILD_ROOT/%{_yumdir}
install -m 0755 buildpy $RPM_BUILD_ROOT/%{_bindir}/buildpy
install -m 0644 std_functions.sh $RPM_BUILD_ROOT/%{_libdir}/std_functions.sh
install -m 0644 os_distro.sh $RPM_BUILD_ROOT/%{_libdir}/os_distro.sh
install -m 0644 colors.sh $RPM_BUILD_ROOT/%{_libdir}/colors.sh
install -m 0644 exitcodes.sh $RPM_BUILD_ROOT/%{_libdir}/exitcodes.sh
install -m 0644 version.py $RPM_BUILD_ROOT/%{_libdir}/version.py
install -m 0444 bc.pkg $RPM_BUILD_ROOT/%{_libdir}/bc.pkg
install -m 0444 curl.pkg $RPM_BUILD_ROOT/%{_libdir}/curl.pkg
install -m 0444 gawk.pkg $RPM_BUILD_ROOT/%{_libdir}/gawk.pkg
install -m 0444 uninstall.paths $RPM_BUILD_ROOT/%{_libdir}/uninstall.paths
install -m 0644 buildpy-completion.bash $RPM_BUILD_ROOT/%{_compdir}/buildpy-completion.bash
install -m 0644 developer-tools.repo $RPM_BUILD_ROOT/%{_yumdir}/developer-tools.repo


%files
 %defattr(-,root,root)
/%{_libdir}
/%{_compdir}
/%{_yumdir}
/%{_bindir}/buildpy
%exclude /%{_libdir}/*.pyc
%exclude /%{_libdir}/*.pyo


%post  -p  /bin/bash

BIN_PATH=/usr/local/bin

##  finalize file ownership & permissions  ##

# log files
touch /var/log/buildpy.log
touch /var/log/console.log
chown root:root /var/log/buildpy.log
chown root:root /var/log/console.log
chmod 0666 /var/log/buildpy.log
chmod 0666 /var/log/console.log


##   ensure /usr/local/bin for python executables in PATH   ##

if [ ! "$(echo $PATH | grep '\/usr\/local\/bin')" ]; then

    # path updates - root user
    if [[ -f "$HOME/.bashrc" ]]; then
        printf -- '%s\n\n' 'PATH=$PATH:/usr/local/bin' >> "$HOME/.bashrc"
        printf -- '%s\n' 'export PATH' >> "$HOME/.bashrc"

    elif [[ -f "$HOME/.bash_profile" ]]; then
        printf -- '%s\n\n' 'PATH=$PATH:/usr/local/bin' >> "$HOME/.bash_profile"
        printf -- '%s\n' 'export PATH' >> "$HOME/.bash_profile"

    elif [[ -f "$HOME/.profile" ]]; then
        printf -- '%s\n\n' 'PATH=$PATH:/usr/local/bin' >> "$HOME/.profile"
        printf -- '%s\n' 'export PATH' >> "$HOME/.profile"

    fi

    # path updates - sudo user
    if [[ $SUDO_USER ]]; then

        if [[ -f "/home/$SUDO_USER/.bashrc" ]]; then
            printf -- '%s\n\n' 'PATH=$PATH:/usr/local/bin' >> "/home/$SUDO_USER/.bashrc"
            printf -- '%s\n' 'export PATH' >> "/home/$SUDO_USER/.bashrc"

        elif [[ -f "/home/$SUDO_USER/.bash_profile" ]]; then
            printf -- '%s\n\n' 'PATH=$PATH:/usr/local/bin' >> "/home/$SUDO_USER/.bash_profile"
            printf -- '%s\n' 'export PATH' >> "/home/$SUDO_USER/.bash_profile"

        elif [[ -f "/home/$SUDO_USER/.profile" ]]; then
            printf -- '%s\n\n' 'PATH=$PATH:/usr/local/bin' >> "/home/$SUDO_USER/.profile"
            printf -- '%s\n' 'export PATH' >> "/home/$SUDO_USER/.profile"

        fi

    fi
fi


# update sudoers path
if [[ -f /etc/sudoers ]]; then

    var=$(grep secure_path /etc/sudoers)
    cur_path="$(echo ${var##*=})"

    if [[ -z "$(echo $cur_path | grep $BIN_PATH)" ]]; then
        # append secure_path (single quotes mandatory)
        sed -i 's/secure_path\ =\ .*/secure_path\ =\ \/sbin:\/bin:\/usr\/sbin:\/usr\/bin:\/usr\/local\/bin/g' /etc/sudoers
    fi

fi


##   install bash_completion, amazonlinux 1   ##

if [[ -f '/usr/local/lib/buildpy/os_distro.sh' ]]; then
    if [[ "$(sh /usr/local/lib/buildpy/os_distro.sh | awk '{print $2}')" -eq "1" ]]; then
        yum -y install bash-completion --enablerepo=epel
    fi
fi


##   enable bash_completion   ##

# - /etc/bash_completion.d
# - /usr/local/etc/bash_completion.d
# - /usr/share/bash-completion/completions

if [[ -f '/etc/bash_completion' ]]; then
    . /etc/bash_completion

elif [[ -d '/etc/bash_completion.d' ]]; then
    . /etc/bash_completion.d/buildpy-completion.bash

elif [[ -f '/usr/share/bash-completion/bash_completion' ]]; then
    . /usr/share/bash-completion/bash_completion

elif [[ -f '/usr/local/etc/bash_completion.d/buildpy-completion.bash' ]]; then
    . /usr/local/etc/bash_completion.d/buildpy-completion.bash
fi


exit 0      ## post install end ##
