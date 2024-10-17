%define	title		Ur-Quan Masters
%define	longtitle	The Ur-Quan Masters
%define debug_package	%{nil}

Name:		uqm-megamod
Version:	0.8.0.85
Release:	3
Summary:	The Ur-Quan Masters, Modified version
License:	GPLv2
Group:		Games/Strategy
URL:		https://megamod.serosis.net/
Source0:	https://github.com/Serosis/UQM-MegaMod/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	uqm-16.png
Source2:	uqm-32.png
Source3:	uqm-48.png
Requires:	%{name}-content
Suggests:	%{name}-voice
Suggests:	%{name}-3domusic
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libmikmod)
BuildRequires:	pkgconfig(libpng16)
BuildRequires:	pkgconfig(lua)

%description
The Ur-Quan Masters (uqm package in OpenMandriva) is a port of
the 3DO version of Star Control 2.

UQM-MegaMod is a modified fork, featuring among other things
higher resolution graphics.

%prep
%autosetup -p1 -n UQM-MegaMod-%{version}

# create configuration
cat > config.state <<EOF
CHOICE_debug_VALUE='nodebug'
CHOICE_graphics_VALUE='sdl2'
CHOICE_sound_VALUE='mixsdl'
CHOICE_mikmod_VALUE='external'
CHOICE_lua_VALUE='external'
CHOICE_ovcodec_VALUE='standard'
CHOICE_netplay_VALUE='full'
CHOICE_joystick_VALUE='enabled'
CHOICE_ioformat_VALUE='stdio_zip'
CHOICE_accel_VALUE='asm'
CHOICE_threadlib_VALUE='sdl'
INPUT_install_prefix_VALUE='%{_gamesbindir}'
INPUT_install_bindir_VALUE='%{_gamesbindir}'
INPUT_install_libdir_VALUE='%{_libdir}'
INPUT_install_sharedir_VALUE='%{_gamesdatadir}'
EOF

echo |./build.sh uqm config

%build
sed -i -e 's,gcc,%{__cc},g;s,g++,%{__cxx},g' build.vars
./build.sh %{?_smp_mflags} uqm

%install
rm -rf %{buildroot}
perl -pi -e 's|%{_prefix}|%{buildroot}%{_prefix}|' build.vars
./build.sh uqm install

# icons
install -D -m 644 %{S:3} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m 644 %{S:2} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m 644 %{S:1} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png

# menu
install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame
EOF

%files
%defattr(-,root,root)
%doc AUTHORS BUGS WhatsNew ChangeLog README Contributing
%doc doc/users/manual.txt
%{_gamesbindir}/UrQuanMasters
%{_gamesdatadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
