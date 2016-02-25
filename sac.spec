%global pkg_name sac
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name: %{?scl_prefix}%{pkg_name}
Version: 1.3
Release: 17.13%{?dist}
Summary: Java standard interface for CSS parser
License: W3C
#Original source: http://www.w3.org/2002/06/%{pkg_name}java-%{version}.zip
#unzip, find . -name "*.jar" -exec rm {} \;
#to simplify the licensing
Source0: %{pkg_name}java-%{version}-jarsdeleted.zip
Source1: %{pkg_name}-build.xml
Source2: %{pkg_name}-MANIFEST.MF
Source3: http://mirrors.ibiblio.org/pub/mirrors/maven2/org/w3c/css/sac/1.3/sac-1.3.pom
URL: http://www.w3.org/Style/CSS/SAC/
BuildRequires: %{?scl_prefix_java_common}ant
BuildRequires: %{?scl_prefix_java_common}javapackages-tools
BuildRequires: zip
BuildArch: noarch

%description
SAC is a standard interface for CSS parsers, intended to work with CSS1, CSS2,
CSS3 and other CSS derived languages.

%package javadoc
Summary: Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
install -m 644 %{SOURCE1} build.xml
find . -name "*.jar" -exec rm -f {} \;
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
ant jar javadoc
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/sac.jar META-INF/MANIFEST.MF

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p ./build/lib/sac.jar $RPM_BUILD_ROOT%{_javadir}/sac.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE3} \
    %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom

%add_maven_depmap
%{?scl:EOF}

%files -f .mfiles
%defattr(-,root,root,-)
%doc COPYRIGHT.html

%files javadoc
%defattr(-,root,root,-)
%doc COPYRIGHT.html
%{_javadocdir}/%{name}

%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 1.3-17.13
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.3-17.12
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.3-17.11
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.3-17.10
- Mass rebuild 2015-01-13

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.3-17.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.3-17.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-17.1
- First maven30 software collection build

* Wed Jan 08 2014 Caolán McNamara <caolanm@redhat.com> - 1.3-17
- Resolves: rhbz#1027720 Use add_maven_depmap instead of deprecated macros

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3-16
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Caolán McNamara <caolanm@redhat.com> - 1.3-14
- repack zip to drop jars

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Caolán McNamara <caolanm@redhat.com> - 1.3-11
- Resolves: rhbz#715875 FTBFS

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 1.3-9
- Drop gcj.
- Adapt to current guidelines.

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 1.3-8
- add COPYING to all subpackages

* Mon May 31 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.3-7
- Fix spelling of my surname in %%changelog.

* Wed Mar 24 2010 Alexander Kurtakov <akurtako@redhat.com> 1.3-6
- Add maven pom and metadata.

* Fri Jul 24 2009 Caolán McNamara <caolanm@redhat.com> - 1.3-5
- make javadoc no-arch when building as arch-dependant aot

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 6 2009 Alexander Kurtakov <akurtako@redhat.com> 1.3-3.3
- Add osgi manifest (needed by eclipse-birt).

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-3.2
- drop repotag

* Fri May 09 2008 Caolán McNamara <caolanm@redhat.com> 1.3-3jpp.1
- update for guidelines

* Sat May 03 2008 Caolán McNamara <caolanm@redhat.com> 1.3-3jpp
- import from jpackage

* Fri Sep 03 2004 Fernando Nasser <fnasser@redhat.com> 1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 1.3-2jpp
- update for JPackage 1.5

* Thu Jul 11 2002 Ville Skyttä <ville.skytta@iki.fi> 1.3-1jpp
- Update to 1.3.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Add Distribution tag, fix URL, tweak Summary and description.

* Wed Feb 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp 
- first jpp release
