%{?scl:%scl_package sac}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name: %{?scl_prefix}sac
Version: 1.3
Release: 23.%{baserelease}%{?dist}
Summary: Java standard interface for CSS parser
License: W3C
Group: System Environment/Libraries
#Original source: http://www.w3.org/2002/06/%{pkg_name}java-%{version}.zip
#unzip, find . -name "*.jar" -exec rm {} \;
#to simplify the licensing
Source0: %{pkg_name}java-%{version}-jarsdeleted.zip
Source1: %{pkg_name}-build.xml
Source2: %{pkg_name}-MANIFEST.MF
Source3: https://repo1.maven.org/maven2/org/w3c/css/sac/1.3/sac-1.3.pom
URL: http://www.w3.org/Style/CSS/SAC/
BuildRequires: %{?scl_prefix_java_common}ant, %{?scl_prefix_java_common}jpackage-utils, zip
Requires:%{?scl_prefix_java_common}jpackage-utils
BuildArch: noarch

%description
SAC is a standard interface for CSS parsers, intended to work with CSS1, CSS2,
CSS3 and other CSS derived languages.

%package javadoc
Group: Development/Java
Summary: Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q
install -m 644 %{SOURCE1} build.xml
find . -name "*.jar" -exec rm -f {} \;
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
ant jar javadoc
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/sac.jar META-INF/MANIFEST.MF

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p ./build/lib/sac.jar $RPM_BUILD_ROOT%{_javadir}/sac.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE3} \
    %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom

%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar
%{?scl:EOF}


%files
%doc COPYRIGHT.html
%{_javadir}/%{pkg_name}.jar
%{_mavenpomdir}/*
%{_datadir}/maven-metadata/*

%files javadoc
%doc COPYRIGHT.html
%{_javadocdir}/%{pkg_name}

%changelog
* Thu Jul 21 2016 Mat Booth <mat.booth@redhat.com> - 1.3-23.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Feb 23 2016 Sopot Cela <scela@redhat.com> - 1.3-23
- Changed broken Source3: URL

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 10 2014 David Tardon <dtardon@redhat.com> - 1.3-20
- Resolves: rhbz#1107270 fix FTBFS

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Caolán McNamara <caolanm@redhat.com> - 1.3-18
- Resolves: rhbz#1068513 switch to java-headless (build)requires

* Wed Aug 21 2013 Mat Booth <fedora@matbooth.co.uk> - 1.3-17
- Update for newer guidelines, rhbz #993211

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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