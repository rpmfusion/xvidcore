Name:           xvidcore
Version:        1.1.3
Release:        4%{?dist}
Summary:        Free reimplementation of the OpenDivX video codec

Group:          System Environment/Libraries
License:        XVID (GPL with specific restrictions)
URL:            http://www.xvid.org/
Source0:        http://downloads.xvid.org/downloads/xvidcore-%{version}.tar.bz2
Patch0:         %{name}-noexecstack.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
Free reimplementation of the OpenDivX video codec. You can play OpenDivX
and DivX4 videos with it, as well as encode compatible files.

%package        devel
Summary:        Development files for the XviD video codec
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files, static library and API
documentation for the XviD video codec.


%prep
%setup -q
%patch0 -p1 -b .noexec
chmod -x examples/*.pl
f=AUTHORS ; iconv -f iso-8859-1 -t utf-8 -o $f.utf8 $f ; mv $f.utf8 $f
# Yes, we want to see the build output.
%{__perl} -pi -e 's/^\t@(?!echo\b)/\t/' build/generic/Makefile


%build
cd build/generic
export CFLAGS="$RPM_OPT_FLAGS -ffast-math"
%configure
make %{?_smp_mflags} 
cd -


%install
rm -rf $RPM_BUILD_ROOT
make -C build/generic install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libxvidcore.a
cd $RPM_BUILD_ROOT%{_libdir}
chmod 755 libxvidcore.so*
/sbin/ldconfig -n .
ln -s libxvidcore.so.? libxvidcore.so
cd -


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README AUTHORS ChangeLog TODO
%{_libdir}/libxvidcore.so.*

%files devel
%defattr(-,root,root,-)
%doc CodingStyle examples/
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so


%changelog
* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.1.3-4
- rebuild

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.3-3
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 3 to be higher as both livna and freshrpms latest release
- Add -ffast-math to CFLAGS

* Sat Jun 30 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.1.3-1
- 1.1.3, security bugfix release, fixes CVE-2007-3329 (#1563)

* Sun Mar 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.1.2-2
- fix SElinux noexec stack issue (patch by Hans de Goede)

* Sat Nov 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.2-1
- 1.1.2.
- Convert docs to UTF-8.
- Use make install DESTDIR=... instead of %%makeinstall.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.1.0-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-3
- Use yasm to build, enable asm code on x86_64.
- Drop no longer needed Obsoletes.
- Specfile cleanups.

* Sat May 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-2
- Fix library permissions and symlink.
- Don't ship static library.
- Avoid -devel dependency on perl.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Jan 18 2006 Adrian Reber <adrian@lisas.de> - 1.1.0-0.lvn.1
- Updated to 1.10
- Droped now unnecessary patch
- Droped Epoch

* Sun Feb 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.3-0.lvn.1
- 1.0.3.

* Wed Sep 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.2-0.lvn.1
- Update to 1.0.2.

* Tue Jun  8 2004 Dams <anvil[AT]livna.org> 0:1.0.1-0.lvn.1
- Updated to 1.0.1

* Mon May 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.1
- Updated to 1.0.0.
- Patch to show build output.

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.0.2.rc4
- Updated to 1.0.0-rc4.

* Mon Mar 29 2004 Dams <anvil[AT]livna.org> 0:1.0.0-0.lvn.0.2.rc3
- Updated to rc3

* Sat Jan 10 2004 Dams <anvil[AT]livna.org> 0:1.0.0-0.lvn.0.1.beta3
- Updated to 1.0.0-beta3
- Small spec file cleanup

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.1.0.94
- Removed comment after scriptlets

* Fri Aug 15 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:0.9.2-0.fdr.1
- Updated to 0.9.2.
- Updated according to current SPEC template.
- Changed to properly versioned .so-files.

* Tue Apr  8 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.3
- Cleaned up the documentation.

* Fri Apr  4 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.2
- Added epoch and release number to requires.

* Wed Apr  2 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.1
- Updated to 0.9.1.

* Wed Apr  2 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.0-0.fdr.1
- Initial fedora RPM release.
- Changed -static back to -devel as that seems more logic.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Wed Jan 29 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the location of the .h files... doh!

* Sun Jan 12 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Remove the decore.h and encore2.h inks as divx4linux 5.01 will provide them.
- Rename -devel to -static as it seems more logic.

* Fri Dec 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
