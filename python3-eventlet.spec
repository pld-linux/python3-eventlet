#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# unit tests (random timeouts on builders)

Summary:	Highly concurrent networking library for Python 2
Summary(pl.UTF-8):	Biblioteka sieciowa o dużym stopniu zrównoleglenia dla Pythona 2
Name:		python3-eventlet
Version:	0.39.1
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/eventlet/
Source0:	https://files.pythonhosted.org/packages/source/e/eventlet/eventlet-%{version}.tar.gz
# Source0-md5:	00206ce34e033f9a8167270c29c4b24d
URL:		https://pypi.org/project/eventlet/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-build
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-dns >= 1.15.0
BuildRequires:	python3-greenlet >= 0.3
BuildRequires:	python3-nose >= 1.3.1
BuildRequires:	python3-six >= 1.10.0
%endif
%if %{with doc}
BuildRequires:	python3-dns >= 1.15.0
BuildRequires:	python3-greenlet >= 0.3
BuildRequires:	sphinx-pdg >= 2
%endif
%if %{with tests}
# SO_REUSEPORT option for tests.convenience_test.test_socket_reuse
BuildRequires:	uname(release) >= 3.9
%endif
Requires:	python3-modules >= 1:2.7
BuildArch:	noarch
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

%package apidocs
Summary:	API documentation for eventlet module
Summary(pl.UTF-8):	Dokumentacja API modułu eventlet
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for eventlet module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu eventlet.

%prep
%setup -q -n eventlet-%{version}

# uses network
%{__rm} tests/greendns_test.py
# requires local mysql
%{__rm} tests/mysqldb_test.py

%build
%py3_build_pyproject

%if %{with tests}
#PYTHONPATH=$(pwd) \
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html doc/source doc/source/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.rst
%{py3_sitescriptdir}/eventlet
%{py3_sitescriptdir}/eventlet-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/source/_build/html/{_images,_static,modules,*.html,*.js}
%endif
