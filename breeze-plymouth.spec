%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 70 ] && echo -n un; echo -n stable)

Summary:	The Breeze theme for the Plymouth boot splash system
Name:		breeze-plymouth
Version:	5.20.1
Release:	1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}.tar.xz
# (tpg) https://bugs.kde.org/show_bug.cgi?id=371276
Source1:	https://src.fedoraproject.org/rpms/plymouth-theme-breeze/raw/master/f/plymouth-theme-breeze.conf
Requires:	plymouth
Requires:	plymouth-plugin-script
BuildRequires:	cmake ninja
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(ply-boot-client)
BuildRequires:	pkgconfig(ply-splash-core)
BuildRequires:	distro-release
# For the logo system-white-logo
BuildRequires:	distro-theme-OpenMandriva
BuildRequires:	imagemagick

%description
This package contains a version of the KDE Breeze theme for
Plymouth boot splash system

%files
%{_datadir}/plymouth/themes/breeze
%{_datadir}/plymouth/themes/breeze-text
%{_libdir}/plymouth/breeze-text.so
%{_prefix}/lib/dracut/dracut.conf.d/10-plymouth-theme-breeze.conf

%prep
%autosetup
%cmake_kde5 \
	-DDISTRO_NAME="%product_distribution" \
	-DDISTRO_VERSION="%product_version" \
	-DDISTRO_LOGO=openmandriva

%build
%ninja_build -C build

%install
%ninja_install -C build

# (tpg) https://bugs.kde.org/show_bug.cgi?id=371276
install -D -m644 -p %{SOURCE1} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/10-plymouth-theme-breeze.conf
# (tpg) convert our logo
convert -scale 128x128 %{_datadir}/pixmaps/system-logo-white.png %{buildroot}%{_datadir}/plymouth/themes/breeze/images/openmandriva.logo.png
convert -scale 128x128 -background black -alpha remove -alpha off %{_datadir}/pixmaps/system-logo-white.png %{buildroot}%{_datadir}/plymouth/themes/breeze/images/16bit/openmandriva.logo.png
