%include /usr/lib/rpm/macros.python

Summary:	Tool for browsing CVS on the Web
Summary(pl):	Narz�dzie do przegl�dania CVS przez WWW
Name:		viewcvs
Version:	0.9.2
Release:	2.1
License:	distributable
Group:		Development/Tools
Source0:	http://viewcvs.sourceforge.net/viewcvs-0.9.2.tar.gz
Patch0:		%{name}-install_dir.patch
URL:		http://viewcvs.sourceforge.net/
BuildRequires:	python > 1.5
BuildRequires:	python-modules
BuildRequires:	perl
BuildRequires:	findutils
Requires:	enscript
Requires:	python > 1.5
Requires:	rcs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is tool for browsing CVS repositories on the Web. It has superior
feature set over cvsweb.

%description -l pl
Jest to narz�dzie do przegl�dania repozytori�w CVS poprzez WWW. Ma znacznie 
bogatsz� funkcjonalno�� od cvsweb.

%prep
%setup -q
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

echo "$RPM_BUILD_ROOT" | ./viewcvs-install

find $RPM_BUILD_ROOT -type f -exec \
	perl -pi -e \
	's@'$RPM_BUILD_ROOT'@@g;' {} \;

rm $RPM_BUILD_ROOT%{_libdir}/python2.2/site-packages/*.pyc
%{py_comp} $RPM_BUILD_ROOT%{_libdir}/python2.2/site-packages
%{py_ocomp} $RPM_BUILD_ROOT%{_libdir}/python2.2/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO LICENSE.html CHANGES website
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_libdir}/python2.2/site-packages/*.py[co]
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
/home/services/httpd/cgi-bin/*