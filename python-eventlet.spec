# TODO: fix green.ssl on Python 3.7
#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# unit tests [failures with python3.7: green.ssl is broken there, as of 0.23.0]
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

Summary:	Highly concurrent networking library for Python 2
Summary(pl.UTF-8):	Biblioteka sieciowa o dużym stopniu zrównoleglenia dla Pythona 2
Name:		python-eventlet
Version:	0.23.0
Release:	3
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/eventlet/
Source0:	https://files.pythonhosted.org/packages/source/e/eventlet/eventlet-%{version}.tar.gz
# Source0-md5:	9b459a4d3b1365febd0d22cf71b9e7ce
URL:		https://pypi.org/project/eventlet/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools >= 5.4.1
%if %{with tests}
BuildRequires:	python-enum34
BuildRequires:	python-greenlet >= 0.3
BuildRequires:	python-nose >= 1.3.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-setuptools >= 5.4.1
%if %{with tests}
%if "%{py3_ver}" < "3.4"
BuildRequires:	python3-enum34
%endif
BuildRequires:	python3-greenlet >= 0.3
BuildRequires:	python3-nose >= 1.3.1
%endif
%endif
%{?with_doc:BuildRequires:	sphinx-pdg}
%if %{with tests}
# SO_REUSEPORT option for tests.convenience_test.test_socket_reuse
BuildRequires:	uname(release) >= 3.9
%endif
Requires:	python-modules >= 1:2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eventlet is a concurrent networking library for Python that allows you
to change how you run your code, not how you write it.

It uses epoll or libevent for highly scalable non-blocking I/O.
Coroutines ensure that the developer uses a blocking style of
programming that is similar to threading, but provide the benefits of
non-blocking I/O. The event dispatch is implicit, which means you can
easily use Eventlet from the Python interpreter, or as a small part of
a larger application.

%description -l pl.UTF-8
Eventlet to równoległa biblioteka sieciowa dla Ptyhona, pozwalająca na
zmianę sposobu uruchamiania kodu bez sposobu pisania go.

Biblioteka wykorzystuje epoll lub libevent do wysoko skalowalnych,
nieblokujących operacji we/wy. Korutyny zapewniają, że programista
korzysta z blokującego stylu programowania, podobnego do wątkowego,
ale mającego zalety nieblokującego we/wy. Przekazywania zdarzeń jest
domyślne, co oznacza, że można łatwo używać modułu Eventlet z poziomu
interpretera Pythona lub jako małej części dużej aplikacji.

%package -n python3-eventlet
Summary:	Highly concurrent networking library for Python 3
Summary(pl.UTF-8):	Biblioteka sieciowa o dużym stopniu zrównoleglenia dla Pythona 3
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-eventlet
Eventlet is a concurrent networking library for Python that allows you
to change how you run your code, not how you write it.

It uses epoll or libevent for highly scalable non-blocking I/O.
Coroutines ensure that the developer uses a blocking style of
programming that is similar to threading, but provide the benefits of
non-blocking I/O. The event dispatch is implicit, which means you can
easily use Eventlet from the Python interpreter, or as a small part of
a larger application.

%description -n python3-eventlet -l pl.UTF-8
Eventlet to równoległa biblioteka sieciowa dla Ptyhona, pozwalająca na
zmianę sposobu uruchamiania kodu bez sposobu pisania go.

Biblioteka wykorzystuje epoll lub libevent do wysoko skalowalnych,
nieblokujących operacji we/wy. Korutyny zapewniają, że programista
korzysta z blokującego stylu programowania, podobnego do wątkowego,
ale mającego zalety nieblokującego we/wy. Przekazywania zdarzeń jest
domyślne, co oznacza, że można łatwo używać modułu Eventlet z poziomu
interpretera Pythona lub jako małej części dużej aplikacji.

%package apidocs
Summary:	API documentation for eventlet module
Summary(pl.UTF-8):	Dokumentacja API modułu eventlet
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for eventlet module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu eventlet.

%prep
%setup -q -n eventlet-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
nosetests-%{py_ver} tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
nosetests-%{py3_ver} tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc -j1 html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install

%if "%{py3_ver}" >= "3.4"
# don't require enum34 on python >= 3.4 (different forms depending on setuptools version)
%{__sed} -i -e '/^\[:python_version *< *"3\.4"]/,$ d' \
	-e '/^enum34;python_version<"3\.4"/d' $RPM_BUILD_ROOT%{py3_sitescriptdir}/eventlet-%{version}-py*.egg-info/requires.txt
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.rst
%{py_sitescriptdir}/eventlet
%{py_sitescriptdir}/eventlet-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-eventlet
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.rst
%{py3_sitescriptdir}/eventlet
%{py3_sitescriptdir}/eventlet-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,modules,*.html,*.js}
%endif
