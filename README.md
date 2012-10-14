libraplus-data-converter
========================

Convert libraplus data to Gesfincas data format

HOWTO
========

1.- Split data files into single-comunity files

Check help for options:

    $ ./splitter.sh -h

Split file:

    $ ./splitter.sh comunidades.data

2.- Convert files

Check help for options:

    $ ./converter.sh -h

Convert data:

    $ ./converter.sh [-v] [-f logfile] comunidad.data

HEX ENCODER
===========
    $ python hexenc.py test.txt latin1
    BANCO ADEUDO POR DOMICILIACIONES
    \u0042\u0041\u004e\u0043\u004f\u0020\u0041\u0044\u0045\u0055\u0044\u004f\u0020\u0050\u004f\u0052\u0020\u0044\u004f\u004d\u0049\u0043\u0049\u004c\u0049\u0041\u0043\u0049\u004f\u004e\u0045\u0053\u000d\u000a
