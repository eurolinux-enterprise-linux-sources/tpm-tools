Name:             tpm-tools
Summary:          Management tools for the TPM hardware
Version:          1.3.8
Release:          6%{?dist}
License:          CPL
Group:            Applications/System
URL:              http://trousers.sourceforge.net

Source0:          http://downloads.sourceforge.net/trousers/%{name}-%{version}.tar.gz
# Package unnecessarily has -Werror and any problem kills the build
Patch0:	          tpm-tools-1.3.5-no-werror.patch
# Package has other flaws preventing proper build
Patch1:           tpm-tools-1.3.7-build.patch

BuildRequires:    trousers-devel openssl-devel opencryptoki-devel chrpath
# Working with upstream to fix this, but in the mean time we need this
BuildRequires:    automake autoconf

%description
tpm-tools is a group of tools to manage and utilize the Trusted Computing
Group's TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's
software state using cryptographic hashes and more.

%package        pkcs11
Summary:        Management tools using PKCS#11 for the TPM hardware
Group:          Applications/System
# opencryptoki is dlopen'd, the Requires won't get picked up automatically
Requires:       opencryptoki-libs%{?_isa}

%description    pkcs11
tpm-tools-pkcs11 is a group of tools that use the TPM PKCS#11 token. All data
contained in the PKCS#11 data store is protected by the TPM (keys,
certificates, etc.). You can import keys and certificates, list out the
objects in the data store, and protect data.

%package        devel
Summary:        Files to use the library routines supplied with tpm-tools
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release} 

%description    devel
tpm-tools-devel is a package that contains the libraries and headers necessary
for developing tpm-tools applications.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
autoreconf

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/libtpm_unseal.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libtpm_unseal.a
chrpath -d %{buildroot}%{_bindir}/tpm_unsealdata
chrpath -d %{buildroot}%{_bindir}/tpm_sealdata

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README
%attr(755, root, root) %{_bindir}/tpm_*
%attr(755, root, root) %{_sbindir}/tpm_*
%attr(755, root, root) %{_libdir}/libtpm_unseal.so.?.?.?
%{_libdir}/libtpm_unseal.so.?
%{_mandir}/man1/tpm_*
%{_mandir}/man8/tpm_*

%files pkcs11
%doc LICENSE
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/tpmtoken_*
%{_mandir}/man1/tpmtoken_*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libtpm_unseal.so
%{_includedir}/tpm_tools/
%{_mandir}/man3/tpmUnseal*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.3.8-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.8-5
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.8-2
- Cleanup spec and modernise spec

* Fri Jun 22 2012 Steve Grubb <sgrubb@redhat.com> 1.3.8-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Steve Grubb <sgrubb@redhat.com> 1.3.7-1
- New upstream release

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> 1.3.5-5
- Remove -Werror from compile flags (#716046)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Michal Schmidt <mschmidt@redhat.com> - 1.3.5-3
- Add the LICENSE file to the -pkcs11 subpackage too, as it may be
  installed independently.
- Remove useless macros.

* Sun Feb 14 2010 Michal Schmidt <mschmidt@redhat.com> - 1.3.5-2
- Fix for DSO linking change.

* Mon Feb 01 2010 Steve Grubb <sgrubb@redhat.com> 1.3.5-1
- New upstream bug fix release

* Fri Jan 29 2010 Steve Grubb <sgrubb@redhat.com> 1.3.4-2
- Remove rpaths

* Wed Oct 21 2009 Michal Schmidt <mschmidt@redhat.com> - 1.3.4-1
- Upstream release 1.3.4:
  - adds SRK password support on unsealing
- LICENSE is back.
- Remove no longer needed patch:
  tpm-tools-1.3.3-check-fwrite-success.patch

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.3-2
- rebuilt with new openssl

* Fri Aug 07 2009 Michal Schmidt <mschmidt@redhat.com> 1.3.3-1
- New upstream release 1.3.3.
- No longer needed patch, dropped:
  tpm-tools-conditionally-build-tpmtoken-manpages-Makefile.in.patch
- Use global instead of define for macros.
- Remove rpaths.
- LICENSE file is suddenly missing in upstream tarball.
- Added patch to allow compilation:
  tpm-tools-1.3.3-check-fwrite-success.patch

* Wed Jul 29 2009 Michal Schmidt <mschmidt@redhat.com> 1.3.1-10
- Split the pkcs11 utilities into a subpackage.

* Wed Jul 29 2009 Michal Schmidt <mschmidt@redhat.com> 1.3.1-9
- Enable pkcs11 support (tpmtoken_* utilities).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.1-6
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.1-5
- Autorebuild for GCC 4.3

* Tue Dec 18 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1-4
- Updated for comments in RHIT#394941 comment #6
* Fri Dec 14 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1-3
- Updated to own the includedir/tpm_tools directory, removed
requirement on trousers and ldconfig in post/postun
* Thu Dec 13 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1-2
- Updated for Fedora package submission guidelines
* Fri Nov 16 2007 Kent Yoder <kyoder@users.sf.net> - 1.3.1
- Updates to configure
* Fri Oct 05 2007 Kent Yoder <kyoder@users.sf.net> - 1.2.5.1
- Updated build section to use smp_mflags

