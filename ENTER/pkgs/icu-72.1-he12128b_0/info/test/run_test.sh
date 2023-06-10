#!/bin/bash

set -e

genrb de.txt
echo "de.res" > list.txt
pkgdata -p mybundle list.txt


set -ex



test -f $PREFIX/lib/libicudata.a
test -f $PREFIX/lib/libicudata.72.1.dylib
test -f $PREFIX/lib/libicui18n.a
test -f $PREFIX/lib/libicui18n.72.1.dylib
test -f $PREFIX/lib/libicuio.a
test -f $PREFIX/lib/libicuio.72.1.dylib
test -f $PREFIX/lib/libicutest.a
test -f $PREFIX/lib/libicutest.72.1.dylib
test -f $PREFIX/lib/libicutu.a
test -f $PREFIX/lib/libicutu.72.1.dylib
test -f $PREFIX/lib/libicuuc.a
test -f $PREFIX/lib/libicuuc.72.1.dylib
genbrk --help
gencfu --help
gencnval --help
gendict --help
icuinfo --help
icu-config --help
makeconv gb-18030-2000.ucm
exit 0
