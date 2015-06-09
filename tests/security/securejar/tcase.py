# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");"""
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

from ...lib import hpdci
import defs
import basic_defs
import time

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
 

def testa01(desc="""CREATE LIBRARY"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library  """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """call testUserFunction();"""
    output = mydci.cmdexec(stmt)    
    mydci.expect_selected_msg(output,1)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library SECURITY_SECUREJAR."""+ defs.sec_libname1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_libname1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' HOST NAME 'seasprite';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' LOCAL FILE '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop library """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""'  HOST NAME 'seasprite' LOCAL FILE '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #No duplicate library name
    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1390')

    #library filename not exist ???

    stmt = """create library """+ defs.sec_lib2 +""" file '/jar/abc.jar';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1382')
    
    #two library can't reference same filename

    #stmt = """create library """+ defs.sec_lib2 +""" file '"""+ defs.spjpath +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '8102')
    #mydci.expect_error_msg(output, '1102')
    
    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #syntax check

    stmt = """create library 
lib01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234 
file '"""+ defs.spjpathrs +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library 
lib01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """create library 
lib012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345 
file '"""+ defs.spjpathrs +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '3118')

    stmt = """create library 2lib file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library _lib file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib-1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib@1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib%1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib&1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib*1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib+1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib=1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib@1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib~1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib!1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib,1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib:1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib;"1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15005')

    stmt = """create library lib[1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib]1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib{1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib}1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib?1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib/1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib<1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib>1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """create library lib.1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib 1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """add library lib1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """creat library lib1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create libary lib1 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """create library lib1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib1 filename '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library lib1 file;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file HOST NAME 'localhost';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """create library """+ defs.sec_lib1 +""" file LOCAL FILE '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' HOST 'localhost';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' HOSTNAME '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' LOCALNAME 'localhost';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' HOST NAME LOCAL FILE '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' HOST NAME 'localhost' LOCAL FILE;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""' HOST NAME 'localhost' HOST FILE '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""'  LOCAL FILE '"""+ defs.spjpath +"""' HOST NAME 'localhost' HOST FILE '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    #user with granted create or create_library privilege 

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #expect any *1 row(s) selected*
    stmt = """call testUserFunction();"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #user with no granted create or create_library privilege 


    mydci = basic_defs.switch_session_qi_user4()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    _testmgr.testcase_end(desc)
    
    
def testa02(desc="""DROP LIBRARY"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #drop library with no procedure
    #default is RESTRICT

    stmt = """drop library """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library SECURITY_SECUREJAR."""+ defs.sec_libname1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_libname1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop library """+ defs.sec_lib1 +""" RESTRICT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" CASCADE;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" RESTRICT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    #drop library with procedure
    stmt = """drop library """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1366')
 
    stmt = """drop library """+ defs.sec_lib1 +""" RESTRICT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1366')

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)

    stmt = """drop library """+ defs.sec_lib1 +""" CASCADE;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #testUserFunction() should not exist
    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1004')
    mydci.expect_error_msg(output, '1389')

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #snytax check
    stmt = """delete library """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drep library """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop libary """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop libraries """+ defs.sec_lib1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """drop library 123_cat.SECURITY_SECUREJAR."""+ defs.sec_libname1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library 123_schema."""+ defs.sec_libname1 +""";"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """drop library 123_lib;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library """+ defs.sec_lib1 +""" RISTRCT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library """+ defs.sec_lib1 +""" CSCADE;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library """+ defs.sec_lib1 +""" RISTRICT CASCADE;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library """+ defs.sec_lib1 +""" CASCADE RISTRICT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library library_not_exist;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1361')
    #mydci.expect_error_msg(output, '1389')

    #user with granted DROP_LIBRARY or DROP privelege

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #user with no granted DROP_LIBRARY or DROP privilege 

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
    
    
    
