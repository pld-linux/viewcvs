%include /usr/lib/rpm/macros.python

Summary:	Tool for browsing CVS on the Web
Summary(pl):	Narzêdzie do przegl±dania CVS przez WWW
Name:		viewcvs
Version:	0.9.2
Release:	2.7
License:	distributable
Group:		Development/Tools
Source0:	http://viewcvs.sourceforge.net/viewcvs-0.9.2.tar.gz
# Source0-md5:	c7857b1ed05240ad1f691ea40044daf2
Patch0:		%{name}-install_dir.patch
Patch1:		%{name}-pager.patch
Patch2:		%{name}-enscript.patch
URL:		http://viewcvs.sourceforge.net/
BuildRequires:	python > 1.5
BuildRequires:	python-modules
BuildRequires:	perl-base
BuildRequires:	findutils
BuildRequires:	sed	
Requires:	enscript
Requires:	python > 1.5
Requires:	rcs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is tool for browsing CVS repositories on the Web. It has superior
feature set over cvsweb.

%description -l pl
Jest to narzêdzie do przegl±dania repozytoriów CVS poprzez WWW. Ma znacznie
bogatsz± funkcjonalno¶æ od cvsweb.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%define	_py_sitedir %(echo "%{py_sitedir}" | sed -e 's@/@@')
echo "$RPM_BUILD_ROOT" | ./viewcvs-install "%{_py_sitedir}"

find $RPM_BUILD_ROOT -type f -exec \
	%{__perl} -pi -e \
	's@'$RPM_BUILD_ROOT'@@g;' {} \;

# Hell, I don't know how to make apache to run *.pyo via python :(
# Nasty hack but it seems that there is no way to compile non-.py files.
#for f in $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/*; do mv "$f" "$f.py"; done
#%%{py_comp} $RPM_BUILD_ROOT/home/services/httpd/cgi-bin
#%%{py_ocomp} $RPM_BUILD_ROOT/home/services/httpd/cgi-bin
#rm $RPM_BUILD_ROOT/home/services/httpd/cgi-bin/*.py

%{py_comp} $RPM_BUILD_ROOT%{py_sitedir}
%{py_ocomp} $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO LICENSE.html CHANGES website
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{py_sitedir}/*.py[co]
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
%attr(755,root,root) /home/services/httpd/cgi-bin/*
