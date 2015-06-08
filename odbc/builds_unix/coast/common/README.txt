Go to the proper machine that has the right OS (linux, HP-UX, etc)

to build it:
(1) . ./setup.sh
(2) make clean
(3) make
    <NOTE: make will also create soft links for *.char files and MXODSN;
     they are needed for running the program>

to run it:
(A) On the target side:
   The coast tests need setup on the target machine,  see README.txt
   <test_root>/src/odbctest_spjs for more details.  This only needs to
   be done once per machine.

(B) On the client side:
(1) Make sure that MXODSN has an entry for the data source that you are
    going to provide to the -d option
(2) Modify env.sh to have your dsn/usrid/password/charset
(3) . ./setup.sh
(4) . ./env.sh
(5) ./run.sh
(6) Once you are done, please move the log file(s) to the location where
    the file(s) can be saved.

A few notes if you are running the UNICODE version:
(1) Currently, you can only run the UNICODE version with either ASCII or
    GBK.  The other charset files *.char such as SJIS have not been cleaned
    up yet.  GBK has a bigger plane than SJIS, that's why we have chosen
    GBK to clean up first.  Also, even though ASCII works, we are not running
    ASCII for regression.  The ANSI version already covers ASCII.
(2) The UNIX UNICODE uses ICU library.  The application calls the ICU library
    to convert a string in xxx.char from the local (say GBK) encoding into
    the UNICODE UTF8 encoding before giving the string to the ODBC routines.
    In your MXODSN, you will have to set ClientCharSet to UTF8 so that
    the driver knows that you are feeding it UTF8 characters.

    ClientCharSet = UTF8
(3) On the client shell, depending on what your OS supports, you can set 

    export LANG=zh_CN.GBK
    export LC_ALL=zh_CN.GBK

    or

    export LANG=zh_CN.gb18030
    export LC_ALL=zh_CN.gb18030

    This has less to do with the test, but more to do with being able to
    display the actual characters in a humanely readable form (if you can 
    read the language) on your section.
(4) When using the run script run.sh, make sure that you export
    the environmental variable ODBCTEST_CHARSET to GBK before running it. 

    export ODBCTEST_CHARSET=GBK

    This is important not only that it tells coast to pick up the correct
    xxx.char file, COAST.cpp also calls the following to tell the ICU library
    that the translation is to be done from GBK to UTF8, so that all of
    the icu_ConTo()/icu_ConFrom() (they eventally calls the ICU library
    ucnc_fromUChars()/ucnc_toUChars()) functions know what kind of 
    translation to use.

    /* inputLocale here will be "GBK" */
    icu_conv->locale = ucnv_open(inputLocale, &icu_conv->err);

    ucnv_fromUChars(icu_conv->locale,....)
    ucnv_toUChars(icu_conv->locale,...)
(5) On Seaquest, we no longer support inserting a GBK or SJIS characters into
    a ISO88591 column.  They can only be inserted into a UCS2 column (Seaquest
    M5 feature) or UTF8 column (Seaquest M6 feature).  If you declare a 
    column with no attribute, they will be treated as ISO88591.  If you 
    intend to insert a GBK/SJIS column, you will have to declare the column
    as 
    colname char(10) character set ucs2
    colname varchar(10) character set ucs2
    The Neoview version of xxx.char files have a lot of ISO88591 columns for
    GBK/SJIS,  they will no longer work in Seaquest anymore.