def testa08(desc="""CREATE PROCEDURE with LIBRARY"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR."""+ defs.sec_libname1 +"""
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY """+ defs.sec_libname1 +"""
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY lib_not_exist
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1361')
    mydci.expect_error_msg(output, '1389')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY cat_not_exist.SECURITY_SECUREJAR."""+ defs.sec_libname1 +"""
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1002')
    mydci.expect_error_msg(output, '1389')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY sch_not_exist."""+ defs.sec_libname1 +"""
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1003')
    mydci.expect_error_msg(output, '1389')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    EXTERNAL PATH '"""+ defs.spjpath +"""'
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    mydci.expect_error_msg(output, '1389')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    EXTERNAL LIBRARY SECURITY_SECUREJAR.defs.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    FOR LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1,
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
    
def testa09(desc="""GRANT LIBRARY privileges:usage update all"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #test GRANT USAGE

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #test GRANT UPDATE

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant update on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpathrs +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user4()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')

    #test GRANT ALL

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke update on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpathrs +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #test GRANT USAGE WITH GRANT OPTION

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT OPTION;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #test GRANT UPDATE WITH GRANT OPTION

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant update on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT OPTION;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant update on library """+ defs.sec_lib1 +""" to qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpathrs +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke update on library """+ defs.sec_lib1 +""" from qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke update on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #test GRANT ALL WITH GRANT OPTION

    #stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT OPTION;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all privileges on library """+ defs.sec_lib1 +""" from qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all privileges on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #Test library name

    stmt = """grant all privileges on library SECURITY_SECUREJAR."""+ defs.sec_libname1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke all  on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all privileges on library """+ defs.sec_libname1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all privileges on library lib_not_exist to qauser11;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1361')
    mydci.expect_error_msg(output, '1389')

    #Test grantee lists

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpathrs +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    mydci = basic_defs.switch_session_qi_user2()

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser12;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from PUBLIC;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to DB__SERVICES;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from DB__SERVICES;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    stmt = """grnt all on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant alll on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant usages on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant usages on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant updat on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant create on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1328')

    stmt = """grant usage privileges on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant update privileges on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privilege on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privilges on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
    
    stmt = """grant all for library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all of library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all on """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')

    stmt = """grant all on lib """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all on libary """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all on libraries """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all on library """+ defs.sec_lib1 +""" too qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all on library """+ defs.sec_lib1 +""" qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11, ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 WTH GRANT OPTION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 WITH GRNT OPTION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 WTH GRANT OPTON;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 WITH OPTION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 GRANT OPTION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 GRANT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11 OPTION;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop library """+ defs.sec_lib1 +""" cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
    
def testa10(desc="""REVOKE LIBRARY privileges:usage update all"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    #test REVOKE USAGE

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
 
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #test REVOKE UPDATE

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant update on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpathrs +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke update on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')

    #test REVOKE ALL

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """grant all privileges on library """+ defs.sec_lib1 +""" to qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    time.sleep(10)
    
    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop procedure testUserFunction;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke all privileges on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    time.sleep(10)

    mydci = basic_defs.switch_session_qi_user3()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
	    external name 'TestDML.testUserFunction' 
	    LIBRARY SECURITY_SECUREJAR.sec_lib1
	    language java 
	    parameter style java
	    DYNAMIC RESULT SETS 1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481')

    #stmt = """alter library """+ defs.sec_lib1 +""" file '"""+ defs.spjpathrs +"""';"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')

    #test revoke cascade

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11 restrict;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11 cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """grant update on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke update on library """+ defs.sec_lib1 +""" from qauser11 restrict;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """grant update on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke update on library """+ defs.sec_lib1 +""" from qauser11 cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """grant all on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 restrict;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """grant all on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1014')
    
    #time.sleep(10)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11 restrict;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1014')
    
    #time.sleep(10)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11 cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #procedure should be dropped
    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '15001')

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant all on library """+ defs.sec_lib1 +""" to qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1014')

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 restrict;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1014')

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 cascade;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #procedure should be dropped
    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '15001')

    mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #test revoke privileges from user does not have

    stmt = """revoke usage on library """+ defs.sec_libname1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_warning_msg(output, '1015')
    mydci.expect_complete_msg(output)

    stmt = """revoke update on library """+ defs.sec_libname1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_warning_msg(output, '1015')
    mydci.expect_complete_msg(output)

    stmt = """revoke all on library """+ defs.sec_libname1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_warning_msg(output, '1015')
    mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #test revoke from non-exist user

