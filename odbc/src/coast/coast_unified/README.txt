- The unix version of Coast_UNICODE_unix is built and run from the unix build 
  structure.  See README.txt in the build strcuture for more details.

- To build the windows version
  (1) Go to Coast_UNICODE_win\builds_win, click on COAST.vs2005.vcproj, 
      or any other vcproj file that is suitable for your machine.
  (2) on top of the window bar select:
      * 64-bit machine: Solution Configurations: UNICODE
                        Solution Platforms: x64
      * 32-bit machine: Solution Configurations: UNICODE
                        Solution Platforms: Win32
  (3) Build -> Rebuild Solution. 
      Coast.exe should be generated in
      * 64-bit machine: Coast_UNICODE_win\builds_win\UNICODE\x64
      * 32-bit machine: Coast_UNICODE_win\builds_win\UNICODE\Win32

- To run the windows version
(A) On the target side:
   The coast tests need setup on the target machine,  see README.txt
   <test_root>/src/odbctest_spjs for more details.  This only needs to
   be done once per machine.

(B) On the client side:
  (1) Make sure that the data source that you want to use is registered:
      Control Panel -> Administrative Tools -> Data Sources (ODBC)
      If it is not there, you can either add it as "User DSN" for only
      this particular user, or "System DSN" for everyone to use.  It 
      does not matter since everyone log on to the PC using the same
      administrator account.
  (2) Open a DOS window, cd to where the program is (see to build it session
      about where the exe file is on each different type of machines).
  (3) If you are running from a 32-bit machine:
      * Modify ..\..\env_win32.bat to have your dsn/usrid/password/charset.
      * ..\..\env_win32.bat
      * ..\..\run.bat
      If you are running from a 64-bit machine:
      * Modify ..\..\env_win64.bat to have your dsn/usrid/password/charset.
      * ..\..\env_win64.bat
      * ..\..\run.bat
  (4) Once you are done, please move the log files to the linux location
      where all log files are saved.

A few notes if you are running the UNICODE version:
(1) Currently, you can only run the UNICODE version with either ASCII or
    GBK.  The other charset files *.char such as SJIS have not been cleaned
    up yet.  GBK has a bigger plane than SJIS, that's why we have chosen
    GBK to clean up first.  Also, even though ASCII works, we are not running
    ASCII for regression.  The ANSI version already covers ASCII.
(2) Unlike the UNIX UNICODE test, which uses the ICU library, the Windows
    UNICODE test uses the native UNICODE support such as _T(), etc on 
    Windows.
(3) Before running the test, from Control Panel->Regional and Language, change
    the langauge to Chinese (Simplified, PRC).  Changing this option does not
    require rebooting the system.  You don't have to change the locale, which
    is only needed for non-Unicode program and requires robooting the system.
(4) When using the run script run.bat make sure that you export
    the environmental variable ODBCTEST_CHARSET to GBK before running it.

    export ODBCTEST_CHARSET=GBK

    This ensures that the tests pick up the right char file.
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

