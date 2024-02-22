%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
%define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Summary:	The Breeze theme for the Plymouth boot splash system
Name:		plasma6-breeze-plymouth
Version:	6.0.0
Release:	%{?git:0.%{git}.}1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/breeze-plymouth/-/archive/%{gitbranch}/breeze-plymouth-%{gitbranchd}.tar.bz2#/breeze-plymouth-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/breeze-plymouth-%{version}.tar.xz
%endif
# (tpg) https://bugs.kde.org/show_bug.cgi?id=371276
Source1:	https://src.fedoraproject.org/rpms/plymouth-theme-breeze/raw/%{gitbranchd}/f/plymouth-theme-breeze.conf
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
%autosetup -n breeze-plymouth-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DDISTRO_NAME="%product_distribution" \
	-DDISTRO_VERSION="%product_version" \
	-DDISTRO_LOGO=openmandriva \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# (tpg) https://bugs.kde.org/show_bug.cgi?id=371276
install -D -m644 -p %{SOURCE1} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/10-plymouth-theme-breeze.conf
# (tpg) convert our logo
convert -scale 128x128 %{_datadir}/pixmaps/system-logo-white.png %{buildroot}%{_datadir}/plymouth/themes/breeze/images/openmandriva.logo.png
convert -scale 128x128 -background black -alpha remove -alpha off %{_datadir}/pixmaps/system-logo-white.png %{buildroot}%{_datadir}/plymouth/themes/breeze/images/16bit/openmandriva.logo.png