#expect any *ERROR*
    stmt = """revoke all on library """+ defs.sec_libname1 +""" from user_not_exist;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1008')
    
    #time.sleep(10)

    #test revoke GRANT OPTION FOR, usage

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT OPTION;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #need to have "cascade" option 
    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1014')
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke GRANT OPTION FOR usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #user2 has not privilege to grant usage
    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser13;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1012')

    #user2 still has usage privilege
    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #test revoke GRANT OPTION FOR, all

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant all on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT OPTION;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """grant all on library """+ defs.sec_lib1 +""" to qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user5()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #need to have "cascade" option 
    #stmt = """revoke GRANT OPTION FOR usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1014')
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser12;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user2()
    #stmt = """set schema SECURITY_SECUREJAR;"""

    #stmt = """revoke GRANT OPTION FOR all on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #mydci = basic_defs.switch_session_qi_user3()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #user2 has not privilege to grant usage
    #stmt = """grant all on library """+ defs.sec_lib1 +""" to qauser13;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1012')

    #user2 still has usage privilege
    #stmt = """Create procedure testUserFunction()
	    #external name 'TestDML.testUserFunction' 
	    #LIBRARY SECURITY_SECUREJAR.sec_lib1
	    #language java 
	    #parameter style java
	    #DYNAMIC RESULT SETS 1;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """drop procedure testUserFunction;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #mydci = basic_defs.switch_session_qi_user2()
    
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)

    #stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    
    #time.sleep(10)

    #test revoke GRANT BY

    #process user_root
    #stmt = """set schema SECURITY_SECUREJAR;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser11 WITH GRANT OPTION;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser12 GRANTED BY qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser12 GRANTED BY qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """grant usage on library """+ defs.sec_lib1 +""" to qauser12 BY qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)

   # stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser12;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output, '1015')
    
    #time.sleep(10)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser12 BY qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    #time.sleep(10)

    #stmt = """revoke usage on library """+ defs.sec_lib1 +""" from qauser11;"""
    #output = _dci.cmdexec(stmt)
    #_dci.expect_complete_msg(output)
    
    #time.sleep(10)

    #test syntax error
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)

    stmt = """revok all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """remove all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """delete all on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke usag on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke  usage privileges on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke updte on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke update privileges on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke alll on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all privilege on library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all of library """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on libary """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on """+ defs.sec_lib1 +""" from qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1389')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" of qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" qauser11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 GRANT BY qauser10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 GRANTED qauser10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 GRANTED FROM qauser10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 GRANTED BY;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 RESTRCT;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 CASCDE;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 CASCADE GRANT BY qauser10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """revoke all on library """+ defs.sec_lib1 +""" from qauser11 RESTRCT GRANT BY qauser10;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    _testmgr.testcase_end(desc)

def testa11(desc="""CREATE LIBRARY,max, below max,blank,invalid name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return


    mydci = basic_defs.switch_session_qi_user2()

    stmt = """set schema SECURITY_SECUREJAR;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """create library  """ """ file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """create library qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '3118')

    stmt = """create library "1289-_@" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library  "1289-_@";"""
    output = mydci.cmdexec(stmt)

    stmt = """create library  qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127 file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library  qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = mydci.cmdexec(stmt)

    stmt = """create library  "_AREqw3132 4d afd3AAA"  file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library  "_AREqw3132 4d afd3AAA";"""
    output = mydci.cmdexec(stmt)

    stmt = """create library  "Test~!#$" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library  "Test~!#$";"""
    output = mydci.cmdexec(stmt)

    stmt = """create library  AaBb file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop library  AaBb;"""
    output = mydci.cmdexec(stmt)

    stmt = """create library _W1245wereqwr file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '3127')

    stmt = """drop library _W1245wereqwr;"""
    output = mydci.cmdexec(stmt)

    stmt = """create library "^testa**$" file '"""+ defs.spjpath +"""';"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '3127')

    stmt = """drop library "^testa**$";"""
    output = mydci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
