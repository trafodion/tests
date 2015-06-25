-- @@@ START COPYRIGHT @@@
--
-- (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
--
--  Licensed under the Apache License, Version 2.0 (the "License");
--  you may not use this file except in compliance with the License.
--  You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
--  Unless required by applicable law or agreed to in writing, software
--  distributed under the License is distributed on an "AS IS" BASIS,
--  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--  See the License for the specific language governing permissions and
--  limitations under the License.
--
-- @@@ END COPYRIGHT @@@



Go to the proper machine that has the right OS (linux,etc)

to build it:
(1) . ./setup.sh
(2) make clean
(3) make
    <NOTE: make will also create soft links for *.char files and TRAFDSN;
     they are needed for running the program>

to run it:
(A) On the target side:
   The coast tests need setup on the target machine,  see README.txt
   <test_root>/src/odbctest_spjs for more details.  This only needs to
   be done once per machine.

(B) On the client side:
(1) Make sure that TRAFDSN has an entry for the data source that you are
    going to provide to the -d option
(2) Modify env.sh to have your dsn/usrid/password/charset
(3) . ./setup.sh
(4) . ./env.sh
(5) ./run.sh
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

