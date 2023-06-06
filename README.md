INSTALLATION PROCEDURE:
----------------------

1.  First, decide whether you want ncurses to replace your existing library (in
    which case you'll need super-user privileges) or be installed in parallel
    with it.

    The --prefix option to configure changes the root directory for installing
    ncurses.  The default is normally in subdirectories of /usr/local, except
    for systems where ncurses is normally installed as a system library (see
    "IF YOU ARE A SYSTEM INTEGRATOR").  Use --prefix=/usr to replace your
    default curses distribution.

    The package gets installed beneath the --prefix directory as follows:

    In $(prefix)/bin:          tic, infocmp, captoinfo, tset,
				reset, clear, tput, toe, tabs
    In $(prefix)/lib:          libncurses*.* libcurses.a
    In $(prefix)/share/terminfo: compiled terminal descriptions
    In $(prefix)/include:      C header files
    Under $(prefix)/man:       the manual pages

    Note that the configure script attempts to locate previous installation of
    ncurses, and will set the default prefix according to where it finds the
    ncurses headers.

    Do not use commands such as

	make install prefix=XXX

    to change the prefix after configuration, since the prefix value is used
    for some absolute pathnames such as TERMINFO.  Instead do this

	make install DESTDIR=XXX

    See also the discussion of --with-install-prefix.

2.  Type `./configure' in the top-level directory of the distribution to
    configure ncurses for your operating system and create the Makefiles.
    Besides --prefix, various configuration options are available to customize
    the installation; use `./configure --help' to list the available options.

    If your operating system is not supported, read the PORTABILITY section in
    the file ncurses/README for information on how to create a configuration
    file for your system.

    The `configure' script generates makefile rules for one or more object
    models and their associated libraries:

	libncurses.a (normal)

	libcurses.a (normal, a link to libncurses.a)
		This gets left out if you configure with --disable-overwrite.

	libncurses.so (shared)

	libncurses_g.a (debug)

	libncurses_p.a (profile)

	libncurses.la (libtool)

    If you configure using the --enable-widec option, a "w" is appended to the
    library names (e.g., libncursesw.a), and the resulting libraries support
    wide-characters, e.g., via a UTF-8 locale.  The corresponding header files
    are compatible with the non-wide-character configuration; wide-character
    features are provided by ifdef's in the header files.  The wide-character
    library interfaces are not binary-compatible with the non-wide-character
    version.  Building and running the wide-character code relies on a fairly
    recent implementation of libiconv.  We have built this configuration on
    various systems using libiconv, sometimes requiring libutf8.

    If you configure using the --with-pthread option, a "t" is appended to
    the library names (e.g., libncursest.a, libncursestw.a).

    If you do not specify any models, the normal and debug libraries will be
    configured.  Typing `configure' with no arguments is equivalent to:

	./configure --with-normal --with-debug --enable-overwrite

    Typing

	./configure --with-shared

    makes the shared libraries the default, resulting in

	./configure --with-shared --with-normal --with-debug --enable-overwrite

    If you want only shared libraries, type

	./configure --with-shared --without-normal --without-debug

    Rules for generating shared libraries are highly dependent upon the choice
    of host system and compiler.  We've been testing shared libraries on
    several systems, but more work needs to be done to make shared libraries
    work on other systems.

    If you have libtool installed, you can type

	./configure --with-libtool

    to generate the appropriate static and/or shared libraries for your
    platform using libtool.

    You can make curses and terminfo fall back to an existing file of termcap
    definitions by configuring with --enable-termcap.  If you do this, the
    library will search /etc/termcap before the terminfo database, and will
    also interpret the contents of the TERM environment variable.  See the
    section BSD CONVERSION NOTES below.

3.  Type `make'.  Ignore any warnings, no error messages should be produced.
    This should compile the ncurses library, the terminfo compiler tic(1),
    captoinfo(1), infocmp(1), toe(1), clear(1) tset(1), reset(1), and tput(1)
    programs (see the manual pages for explanation of what they do), some test
    programs, and the panels, menus, and forms libraries.

4.  Run ncurses and several other test programs in the test directory to
    verify that ncurses functions correctly before doing an install that
    may overwrite system files.  Read the file test/README for details on
    the test programs.

    NOTE: You must have installed the terminfo database, or set the
    environment variable $TERMINFO to point to a SVr4-compatible terminfo
    database before running the test programs.  Not all vendors' terminfo
    databases are SVr4-compatible, but most seem to be.

    It is possible to configure ncurses to use other terminfo database formats.
    A few are provided as examples in the include-directory (see --with-caps).

    If you run the test programs WITHOUT installing terminfo, ncurses may
    read the termcap file and cache that in $HOME/.terminfo, which will
    thereafter be used instead of the terminfo database.  See the comments
    on "--enable-getcap-cache", to see why this is a Bad Thing.

    The ncurses program is designed specifically to test the ncurses library.
    You can use it to verify that the screen highlights work correctly, that
    cursor addressing and window scrolling works OK, etc.

5.  Once you've tested, you can type `make install' to install libraries,
    the programs, the terminfo database and the manual pages.  Alternately, you
    can type `make install' in each directory you want to install.  In the
    top-level directory, you can do a partial install using these commands:

	'make install.progs'    installs tic, infocmp, etc...
	'make install.includes' installs the headers.
	'make install.libs'     installs the libraries (and the headers).
	'make install.data'     installs the terminfo data. (Note: `tic' must
				be installed before the terminfo data can be
				compiled).
	'make install.man'      installs the manual pages.
