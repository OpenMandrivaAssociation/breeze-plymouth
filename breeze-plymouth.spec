%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 70 ] && echo -n un; echo -n stable)

Summary:	The Breeze theme for the Plymouth boot splash system
Name:		breeze-plymouth
Version:	5.14.3
Release:	1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}.tar.xz
Requires:	plymouth
BuildRequires:	cmake ninja
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(ply-boot-client)
BuildRequires:	pkgconfig(ply-splash-core)
BuildRequires:	distro-release
# For the logo
BuildRequires:	distro-theme-OpenMandriva
BuildRequires:	imagemagick

%description
This package contains a version of the KDE Breeze theme for
Plymouth boot splash system

%files
%{_datadir}/plymouth/themes/breeze
%{_datadir}/plymouth/themes/breeze-text
%{_libdir}/plymouth/breeze-text.so

%prep
%autosetup
%cmake_kde5 \
	-DDISTRO_NAME="%product_distribution" \
	-DDISTRO_VERSION="%product_version" \
	-DDISTRO_LOGO=openmandriva.logo.png

%build
%ninja_build -C build

%install
%ninja_install -C build
convert %{_datadir}/icons/openmandriva.svg -scale 128x128 %{buildroot}%{_datadir}/plymouth/themes/breeze/images/openmandriva.logo.png
