%global revision 20180923
Name:          ncurses
Version:       6.1
Release:       12
Summary:       Terminal control library
License:       MIT
URL:           https://invisible-island.net/ncurses/ncurses.html
Source0:       https://invisible-mirror.net/archives/ncurses/current/ncurses-%{version}-%{revision}.tgz

Patch8:        ncurses-config.patch
Patch9:        ncurses-libs.patch
Patch11:       ncurses-urxvt.patch
Patch12:       ncurses-kbs.patch

Patch6000:     CVE-2019-17594.patch
Patch6001:     CVE-2019-17595.patch

BuildRequires: gcc gcc-c++ gpm-devel pkgconfig

Obsoletes:     ncurses < 5.6-13
Obsoletes:     libtermcap < 2.0.8-48
Obsoletes:     termcap < 1:5.5-2
Provides:      %{name}-base = %{version}-%{release}
Obsoletes:     %{name}-base < %{version}-%{release}
Provides:      %{name}-libs = %{version}-%{release}
Obsoletes:     %{name}-libs < %{version}-%{release}
Provides:      %{name}-compat-libs = %{version}-%{release}
Provides:      %{name}-compat-libs%{?_isa} = %{version}-%{release}
Obsoletes:     %{name}-compat-libs < %{version}-%{release}
Provides:      %{name}-c++-libs = %{version}-%{release}
Obsoletes:     %{name}-c++-libs < %{version}-%{release}
Provides:      %{name}-term = %{version}-%{release}
Obsoletes:     %{name}-term < %{version}-%{release}

%description
The ncurses (new curses) library is a free software emulation of 
curses in System V Release 4.0 (SVr4), and more. It uses terminfo 
format, supports pads and color and multiple highlights and forms 
characters and function-key mapping, and has all the other SVr4-curses 
enhancements over BSD curses. SVr4 curses became the basis of X/Open Curses.

%package devel
Summary:       Development files for the ncurses library
Requires:      %{name} = %{version}-%{release}
Requires:      pkgconfig
Obsoletes:     libtermcap-devel < 2.0.8-48
Provides:      libtermcap-devel = 2.0.8-48
Provides:      %{name}-static = %{version}-%{release}
Obsoletes:     %{name}-static = %{version}-%{release}

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.a, including static libraries 
of the ncurses library.

%package help
Summary: Ncurse help document
Requires: %{name} = %{version}-%{release}

%description help
This package contains development documentation, manuals 
for interface function, and related documents.

%prep
%autosetup -n %{name}-%{version}-%{revision} -p1

for f in ANNOUNCE; do
    iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
        touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
common_options="--enable-colorfgbg --enable-hard-tabs --enable-overwrite \
    --enable-pc-files --enable-xmc-glitch --disable-wattr-macros \
    --with-cxx-shared --with-ospeed=unsigned \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --with-shared \
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \
    --with-termlib=tinfo --with-ticlib=tic --with-xterm-kbs=DEL \
    --without-ada"
abi5_options="--with-chtype=long"

for abi in 5 6; do
    for char in narrowc widec; do
        mkdir $char$abi
        pushd $char$abi
        ln -s ../configure .

        [ $abi = 6 -a $char = widec ] && progs=yes || progs=no

        %configure $(
            echo $common_options --with-abi-version=$abi
            [ $abi = 5 ] && echo $abi5_options
            [ $char = widec ] && echo --enable-widec
            [ $progs = yes ] || echo --without-progs
        )

        make %{?_smp_mflags} libs
        [ $progs = yes ] && make %{?_smp_mflags} -C progs

        popd
    done
done

%install
make -C narrowc5 DESTDIR=$RPM_BUILD_ROOT install.libs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.5*
make -C widec5 DESTDIR=$RPM_BUILD_ROOT install.libs
make -C narrowc6 DESTDIR=$RPM_BUILD_ROOT install.libs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.6*
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data,includes,man}

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

baseterms=

# prepare -base and -term file lists
for termname in \
    ansi dumb linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    konsole konsole-256color mach\* mlterm mrxvt nsterm putty{,-256color} pcansi \
    rxvt{,-\*} screen{,-\*color,.[^mlp]\*,.linux,.mlterm\*,.putty{,-256color},.mrxvt} \
    st{,-\*color} sun teraterm teraterm2.3 tmux{,-\*} vte vte-256color vwmterm \
    wsvt25\* xfce xterm xterm-\*
do
    for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
        for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
            baseterms="$baseterms $(basename $t)"
        done
    done
done 2> /dev/null
for t in $baseterms; do
    echo "%dir %{_datadir}/terminfo/${t::1}"
    echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
    sed "s|^$RPM_BUILD_ROOT||" | while read t
do
    echo "%dir $(dirname $t)"
    echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

# don't require -ltinfo when linking with --no-add-needed
for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

rm -f $RPM_BUILD_ROOT%{_bindir}/ncurses*5-config
rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*_g.pc

bzip2 NEWS

%ldconfig_scriptlets 

%files
%doc ANNOUNCE AUTHORS
%doc c++/README*
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/[cirt]*
%{_libdir}/lib*.so.5*
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%{_datadir}/terminfo/*
%{_libdir}/lib*.so.6*

%files devel
%{_bindir}/ncurses*-config
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ncurses/*.h
%{_includedir}/ncursesw/*.h
%{_includedir}/*.h

%files help
%doc NEWS.bz2 README TO-DO
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%doc misc/ncurses.supp
%{_mandir}/man1/ncurses*-config*
%{_mandir}/man3/*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*


%changelog
* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.1-12
- Type:cves
- ID:CVE-2019-17594  CVE-2019-17595
- SUG:NA
- DESC:fix CVE-2019-17594 and CVE-2019-17595

* Wed Oct 30 2019 shenyangyang <shenyangyang4@huawei.com> - 6.1-11
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify the obsoletes version

* Thu Oct 17 2019 caomeng <caomeng5@huawei.com> - 6.1-10
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add ncurses-compat-libs%{?isa}
* Wed Sep 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.1-9
- Package init
