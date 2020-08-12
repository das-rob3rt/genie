###############################################################################
# Spec file for Utils
################################################################################
# Configured to be built by user student or other non-root user
################################################################################
#
Summary: A quick way into a systemd "bottle" for WSL
Name: systemd-genie
Version: 1.26
Release: 1
License: Unlicense
URL: https://github.com/arkane-systems/genie
Group: System
Packager: Robert Wang
Requires: bash
Requires: screen
Requires: mc
Requires: dmidecode
BuildRoot: ~/rpmbuild/

# Build with the following syntax:
# rpmbuild --target noarch -bb utils.spec

%description
A quick way into a systemd "bottle" for WSL

%prep
################################################################################
# Create the build tree and copy the files from the development directories    #
# into the build tree.                                                         #
################################################################################
echo "BUILDROOT = $RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/
mkdir -p $RPM_BUILD_ROOT/usr/local/share/utils

cp /home/student/development/scripts/* $RPM_BUILD_ROOT/usr/local/bin
cp /home/student/development/license/* $RPM_BUILD_ROOT/usr/local/share/utils
cp /home/student/development/spec/* $RPM_BUILD_ROOT/usr/local/share/utils

exit

%files
%attr(0744, root, root) /usr/local/bin/*
%attr(0644, root, root) /usr/local/share/utils/*

%pre

%post
################################################################################
# Set up MOTD scripts                                                          #
################################################################################
cd /etc
# Save the old MOTD if it exists
if [ -e motd ]
then
   cp motd motd.orig
fi
# If not there already, Add link to create_motd to cron.daily
cd /etc/cron.daily
if [ ! -e create_motd ]
then
   ln -s /usr/local/bin/create_motd
fi
# create the MOTD for the first time
/usr/local/bin/mymotd > /etc/motd


%postun
# remove installed files and links
rm /etc/cron.daily/create_motd

# Restore the original MOTD if it was backed up
if [ -e /etc/motd.orig ]
then
   mv -f /etc/motd.orig /etc/motd
fi

%clean
rm -rf $RPM_BUILD_ROOT/usr/local/bin
rm -rf $RPM_BUILD_ROOT/usr/local/share/utils

%changelog
* Wed Aug 29 2018 Your Name <Youremail@yourdomain.com>
  - The original package includes several useful scripts. it is
    primarily intended to be used to illustrate the process of
    building an RPM.
