# TODO:
#  - do sth with apache modules
#  - check patch1

Summary:	Tool for browsing CVS on the Web
Summary(pl):	Narzêdzie do przegl±dania CVS przez WWW
Name:		viewcvs
Version:	1.0
Release:	0.dev.20051002cvs.0.1
License:	BSD
Group:		Development/Tools
# this is version from official cvs -- just packed
Source0:	%{name}.tar.gz
# Source0-md5:
Patch0:		%{name}-install_dir.patch
#check this
Patch1:		%{name}-pager.patch
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
%setup -q -n viewcvs
%patch0 -p1
#%%patch1 -p1

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
%doc README TODO CHANGES website INSTALL
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{py_sitedir}/*.py[co]
%{py_sitedir}/vclib/*.py[co]
%{py_sitedir}/vclib/*/*.py[co]
%{py_sitedir}/vclib/*/*/*.py[co]
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*
%attr(755,root,root) /home/services/httpd/cgi-bin/*
