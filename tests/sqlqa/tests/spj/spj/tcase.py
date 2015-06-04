# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
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
from ...lib import gvars
import defs

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

#***************************************************************************
#                                 Test0001
#***************************************************************************
#Purpose: 		test create library
#Comments:		None.
#Modification History:  

def test0001(desc="""Test0001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    # make sure library is dropped
    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
           external name 'TestDML.testUserFunction'
           LIBRARY qa_dfr language java
           parameter style java
           DYNAMIC RESULT SETS 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure testUserFunction;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr cascade;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # No duplicate library name

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1390')

    # library filename not exist ???

    stmt = "create library qa_dfrrs file '/jar/abc.jar';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1382')

    stmt = "drop library qa_dfr cascade;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create library
      lib01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234
      file '""" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop library
      lib01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create library
      lib012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
      file '""" + defs.dfr_path + "';"

    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = "create library 2lib file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library _lib file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib-1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib@1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib%1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib&1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib*1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib+1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib=1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib@1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib~1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib!1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib,1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib:1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib;1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib[1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib]1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib{1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib}1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib?1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib/1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib<1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib>1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib.1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib 1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "add library lib1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "creat library lib1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create libary lib1 file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib1 filename '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "create library lib1 file;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                 Test0002
#***************************************************************************
#Purpose: 		test drop library
#Comments:		None.
#Modification History:  

def test0002(desc="""Test0002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr RESTRICT;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure testUserFunction()
           external name 'TestDML.testUserFunction'
           LIBRARY qa_dfr
           language java
           parameter style java
           DYNAMIC RESULT SETS 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1366')

    stmt = "drop library qa_dfr RESTRICT;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1366')

    stmt = "drop procedure testUserFunction;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "delete library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drep library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop libary qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop libraries qa_dfr};"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library 123_cat.123_schema.qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library 123_schema.qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library 123_lib;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library qa_dfr RISTRCT;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library qa_dfr CSCADE;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library qa_dfr CASCADE RISTRICT;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = "drop library library_not_exist;"
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1389')

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0003
#***************************************************************************
#Purpose: 		test SPJ with JDBC call to create table
#Comments:		None.
#Modification History:  

def test0003(desc="""Test0003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table t1 cascade;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure createTable()
	    external name 'TestDDL.createTable' 
	    LIBRARY qa_dfr
	    language java 
           NO TRANSACTION REQUIRED
	    parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "call createTable();"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "showddl t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop table t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure createTable;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0004
#***************************************************************************
#Purpose: 		test SPJ with JDBC call to create view
#Comments:		None.
#Modification History:  

def test0004(desc="""Test0004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table t1 cascade;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure createView()
	    external name 'TestDDL.createView' 
	    LIBRARY qa_dfr
	    language java 
           NO TRANSACTION REQUIRED
	    parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int);"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "call createView();"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "showddl v1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop view v1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop table t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure createView;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0005
#***************************************************************************
#Purpose: 		test SPJ with JDBC call to create index
#Comments:		
#Modification History:  

def test0005(desc="""Test0005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table t1 cascade;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure createIndex()
	    external name 'TestDDL.createIndex' 
	    LIBRARY qa_dfr
	    language java 
           NO TRANSACTION REQUIRED
	    parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int);"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "call createIndex();"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop index idx1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop table t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure createIndex;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0006
#***************************************************************************
#Purpose: 		test SPJ with JDBC call to insert data
#Comments:		
#Modification History:

def test0006(desc="""Test0006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table t1 cascade;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure testInsert()
	    external name 'TestDML.testInsert' 
	    LIBRARY qa_dfr
	    language java 
	    parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int);"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "call testInsert();"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "select * from t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 2)

    stmt = "drop table t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure testInsert;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0007
#***************************************************************************
#Purpose: 		test SPJ with JDBC call to delete data
#Comments:		
#Modification History:

def test0007(desc="""Test0007"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table t1 cascade;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure testDelete()
	    external name 'TestDML.testDelete' 
	    LIBRARY qa_dfr
	    language java 
	    parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int);"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "insert into t1 values(100, 'aaaa', 200);"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into t1 values(200, 'bbbb', 200);"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "call testDelete();"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "select * from t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)

    stmt = "drop table t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure testDelete;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0008
#***************************************************************************
#Purpose: 		test SPJ with JDBC call to update data
#Comments:		
#Modification History:

def test0008(desc="""Test0008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)

    stmt = "drop table t1 cascade;"
    output = _dci.cmdexec(stmt)

    stmt = "create library qa_dfr file '" + defs.dfr_path + "';"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create procedure testUpdate()
	    external name 'TestDML.testUpdate' 
	    LIBRARY qa_dfr
	    language java 
	    parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int);"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "insert into t1 values(1, 'aaaa', 200);"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "insert into t1 values(2, 'bbbb', 200);"
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = "call testUpdate();"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "select * from t1 where c3 = 111;"
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    stmt = "drop table t1;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop procedure testUpdate;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = "drop library qa_dfr;"
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0009
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0302
#SPJ Parameters:	in in1 int/int
#		   	inout inout1 int/int
#			out out1 int/int
#SPJ Actions: 		none
#Comments:		An IN parameter is given as first parameter without specifying <parameter mode>
#
#Modification History: Test2016

def test0009(desc="test0009"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0302 (IN1 integer,
        inout inout1 integer, out out1 integer)
        external name 'Procs.N0302'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 123456789;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 987654321;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0302(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*123456789*987654321*""")

    stmt = """Drop procedure N0302;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0010
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0411
#SPJ Parameters:	out out1 integer / int
#	                in in1 numeric / BigDecimal
#      	        inout inout1 Double PRECISION / double
#      		IN IN2 Real / float
#SPJ Actions: 		none
#Comments:		An IN parameter is given after other parameters without specifying <parameter mode>
#Modification History: Test2017

def test0010(desc="test0010"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0411(out out1 integer, IN1 numeric,inout inout1 double precision, IN2 real)
        external name 'Procs.N0411'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 9876543;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y  1.214E7;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?z 1.2345E6;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0411(?,?x,?y,?z);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*9876543*1234500.0*""")

    stmt = """Drop procedure N0411;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0011
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0411
#SPJ Parameters:	out out1 integer / int
#	                in in1 numeric / BigDecimal
#      	        inout inout1 Double PRECISION / double
#      		IN IN2 Real / float
#SPJ Actions: 		none
#Comments:		CREATE statement contains IN parameters with and without specifying  <parameter mode>
#Modification History: Test2018

def test0011(desc="test0011"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0411(out out1 integer, IN1 numeric,inout inout1 double precision, IN IN2 real)
        external name 'Procs.N0411'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 9876543;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y  1.214E7;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?z 1.2345E6;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0411(?,?x,?y,?z);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*9876543*1234500.0*""")

    stmt = """Drop procedure N0411;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0012
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0302
#SPJ Parameters:	   IN1 integer / int
#                  	INOUT1 integer / int
#                  	OUT1 integer /int
#SPJ Actions: 		none
#Comments:		'OUT' sql indentifier is not defined
#
#Modification History: Test1953

def test0012(desc="test0012"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0302 (in in1 int, inout inout1 int, OUT int)
        external name 'Procs.N0302'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 123456789;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 987654321;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0302(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*123456789*987654321*""")

    stmt = """Drop procedure N0302;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0013
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0501
#SPJ Parameters:	in in1 Varchar(20) / String
#                  	IN IN2 integer / int
#                  	out out1 Varchar(20) / String
#      		out out2 Varchar(20) / String
#                  	out out3 Varchar(40) / String
#SPJ Actions: 		none
#Comments:		Multiple IN parameters without <sql identifier> specified
#
#Modification History: Test1981

def test0013(desc="test0013"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0501(IN varchar(20), IN integer, out out1 varchar(20), out out2 varchar(20), out out3 varchar(40))
        external name 'Procs.N0501'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0501('20002',124587,?,?,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*20002*[124587]*20002[124587]*""")

    stmt = """Drop procedure N0501;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0014
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0603
#SPJ Parameters:	IN1 largeint / long
#                  	IN2 largeint / long
#                  	INOUT1 largeint / long
#                  	INOUT2 Varchar(35) / String
#                  	OUT1 Varchar(50) / String
#SPJ Actions: 		none
#Comments:		Multiple INOUT parameters without <sql identifier> specified
#
#Modification History: Test1983

def test0014(desc="test0014"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0603 ( in in1 largeint, IN IN2 largeint, INOUT largeint,
        INOUT varchar(35), out out1 varchar(50) )
        external name 'Procs.N0603'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 47976446776434;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 75247774134477;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?a 77697674448777;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?b '1134777649764';"""
    output = _dci.cmdexec(stmt)

    stmt = """call N0603(?x,?y,?a,?b,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*7099283896260067146*7099283896260067146*7099283896260067146*""")

    stmt = """Drop procedure N0603;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                 Test0015
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0208
#SPJ Parameters:	   INOUT1 largeint / long
#                  	OUT1 Real / float
#SPJ Actions: 		none
#Comments:		'sql procedure name' and 'Java method name' are different
#
#Modification History: Test1954

def test0015(desc="test0015"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0208 (in in1 largeint, out out1 real)
        external name 'Procs.Z0208'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0208;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0016
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0209
#SPJ Parameters:	   IN1 smallint / short
#                  	OUT1 smallint / short
#SPJ Actions: 		none
#Comments:		'modifies sql data' is specified
#
#Modification History: Test1955

def test0016(desc="test0016"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0209 (in in1 smallint, out out1 smallint)
        external name 'Procs.N0209'
        library qa_spjcall
        language java
        parameter style java
        modifies sql data;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0209(32767,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*32767*""")

    stmt = """Drop procedure N0209;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0017
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0209
#SPJ Parameters:	IN1 smallint / short
#                  	OUT1 smallint / short
#SPJ Actions: 		none
#Comments:		'READS SQL DATA' is specified
#
#Modification History: Test1956

def test0017(desc="test0017"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0209 (in in1 smallint, out out1 smallint)
        external name 'Procs.N0209'
        library qa_spjcall
        language java
        parameter style java
        READS SQL DATA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0209(32250,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*32250*""")

    stmt = """Drop procedure N0209;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0018
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N1206
#SPJ Parameters:	in in1 CHAR(14) / String
#			         out out1 int / ointeger
#SPJ Actions: 		none
#Comments:		One 'DYNAMIC RESULT SETS' specified
#
#Modification History: Test1973

def test0018(desc="test0018"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1206 (in in1 CHAR(14), out out1 int)
        external name 'Procs.N1206 (java.lang.String,java.lang.Integer[])'
        library qa_spjcall
        language java
        parameter style java
        DYNAMIC RESULT SETS 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N1206('99999',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*99999*""")

    stmt = """Drop procedure N1206;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0019
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0210
#SPJ Parameters:	IN1 integer / int
#                  	OUT1 integer / int
#SPJ Actions: 		none
#Comments:		'DETERMINISTIC' is specified
#
#Modification History: Test1958

def test0019(desc="test0019"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0210 (in in1 int, out out1 int)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java
        DETERMINISTIC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0210(64548478,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*64548478*""")

    stmt = """Drop procedure N0210;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0020
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0210
#SPJ Parameters:	   IN1 integer / int
#                  	OUT1 integer / int
#SPJ Actions: 		none
#Comments:		'NOT DETERMINISTIC' is specified
#
#Modification History: Test1959

def test0020(desc="test0020"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0210 (in in1 int signed, out out1 int)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java
        NOT DETERMINISTIC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0210(64548478,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*64548478*""")

    stmt = """Drop procedure N0210;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0021
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0211
#SPJ Parameters:	   IN1 largeint / long
#                  	OUT1 largeint / long
#SPJ Actions: 		none
#Comments:		'ISOLATE' is specified
#
#Modification History: Test1960

def test0021(desc="test0021"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0211 (in in1 largeint, out out1 largeint)
        external name 'Procs.N0211'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0211(6454847874247,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*6454847874247*""")

    stmt = """Drop procedure N0211 ;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0022
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N1200
#SPJ Parameters:       IN1 integer / ointeger
#                      OUT1 Real / Float
#SPJ Actions: 		none
#Comments:		<java class name> does not contain package identifier but the class is in package
#
#Modification History: Test1986

def test0022(desc="test0022"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1200 (in in1 int, out out1 real)
        external name 'PackProcs.N1200 (java.lang.integer,float[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0023
#***************************************************************************
#Purpose:              test Create procedure command
#SPJ:                  N1200
#SPJ Parameters:       IN1 integer / ointeger
#                      OUT1 Real / Float
#SPJ Actions:          none
#Comments:             <java class name> contain <package identifier> but the class not in the package
#
#Modification History: Test1988

def test0023(desc="test0023"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1200 (in in1 int, out out1 real)
        external name 'Pack.Procs.N1200 (java.lang.integer,float[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0024
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0211
#SPJ Parameters:	IN1 largeint / long
#                  	OUT1 largeint / long
#SPJ Actions: 		none
#Comments:		Fully qualified name NSK name type setting
#
#Modification History: Test1989

def test0024(desc="test0024"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0211e (in in1 largeint, out out1 largeint)
        external name 'Procs.N0211'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0211e;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                 Test0025
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N1200
#SPJ Parameters:	  in in1 int / ointeger
#			           out out1 Real / float
#SPJ Actions: 		none
#Comments:		Partially qualified name.  ANSI name type setting
#
#Modification History: Test1965

def test0025(desc="test0025"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1200 (in in1 int, out out1 real)
        external name 'Procs.N1200 (java.lang.Integer,float[])'
        library qa_spjcall
        language java
        parameter style java
        modifies sql data;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N1200(94144424,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*9.4144424E7*""")

    stmt = """Drop procedure N1200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0026
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			N1458
#SPJ Parameters:	Procedure with IN1 and IN2 parameters.
#SPJ Actions: 		'UPSHIFT' has been given.
#Comments:
#Modification History: Test1160

def test0026(desc="test0026"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1458(in in1 varchar(25) UPSHIFT, IN IN2 varchar(25)UPSHIFT)
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N1458('radha','sudha');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1458;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
#**************************************************************************
#                                 Test0027
#***************************************************************************
#Purpose: 		Negative Tests
#SPJ:			N0184
#SPJ Parameters:	in in1 double / float(23)
#SPJ Actions: 		Decinal value passed to short from inside a Sqlj0 program.
#Comments:
#Modification History: Test1165

def test0027(desc="test0027"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0184 (in in1 FLOAT(23))
        external name 'Procs.N0184'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0184(123456.8547);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0184;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0028
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			N1452
#SPJ Parameters:	Procedure with two parameteno parameters.
#SPJ Actions: 		Execute an SPJ using Sqlj0 Calling program.
#Comments:
#Modification History: Test1154

def test0028(desc="test0028"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1453(in in1 varchar(25), IN IN2 varchar(25))
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N1453('error','right');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1453;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0029
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			N1452
#SPJ Parameters:	Procedure with IN and INOUT parameters.
#SPJ Actions: 		IN and INOUT parameters.
#Comments:
#Modification History: Test1155

def test0029(desc="test0029"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1457(in in1 varchar(25), inout inout1 varchar(25))
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0030
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			N1453
#SPJ Parameters:	Procedure with IN1 and IN2 parameters.
#SPJ Actions:
#Comments:
#Modification History: Test1156

def test0030(desc="test0030"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1453(in in1 varchar(25), IN IN2 varchar(25))
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1453;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0031
#***************************************************************************
#Purpose: 		Create procedure tests.
#SPJ:			N4249
#SPJ Parameters:	in in1 double /Double PRECISION
#			inout inout1 double /Double PRECISION
#SPJ Actions: 		IN, OUT modes have been specified in Create procedure.
#Comments:		None
#Modification History: Test1203

def test0031(desc="test0031"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4249 (IN double precision, INOUT double precision)
        external name 'Procs.N4249'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N4249;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                  Test0032
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			M100B
#SPJ Parameters:	Procedure with no parameters.
#SPJ Actions: 		None.
#Comments:		Procedure name in quotes(valid).
#Modification History: Test1246

def test0032(desc="test0032"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure "''" (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure "''";"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure "%**" (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure "%**";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0033
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N0525
#SPJ Parameters:	IN1 NCHAR / String
#                  	OUT1 Varchar / String
#SPJ Actions: 		none
#Comments:		National Character set as SQL data type.
#
#Modification History: Test1990

def test0033(desc="test0033"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0525 ( in in1 NCHAR(21), out out1 varchar(15))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0525;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0034
#***************************************************************************
#Purpose: 		'Create SPJ'  without specifying IN parameter mode
#			and with invalid signature.
#SPJ:			N0166
#SPJ Parameters:	None.
#SPJ Actions: 		To check that the default parameter shall be IN mode.
#Comments:		Procedure 'SPJTEST' will NOT be created after Call execution.
#Modification History: Test1253

def test0034(desc="test0034"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0166 ()
        external name 'hp2004.N0166'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0166();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """drop procedure N0166;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure N0166;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0035
#***************************************************************************
#Purpose: 		'Create SPJ'.Many IN parameters without parameter mode
#SPJ:			N0168
#SPJ Parameters:	None.
#SPJ Actions: 		Parameter modes are given in different order.
#Comments:		Procedure 'SPJTEST' will NOT be created after Call execution.
#Modification History: Test1255

def test0035(desc="test0035"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0168 ()
        external name 'hp2004.N0168'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0168();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """drop procedure N0168;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0036
#***************************************************************************
#Purpose: 		Create procedrue Testing.
#SPJ:			NA19
#SPJ Parameters:	SPJ consists of only INOUT parameter.(parameter mode INOUT)
#SPJ Actions: 		none
#Comments:
#Modification History: Test2037

def test0036(desc="test0036"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure NA19 (inout inout1 largeint) external name 'Spjqa.NA19'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure NA19;"""
    output = _dci.cmdexec(stmt)

#SPJ Parameters:	SPJ consists of only OUT parameter.
    stmt = """Create procedure NA20 (out out1 largeint)
        external name 'Spjqa.NA20'
        library qa_spjcall
        language java parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure NA20;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0037
#***************************************************************************
#Purpose: 		Create procedrue Testing.
#SPJ:			NA200
#SPJ Parameters:	SPJ name created with double quotes;
#SPJ Actions: 		none
#Comments:
#Modification History: Test2039

def test0037(desc="test0037"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure "NA200" (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure "NA200";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0038
#***************************************************************************
#Purpose: 		Create procedrue Testing.
#SPJ:			NB200
#SPJ Parameters:	SPJ name given with under score.
#SPJ Actions: 		none
#Comments:
#Modification History: Test2040

def test0038(desc="test0038"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure NB_200 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure "NB_200";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0039
#***************************************************************************
#Purpose: 		Create procedrue Testing.
#SPJ:			NC200
#SPJ Parameters:	Lengthy SPJ name has been given. 130 Characters.
#SPJ Actions: 		none
#Comments:
#Modification History: Test2041

def test0039(desc="test0039"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure This_java_stored_procedure_is_so_long_and_this_testcase_is_intended_to_test_the_allowable_length_of_the_java_stored_procedure_name(in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

#SPJ Parameters:	Lengthy SPJ name has been given. 128 Characters.Acceptable.
    stmt = """Create procedure This_java_stored_procedure_is_so_long_and_this_testcase_is_intended_to_test_the_allowable_length_of_the_java_stored_procedure_sp(in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure This_java_stored_procedure_is_so_long_and_this_testcase_is_intended_to_test_the_allowable_length_of_the_java_stored_procedure_sp;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0040
#***************************************************************************
#Purpose: 		Create procedrue Testing.
#SPJ:			NE200
#SPJ Parameters:	SPJ name has given in sigle quotes.
#SPJ Actions: 		none
#Comments:
#Modification History: Test2044

def test0040(desc="test0040"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure 'NE200' (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Create procedure "NF-200" (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call "NF-200"('Procedure name is quotes ',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure "NF-200";"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure "NG 200" (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call "NG 200"('Procedure name is quotes ',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure "NG 200";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0041
#***************************************************************************
#Purpose: 		test Java exceptions
#SPJ:			N1320
#SPJ Parameters:	N1320: in in1 Varchar(9)/String, out out1 Varchar(9)/String
#SPJ Actions: 		none
#Comments:		String data provided has more characters than specified
#Modification History: Test2232

def test0041(desc="test0041"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1320 (in in1 varchar(9), out out1 varchar(9))
        external name 'nProcs.N1320'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N1320 ('God Bless America',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "8402")

    stmt = """Drop procedure N1320;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0042
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			N1453
#SPJ Parameters:	Procedure with IN1 and IN2 parameters.
#SPJ Actions:
#Comments:
#Modification History: Test2423

def test0042(desc="test0042"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1453(in in1 varchar(25), IN IN2 varchar(25))
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1453;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N1454(in in1 varchar(25), out out1 varchar(25))
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Create procedure N1455(in in1 varchar(25), IN IN2 varchar(25))
        external name 'mainmethod.main(java.lang.String[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1455;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N1456(in in1 varchar(25), IN IN2 varchar(25))
        external name 'mainmethod.main(java.lang.String[],java.lang.String[] )'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Create procedure N1457(in in1 varchar(25), inout inout1 varchar(25))
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0043
#***************************************************************************
#Purpose: 		Test Create procedure Command.
#SPJ:			N1458
#SPJ Parameters:	Procedure with IN1 and IN2 parameters.
#SPJ Actions: 		'UPSHIFT' has been given.
#Comments:
#Modification History: Test2428

def test0043(desc="test0043"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1458(in in1 varchar(25) UPSHIFT, IN IN2 varchar(25)UPSHIFT)
        external name 'mainmethod.main'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1458;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0044
#***************************************************************************
#Purpose: 		Create procedure with prepare command.
#SPJ:			N0200
#SPJ Parameters:	None.
#SPJ Actions: 		None.
#Comments:		None.
#Modification History: Test2494

def test0044(desc="test0044"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Drop procedure N0210;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare s from
        Create procedure N0210 (integer, out out1 integer)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2494""", "verify")

    stmt = """Drop procedure N0210;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0045
#***************************************************************************
#Purpose: 		CQD for incompatible comparison.
#SPJ:			N0200
#SPJ Parameters:	None.
#SPJ Actions: 		None.
#Comments:		None.
#Modification History: Test2495

def test0045(desc="test0045"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """delete from testtab;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into testtab values(
        'AAA Computers',
        1234567890,
        'San Francisco',
        'programmer',
        123456789,
        32766,
        date '2001-10-30',
        time '10:10:10',
        timestamp '2001-10-10 10:10:10.00',
        123456789987654321,
        3.40E+37,
        3.0125E+18,
        1.78145E+75,
        8765432.45678,
        8765478.56895,
        987654321.0,
        123456789.0);"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N0200 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0200((Select e_name from Testtab where e_date > '1997-02-28'),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2495""", "verify1")

    stmt = """control query default allow_incompatible_comparison 'ON';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0200((Select e_name from Testtab where e_date > '1997-02-28'),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")
    _dci.expect_file(output, defs.test_dir + """/t2495""", "verify")

    stmt = """Drop procedure N0200;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop procedure n0001;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0046
#***************************************************************************
#Purpose: 		Preparing and executing 26 SPJs
#SPJ:			Many procedures.
#SPJ Parameters:	None.
#SPJ Actions: 		Preparing and executing many SPJS.
#Comments:		None.
#Modification History: Test1289

def test0046(desc="test0046"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0001 ()
        external name 'Procs.N0001'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure NA014 (in in1 smallint, out out1 integer)
        external name 'Spjqa.NA014 (short,java.lang.Integer[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure NA016 (in in1 int, out out1 integer)
        external name 'Spjqa.NA016 (int,java.lang.Integer[])'
        library qa_spjcall
        parameter style java
        language java	;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0202 (in in1 numeric, out out1 numeric)
        external name 'Procs.N0202'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0204 (in in1 smallint, out out1 real)
        external name 'Procs.N0204'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0208 (inout inout1 largeint, in in1 real)
        external name 'Procs.N0208'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0210 (in in1 integer, out out1 integer)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0211 (in in1 largeint, out out1 largeint)
        external name 'Procs.N0211'
        library qa_spjcall
        language java parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0212 (in in1 real, out out1 real)
        external name 'Procs.N0212'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0213 (in in1 double precision, out out1 double precision)
        external name 'Procs.N0213'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0214 (in in1 CHAR(25), out out1 varchar(25))
        external name 'Procs.N0214'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0215 (in in1 Date, out out1 Date)
        external name 'Procs.N0215'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0216 (in in1 TIME, out out2 TIME)
        external name 'Procs.N0216'
        library qa_spjcall
        parameter style java
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0217 (in in1 Timestamp, out out1 Timestamp)
        external name 'Procs.N0217'
        library qa_spjcall
        parameter style java
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0300 (in in1 CHAR(30),inout inout1 varchar(30), out out1 varchar(45))
        external name 'Procs.N0300'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0302 (IN integer,
        inout inout1 integer, out out1 integer)
        external name 'Procs.N0302'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0303 (in in1 smallint,inout inout1 smallint, out out1 smallint)
        external name 'Procs.N0303'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0304 (in in1 largeint,
        inout inout1 largeint, out out1 largeint)
        external name 'Procs.N0304'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0306 (in in1 integer,
        out out1 varchar(50), inout inout1 smallint )
        external name 'Procs.N0306'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0309 (out out1 varchar(50),in in1 numeric,inout inout1 integer)
        external name 'Procs.N0309'
        library qa_spjcall
        language java parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0311 (in in1 decimal(8,2),
        inout inout2 decimal(8,2) signed,
        out out3 decimal(8,2))
        external name 'Procs.N0311'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0315(in in1 real, inout inout1 real, out out1 real)
        external name 'Procs.N0315'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0316(in in1 double precision, inout inout1 double precision, out out1 double precision)
        external name 'Procs.N0316'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0411(out out1 integer, in in1 numeric,inout inout1 double precision, IN IN2 real)
        external name 'Procs.N0411'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0501(in in1 varchar(20), IN IN2 integer,
        out out1 varchar(20), out out2 varchar(20), out out3 varchar(40))
        external name 'Procs.N0501'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """prepare a from Call N0001();"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare c from call NA014(32321,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare d from call NA016(32321854,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare e from call N0202(1234567.0,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare f from call N0204(11085,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?x 1234567894125;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare g from call N0208(?x,1.01E12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?x 'NONSTOPDIVISION';"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 'AAA CORPORATION';"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare h from call N0300(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?u 12345;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?v 32225;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare j from call N0303(?u,?v,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?x 1234567789965445;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 9876543478558474;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare k from call N0304(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?p 12345;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?q 31012;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare l from call N0306(?p,?,?q);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?ab 123465.67;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?ba 987657.43;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare n from call N0311(?ab,?ba,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?x 1.2346E12;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 2.8765E7;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare o from call N0315(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """set param ?x 1.18456855E22;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y  1.0214578E33;"""
    output = _dci.cmdexec(stmt)

    stmt = """prepare p from call N0316(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare r from Call N0501('HELLO WORLD',123456,?x,?y,?z);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare s from Call N0215(current_date,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare t from Call N0216(current_time,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare u from Call N0217(current_timestamp,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare v from Call N0210(987654321,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare w from Call N0211(98765432123456789,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare x from Call N0212(2.245E15,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare y from Call N0213(2.245E75,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """prepare z from Call N0214('PreparingHere',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL command prepared.*""")

    stmt = """execute a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute g;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*numeric_out_of_range*""")

    stmt = """execute h;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute j;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute k;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*numeric_out_of_range*""")

    stmt = """execute l;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute n;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute o;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute r;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute t;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute u;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute v;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute w;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute y;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """execute z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure  N0001;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  NA014;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  NA016;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0202;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0204;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0208;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0300;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0302;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0303;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0304;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0306;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0309;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0311;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0315;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0316;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0411;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0501;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0215;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0216;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0217;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0210;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0211;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0212;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0213;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure  N0214;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0047
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			NA016
#SPJ Parameters:	IN1 int / int
#			OUT1 integer /java.lang.integer.
#SPJ Actions: 		none
#Comments:
#Modification History: Test1443

def test0047(desc="test0047"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure NA016 (in in1 int, out out1 integer)
        external name 'Spjqa.NA016 (int,java.lang.Integer[])'
        library qa_spjcall
        parameter style java
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call NA016(32321854,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1443""", "verify")

    stmt = """call NA016(12E32,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure NA016;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                             Test0048
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0210
#SPJ Parameters:	IN1 integer / int
#                  	OUT1 integer / int
#SPJ Actions: 		none
#Comments:
#Modification History: Test2383

def test0048(desc="test0048"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0210 (in in1 integer, out out1 integer)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0210(1.234567E8,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2383""", "verify")

    stmt = """call N0210(-1.234567E+8,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2384""", "verify")

    stmt = """call N0210(-1.234567+-8,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2385""", "verify")

    stmt = """call N0210(15*25/52*78,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2386""", "verify")

    stmt = """call N0210(sqrt(98989898989898989),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2387""", "verify")

    stmt = """call N0210(exp(1.2145),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2388""", "verify")

    stmt = """call N0210(exp(log(1.2145)),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2389""", "verify")

    stmt = """call N0210(extract(year from date '2003-01-08'),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2390""", "verify")

    stmt = """call N0210(floor(1.2547),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2391""", "verify")

    stmt = """call N0210(power(15,5),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2392""", "verify")

    stmt = """control query default ALLOW_RAND_FUNCTION 'ON';"""
    output = _dci.cmdexec(stmt)

    stmt = """call N0210(rand(),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2393""", "verify")

    stmt = """control query default ALLOW_RAND_FUNCTION 'OFF';"""
    output = _dci.cmdexec(stmt)

    stmt = """call N0210(radians(25417845),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2394""", "verify")

    stmt = """call N0210(tan(45),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2395""", "verify")

    stmt = """call N0210(tanh(79+6446743454),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2396""", "verify")

    stmt = """call N0210(ABS(79+6446.7543447),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2397""", "verify")

    stmt = """call N0210(ATAN(TAN(1.7543447)),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2398""", "verify")

    stmt = """call N0210(ATAN2(1.192, -2.3),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2399""", "verify")

    stmt = """call N0210(CEILING(747.643447),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2400""", "verify")

    stmt = """call N0210(cos(tan(sin(tan(cos(sin(45)))))),?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2401""", "verify")

    stmt = """Drop procedure N0210;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0049
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			NA014
#SPJ Parameters:	IN1 SHORT / short
#			OUT1 integer /java.lang.integer.
#SPJ Actions: 		none
#Comments:
#Modification History: Test1441

def test0049(desc="test0049"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure NA014 (in in1 smallint, out out1 integer)
        external name 'Spjqa.NA014 (short,java.lang.Integer[])'
        library qa_spjcall
        parameter style java
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call NA014(32321,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1441""", "verify")

    stmt = """call NA014(-25658,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1442""", "verify")

    stmt = """Drop procedure NA014;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                            Test0050
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0204
#SPJ Parameters:	IN1 smallint / short
#                 	OUT1 Real / float
#SPJ Actions: 		none
#Comments:
#Modification History: Test1458

def test0050(desc="test0050"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0204 (in in1 smallint, out out1 real)
        external name 'Procs.N0204'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0204(11085,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1458""", "verify")

    stmt = """call N0204(1108E45,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0204;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                             Test0051
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0208
#SPJ Parameters:	INOUT1 largeint / long
#                      IN1 Real / float
#SPJ Actions: 		none
#Comments:		IN
#Modification History: Test1462

def test0051(desc="test0051"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0208 (inout inout1 largeint, in in1 real)
        external name 'Procs.N0208'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 1234567894125;"""
    output = _dci.cmdexec(stmt)

    stmt = """call N0208(?x,1.01E12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1462""", "verify")

    stmt = """Drop procedure N0208;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0052
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0211
#SPJ Parameters:	IN1 largeint / long
#                      OUT1 largeint / long
#SPJ Actions: 		none
#Comments:
#Modification History: Test1465

def test0052(desc="test0052"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Drop procedure N0211 ;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N0211 (in in1 largeint, out out1 largeint)
        external name 'Procs.N0211'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0211(1234567894125445888,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1465""", "verify")

    stmt = """Drop procedure N0211 ;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0053
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0212
#SPJ Parameters:	IN1 Real / float
#                      OUT1 Real / float
#SPJ Actions: 		none
#Comments:
#Modification History: Test1466

def test0053(desc="test0053"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0212 (in in1 real, out out1 real)
        external name 'Procs.N0212'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0212(1.201227E13,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1466""", "verify")

    stmt = """Drop procedure N0212;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0054
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0213
#SPJ Parameters:	IN1 IN1 Double/ Double Precision
#			out out1 Double/ Double Precision
#SPJ Actions: 		None.
#Comments:		Max positive value with negative exp to double.
#Modification History: Test1332

def test0054(desc="test0054"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Drop procedure N0213;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N0213 (in in1 double precision, out out1 double precision)
        external name 'Procs.N0213'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0213(2.2250738585072014e-308,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1332""", "verify")

    stmt = """Drop procedure N0213;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                  Test0055
#***************************************************************************
#Purpose: 		Basic functionality
#SPJ:			N0199
#SPJ Parameters:	IN BigDecimal /s9999V9999;
#			OUT BigDecimal /s9999V9999;
#SPJ Actions: 		None.
#Comments:		Truncation takes place.
#Modification History: Test1343

def test0055(desc="test0055"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0199(in in1 pic s9 , out out1 picture s9)
        external name 'Procs.N0199'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0199(9876.543257979,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "8411")

    stmt = """drop procedure N0199;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test56
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0214
#SPJ Parameters:	in in1 CHAR(25) / String
#                      out out1 Varchar(25) / String
#SPJ Actions: 		none
#Comments:
#Modification History: Test1468

def test0056(desc="test0056"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0214 (in in1 CHAR(25), out out1 varchar(25))
        external name 'Procs.N0214'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """call N0214('HELLOWORLD',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1468""", "verify")

    stmt = """Drop procedure N0214;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#************************************************************************
#                                  Test0057
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0236
#SPJ Parameters:	in in1 Varchar/string
#			out out1 largeinteger/long
#SPJ Actions: 		None.
#Comments:
#Modification History: Test1497

def test0057(desc="test0057"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0236 (in in1 varchar(50), out out1 largeint)
        external name 'Procs.N0236'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0236 ('125478456568',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1497""", "verify")

    stmt = """Drop procedure N0236;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                 Test0058
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0300
#SPJ Parameters:	IN1 IN1 String/ Nchar
#			inout inout1 String/ Nchar
#			out out1 String/ Nchar
#SPJ Actions: 		None.
#Comments:		None.
#Modification History: Test1131

def test0058(desc="test0058"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """delete from testtab;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N0300 (in in1 NCHAR(50),inout inout1 NCHAR(50),
        out out1 NCHAR(45))
        external name 'Procs.N0300'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x _ucs2'AAA Computers';"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y _ucs2'Hewlett Packard';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0300(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1131""", "verify")

    stmt = """Drop procedure N0300 ;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                  Test0059
#***************************************************************************
#Purpose: 		Basic functionality
#SPJ:			N0200
#SPJ Parameters:	IN String /pic x(50);
#			OUT String varchar(50);
#SPJ Actions: 		None.
#Comments:
#Modification History: Test1339

def test0059(desc="test0059"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0200 (PIC X(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0200('sql pic x data type',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1339""", "verify")

    stmt = """Drop procedure N0200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#************************************************************************
#                                  Test0060
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0222
#SPJ Parameters:	in in1 Date / Date
#SPJ Actions: 		largeinteger value supplied for date.
#Comments:
#Modification History: Test1484

def test0060(desc="test0060"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0222 (in in1 DATE)
        external name 'Procs.N0222'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0222(123456789987654321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """call N0222(1114317);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Call N0222(123456789.0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0222;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#************************************************************************
#                                  Test0061
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0300
#SPJ Parameters:	in in1 String/Nchar upshift
#			inout inout1  String/Nchar upshift
#			out out1  String/Nchar upshift
#SPJ Actions: 		None.
#Comments:
#Modification History: Test1486

def test0061(desc="test0061"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0300 (in in1 NCHAR(6)UPSHIFT,inout inout1 NCHAR(6)UPSHIFT,
        out out1 	NCHAR(6) UPSHIFT)
        external name 'Procs.N0300'
        library qa_spjcall
        language java parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 'AAA';"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 'denver';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0300(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1486""", "verify")

    stmt = """Drop procedure N0300 ;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#************************************************************************
#                                  Test0062
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0223
#SPJ Parameters:	in in1 Time / time
#SPJ Actions: 		String value supplied for time.
#Comments:
#Modification History: Test1488

def test0062(desc="test0062"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0223 (in in1 TIME)
        external name 'Procs.N0223'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0223('hello world');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Call N0223(12345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0223;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#************************************************************************
#                                  Test0063
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0224
#SPJ Parameters:	in in1 Timestamp/ timesatmp
#SPJ Actions: 		String value supplied for timestamp.
#Comments:
#Modification History: Test1491

def test0063(desc="test0063"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0224 (in in1 TIMESTAMP)
        external name 'Procs.N0224'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0224('AAA computers');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Call N0224(12345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Call N0224(123456789.0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR[4303]*""")

    stmt = """Drop procedure N0224;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                               Test0064
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N1336Z
#SPJ Parameters:
#SPJ Actions: 		Language name has been changed
#Comments:
#Modification History: Test2225

def test0064(desc="test0064"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1336X(in in1 integer, out out1 integer)
        external name 'Spjqa.N1336X'
        library qa_spjcall
        LANGUAGE C
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                            Test0065
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N1336Z
#SPJ Parameters:
#SPJ Actions: 		Parameters order has been changed
#Comments:
#Modification History: Test2226

def test0065(desc="test0065"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1336X(out out1 integer,in in1 integer)
        external name 'Spjqa.N1336X'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                            Test0066
#***************************************************************************
#Purpose: 		test basic functionality
#SPJ:			N0305
#SPJ Parameters:
#SPJ Actions: 		none
#Comments:		Scale is greater than precision. Not acceptable.
#Modification History: Test2227

def test0066(desc="test0066"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure N0305;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N0305 (in in1 numeric(8,11), inout inout1 numeric(8,11))
        external name 'Procs.N0305'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "3015")

    stmt = """Create procedure N0305 (in in1 numeric(9,9), inout inout1 numeric(9,9))
        external name 'Procs.N0305'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure N0305;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N0305 (in in1 decimal(35,23), inout inout1 decimal(35,23))
        external name 'Procs.N0305'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "3016")

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                  Test0067
#***************************************************************************
#Purpose: 		Basic functionality
#SPJ:			N0210
#SPJ Parameters:	None.
#SPJ Actions: 		None.
#Comments:		Drop procedure with Restrict option.
#Modification History: Test1337

def test0067(desc="test0067"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0210 (in in1 integer, out out1 integer)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure N0210 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1337""", "verify")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                  Test0068
#***************************************************************************
#Purpose: 		Basic functionality
#SPJ:			N0210
#SPJ Parameters:	None.
#SPJ Actions: 		None.
#Comments:		Drop procedure with Restrict option.
#Modification History: Test1338

def test0068(desc="test0068"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0210 (in in1 integer, out out1 integer)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """drop procedure N0210 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0210;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0069
#***************************************************************************
#Purpose: 		TestDrop procedure
#SPJ:			N4106
#SPJ Parameters:	IN1 Double PRECISION /double
#			OUT1 Double PRECISION /double
#			INOUT1 Varchar /String
#SPJ Actions: 		none
#Comments:		Procedure does not exist.(Tried to drop twice)
#Modification History: Test1925

def test0069(desc="test0069"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4106 (in in1 double precision, out out1 double precision,inout inout1 varchar(25) )
        external name 'Procs.N4106'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N4106;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure N4106;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0070
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N0311
#SPJ Parameters:	in in1 numeric(9,3) / Decimal
#      	         inout inout2 numeric(9,3) / Decimal
#      	         out out3 numeric(9,3) / Decimal
#SPJ Actions: 		none
#Comments:		Number of parameters given for procedure does not match the definition
#			of Java method name
#
#Modification History: Test1966

def test0070(desc="test0070"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0311 (in in1 numeric(9,3),inout inout1 numeric(9,3))
        external name 'Procs.N0311'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0071
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1203
#SPJ Parameters:	in in1 largeint / oLong
#			         out out1 largeint / oLong
#SPJ Actions: 		none
#Comments:		Number of parameters given for procedure does not match Java signature given
#
#Modification History: Test1967

def test0071(desc="test0071"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1203 (in in1 largeint, out out1 largeint)
        external name 'Procs.N1203 (java.lang.Long[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0072
#***************************************************************************
#Purpose: 		Negative test Create procedure command
#SPJ:			N1203
#SPJ Parameters:	in in1 largeint / oLong
#			         out out1 largeint / oLong
#SPJ Actions: 		none
#Comments:		Java signature given does not match Java method
#
#Modification History: Test1968

def test0072(desc="test0072"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1203 (in in1 largeint, out out1 largeint)
        external name 'Procs.N1203 (java.lang.integer,java.lang.Long[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0073
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1203
#SPJ Parameters:	in in1 largeint / oLong
#			         out out1 largeint / oLong
#SPJ Actions: 		none
#Comments:		Java signature is not given and default mappings are not acceptable
#
#Modification History: Test1969

def test0073(desc="test0073"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1203 (in in1 largeint, out out1 largeint)
        external name 'Procs.N1203'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0074
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1206
#SPJ Parameters:	in in1 CHAR(14) / String
#			         out out1 int / ointeger
#SPJ Actions: 		none
#Comments:		Invalid <path dir> given for 'external path'
#
#Modification History: Test1970

def test0074(desc="test0074"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1206 (in in1 CHAR(14), out out1 int)
        external name 'Procs.N1206 (java.lang.String,java.lang.integer[])'
        external path '/usr.Nxxx/Nxxxx/'
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0075
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1206
#SPJ Parameters:	in in1 Varchar(34) / String
#		         	out out1 int / ointeger
#SPJ Actions: 		none
#Comments:		Valid but non-existent <path dir> given for 'external path'
#
#Modification History: Test1971

def test0075(desc="test0075"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1206 (in in1 varchar(34), out out1 int)
        external name 'Procs.N1206 (java.lang.String,java.lang.Integer[])'
        external path '/usr/spjqa/Testware/Clause'
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0076
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1206
#SPJ Parameters:	in in1 Varchar(34) / String
#			         out out1 int / ointeger
#SPJ Actions: 		none
#Comments:		'external path' missing
#
#Modification History: Test1972

def test0076(desc="test0076"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1206 (in in1 varchar(34), out out1 int)
        external name 'Procs.N1206 (java.lang.String,java.lang.integer[])'
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "3201")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0077
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1300
#SPJ Parameters:	in in1 int / ointeger
#			         inout inout1 int / ointeger
#			         out out1 largeint / long
#SPJ Actions: 		none
#Comments:		'language java' and 'parameter style java;' left out
#
#Modification History: Test1975

def test0077(desc="test0077"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1300 (in in1 int, inout inout1 int, out out1 largeint)
        external name 'Procs.N1300 (java.lang.integer,java.lang.integer[],long[])'
        library qa_spjcall
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0078
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1300
#SPJ Parameters:	in in1 int / ointeger
#			         inout inout1 int / ointeger
#			         out out1 largeint / long
#SPJ Actions: 		none
#Comments:		'language java' left out
#
#Modification History: Test1976

def test0078(desc="test0078"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1300 (in in1 largeint, inout inout1 largeint, out out1 largeint)
        external name 'Procs.N1300b (java.lang.Long,java.lang.Long[],long[])'
        library qa_spjcall
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0079
#***************************************************************************
#Purpose: 		test Create procedure command
#SPJ:			N1300
#SPJ Parameters:	in in1 int / ointeger
#			         inout inout1 int / ointeger
#			         out out1 largeint / long
#SPJ Actions: 		none
#Comments:		'parameter style java;' is optional
#
#Modification History: Test1977

def test0079(desc="test0079"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1300 (in in1 int, inout inout1 int, out out1 largeint)
        external name 'Procs.N1300 (java.lang.Integer,java.lang.Integer[],long[])'
        library qa_spjcall
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0080
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1300
#SPJ Parameters:	in in1 int / ointeger
#			         inout inout1 int / ointeger
#			         out out1 largeint / long
#SPJ Actions: 		none
#Comments:		Java method is not declared public static void
#
#Modification History: Test1978

def test0080(desc="test0080"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1300 (in in1 int, inout inout1 int, out out1 largeint)
        external name 'Procs.N1300a (java.lang.integer,java.lang.integer[],long[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0081
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N1300
#SPJ Parameters:	in in1 int / ointeger
#			         inout inout1 int / ointeger
#			         out out1 largeint / long
#SPJ Actions: 		none
#Comments:		Java method is overloaded
#
#Modification History: Test1979

def test0081(desc="test0081"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """drop procedure N1300e;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create procedure N1300e (in in1 largeint,inout inout1 largeint,out out1 largeint)
        external name 'Procs.N1300b (java.lang.Long,java.lang.Long[],long[])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N1300e;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#**************************************************************************
#                                 Test0082
#***************************************************************************
#Purpose: 		Negative Tests
#SPJ:			N0187
#SPJ Parameters:	in in1 float / Real
#SPJ Actions: 		Double value passed to short from inside a Sqlj0 program.
#Comments:
#Modification History: Test1167

def test0082(desc="test0082"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0187 (in in1 largeint)
        external name 'Procs.N0187'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0187(1.245E45,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0187;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0083
#***************************************************************************
#Purpose: 		Negative Tests
#SPJ:			N0176
#SPJ Parameters:	in in1 float / Real
#SPJ Actions: 		Double value passed to real from inside a Sqlj0 program.
#Comments:
#Modification History: Test1166

def test0083(desc="test0083"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0176 (in in1 real)
        external name 'Procs.N0176'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0176(1.4112E35,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0176;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0086
#***************************************************************************
#Purpose: 		Negative Tests
#SPJ:			N1458
#SPJ Parameters:	in in1 int / integer
#SPJ Actions: 		Real value passed to integer.
#Comments:		Call Fails with an error.
#Modification History: Test1163

def test0086(desc="test0086"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0185 (in in1 integer)
        external name 'Procs.N0185'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0185(1.25E12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0185;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0087
#***************************************************************************
#Purpose: 		Negative Tests
#SPJ:			N0186
#SPJ Parameters:	in in1 short / smallint
#SPJ Actions: 		Decinal value passed to short from inside a Sqlj0 program.
#Comments:		Call Fails with an error.
#Modification History: Test1164

def test0087(desc="test0087"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0186 (in in1 smallint)
        external name 'Procs.N0186'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0186(14314.79464647);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0186;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0088
#***************************************************************************
#Purpose: 		Negative Tests
#SPJ:			N0184
#SPJ Parameters:	in in1 double / float
#SPJ Actions: 		Creating SPJs with float(22) and float(23)
#Comments:
#Modification History: Test1168

def test0088(desc="test0088"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0184 (in in1 FLOAT(23))
        external name 'Procs.N0184'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0184;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Create procedure N0184 (in in1 FLOAT(22))
        external name 'Procs.N0184'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0184;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**************************************************************************
#                                 Test0089
#***************************************************************************
#Purpose: 		negative test Create procedure Command.
#SPJ:			M100
#SPJ Parameters:	Procedure with no parameters.
#SPJ Actions: 		None.
#Comments:		Invalid java signature provided.
#Modification History: Test1242

def test0089(desc="test0089"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure M100 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200 (java.lang.String,java.lang.String)'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Create procedure M100 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200 ()'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Create procedure M100 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200 (java.lang.Double,java.lang.String [])'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "11211")

    stmt = """Create procedure M100 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200 (java.lang.String,)'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "11210")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0090
#***************************************************************************
#Purpose: 		negative test Create procedure command
#SPJ:			N0211
#SPJ Parameters:	IN1 smallint / short
#                  	OUT1 integer / java.lang.integer
#SPJ Actions: 		none
#Comments:		Java Signature has not been specified.
#
#Modification History: Test1963

def test0090(desc="test0090"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure NA014 (in in1 smallint, out out1 integer)
        external name 'Spjqa.NA014'
        library qa_spjcall
        parameter style java
        language java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0091
#***************************************************************************
#Purpose: 		Error Handling
#SPJ:			ProcsN4264
#SPJ Parameters:	IN1 Varchar / String
#			OUT1 Varchar / String
#SPJ Actions: 		none
#Comments:		SPJ throws uncaught SQL exception and SPJ is defined with
#			'modifies sql data'
#Modification History: Test2318

def test0091(desc="test0091"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4264 (in in1 varchar(30), out out1 varchar(45))
        external name 'Procs.N4264'
        library qa_spjcall
        language java     parameter style java
        modifies sql data;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N4264;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0092
#***************************************************************************
#Purpose: 		Error Handling
#SPJ:			ProcN0202
#SPJ Parameters:	IN1 decimal/ BigDecimal
#              	OUT1 decimal/ BigDecimal
#SPJ Actions: 		none
#Comments:		SPJ catches SQL exception.
#			Execute a procedure which was dropped.
#Modification History: Test1934

def test0092(desc="test0092"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0202 (in in1 decimal(9), out out1 decimal(9))
        external name 'Procs.N0202'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)

    stmt = """Drop procedure N0202;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0202(123456.12,654321.21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """**** ERROR[1389]*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0093
#***************************************************************************
#Purpose: 		Error Handling
#SPJ:			ProcsN0202
#SPJ Parameters:	IN1 numeric / BigDecimal
#                      OUT1 numeric /  BigDecimal
#SPJ Actions: 		none
#Comments:		SPJ catches Java exception.
#Modification History: Test1935

def test0093(desc="test0093"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0202 (in in1 numeric, out out1 numeric)
        external name 'Procs.N0202'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0202('hello wolrd',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """**** ERROR[4303]*""")

    stmt = """Drop procedure N0202;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0094
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for INPUT parameters.
#SPJ:			N4256
#SPJ Parameters:	IN1 largeint / long
#                      INOUT1 Double PRECISION  / double
#SPJ Actions: 		none
#Comments:		Double where largeint expected.
#Modification History: Test1862

def test0094(desc="test0094"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4256 (in in1 largeint, inout inout1 double precision)
        external name 'Procs.N4256'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 794147558314435;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y  1.164E72;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N4256(?x,?y);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1862""", "verify")

    stmt = """Drop procedure N4256;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                  Test0095
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1166
#SPJ Parameters:	IN	:Long/largeint
#			INOUT	:BigDecimal/Decimal without scale
#			OUT	:BigDecimal/Decimal without scale
#SPJ Actions: 		none
#Comments:
#Modification History: Test2089

def test0095(desc="test0095"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1166(in in1 largeint, inout inout1 decimal(9,0),
        out out1 decimal(9,0))
        external name 'Spjip.N1166'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 987654321;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 123456789.0;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1166(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2089""", "verify")

    stmt = """Drop procedure N1166;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                  Test0096
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1166
#SPJ Parameters:	IN	:Long/largeint
#			INOUT	:BigDecimal/numeric with scale
#			OUT	:BigDecimal/numeric with scale
#SPJ Actions: 		none
#Comments:
#Modification History: Test2090

def test0096(desc="test0096"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1166(in in1 largeint, inout inout1 numeric(16,7),
        out out1 numeric(16,7))
        external name 'Spjip.N1166'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 987654321;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 123456789.65432;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1166(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2090""", "verify")

    stmt = """Drop procedure N1166;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0097
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for OUTPUT parameters.
#SPJ:			ProcN0202
#SPJ Parameters:	IN1 decimal/ BigDecimal
#              	OUT1 decimal/ BigDecimal
#SPJ Actions: 		none
#Comments:	        DEC value given is declared with higher SCALE than
#                      declared for SPJ, truncation occurs
#CREATED		:Srinivas Nelluru  on 04/24/2001
#Modification History: Test2252

def test0097(desc="test0097"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0202 (in in1 decimal(17,8), out out1 decimal(17,8))
        external name 'Procs.N0202'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 123456789.987654321;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0202(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2252""", "verify")

    stmt = """Drop procedure N0202;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                 Test0098
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1304
#SPJ Parameters:	INOUT	:float/Real
#			OUT	:double/Float
#SPJ Actions: 		none
#Comments:
#Modification History: Test2213

def test0098(desc="test0098"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1304(inout inout1 real, out out1 FLOAT(24))
        external name 'Spjip.N1304'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 1.85657854E4;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1304(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2213""", "verify")

    stmt = """Drop procedure N1304;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                  Test0099
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1304
#SPJ Parameters:	INOUT	:float/Real
#			OUT	:double/ Double PRECISION
#SPJ Actions: 		none
#Comments:
#Modification History: Test2214

def test0099(desc="test0090"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1304(inout inout1 real, out out1 double precision)
        external name 'Spjip.N1304'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 1.85657854E24;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1304(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2214""", "verify")

    stmt = """Drop procedure N1304;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#				   Test0100
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1284
#SPJ Parameters:	INOUT	:int/integer
#			OUT	:BigDecimal/numeric without Scale
#SPJ Actions: 		none
#Comments:
#Modification History: Test2311

def test0100(desc="test0100"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1284(inout inout1 integer, out out1 numeric)
        external name 'Spjip.N1284'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 12345678;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1284(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2311""", "verify")

    stmt = """Drop procedure N1284;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                Test0101
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1254
#SPJ Parameters:	INOUT	:long/largeint
#			OUT	:BigDecimal/numeric without scale.
#SPJ Actions: 		none
#Modification History: Test2285

def test0101(desc="test0101"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1254(inout inout1 largeint, out out1 numeric)
        external name 'Spjip.N1254'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 989431447;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1254(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2285""", "verify")

    stmt = """Drop procedure N1254;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                  Test0102
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1166
#SPJ Parameters:	IN	:Long/largeint
#			INOUT	:BigDecimal/numeric without scale
#			OUT	:BigDecimal/numeric without scale
#SPJ Actions: 		none
#Comments:
#Modification History: Test2300

def test0102(desc="test0102"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1166(in in1 largeint, inout inout1 numeric(9,0),
        out out1 numeric(9,0))
        external name 'Spjip.N1166'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 125847894;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 797428785.0;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1166(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2300""", "verify")

    stmt = """Drop procedure N1166;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0103
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for INPUT parameters.
#SPJ:			N0206
#SPJ Parameters:	IN1 Varchar / String
#                      IN1 Varchar / String
#SPJ Actions: 		none
#Comments:		CHAR or Varchar of  different character set than expected.
#Modification History: Test1742

def test0103(desc="test0103"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0206 (in in1 CHAR(25), inout inout1 varchar(25))
        external name 'Procs.N0206'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 'HOW IS MY DRIVING';"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y  'WHO CARES HERE';"""
    output = _dci.cmdexec(stmt)

    stmt = """call N0206(?x,?y);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1742""", "verify")

    stmt = """Drop procedure N0206;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                                  Test0104
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			N0200
#SPJ Parameters:	IN	:String / char
#			OUT	:String /char
#SPJ Actions: 		none
#Comments:		CHAR without length. Accepts a single byte.
#Modification History: Test2155

def test0104(desc="test0104"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0200 (in in1 varchar(50), out out1 varchar(50))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0200('A',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2155""", "verify")

    stmt = """Drop procedure N0200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


#***************************************************************************
#                              Test0105
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1306
#SPJ Parameters:	INOUT	:String/Varchar
#			OUT	:BigDecimal/decimal without Scale
#SPJ Actions: 		none
#Comments:
#Modification History: Test2215

def test0105(desc="test0105"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1306(inout inout1 varchar(25), out out1 numeric(13,4))
        external name 'Spjip.N1306'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x '185657854.5478';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1306(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2215""", "verify")

    stmt = """Drop procedure N1306;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0106
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1306
#SPJ Parameters:	INOUT	:String/Varchar
#			OUT	:BigDecimal/decimal with Scale
#SPJ Actions: 		none
#Comments:
#Modification History: Test2216

def test0106(desc="test0106"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1306(inout inout1 varchar(25), out out1 decimal(13,4))
        external name 'Spjip.N1306'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x '185657854.5214';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1306(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2216""", "verify")

    stmt = """Drop procedure N1306;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0107
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1311
#SPJ Parameters:	INOUT	:String/Varchar
#			OUT	:short/smallint
#SPJ Actions: 		none
#Comments:
#Modification History: Test2217

def test0107(desc="test0107"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1311(inout inout1 varchar(25), out out1 smallint)
        external name 'Spjip.N1311'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x '18565';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1311(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2217""", "verify")

    stmt = """Drop procedure N1311;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                              Test0108
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			1313
#SPJ Parameters:	INOUT	:String/Varchar
#			OUT	:int/integer
#SPJ Actions: 		none
#Comments:
#Modification History: Test2219

def test0108(desc="test0108"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N1313(inout inout1 varchar(25), out out1 integer)
        external name 'Spjip.N1313'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x '56578544';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N1313(?x,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2219""", "verify")

    stmt = """Drop procedure N1313;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0109
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for INPUT parameters.
#SPJ:			N0206
#SPJ Parameters:	IN1 Varchar / String
#                      INOUT1 CHAR / String
#SPJ Actions: 		none
#Comments:		Varchar of < length declared at CREATE received and CHAR expected.
#Modification History: Test2261

def test0109(desc="test0109"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0206 (in in1 CHAR(25), INOUT ONOUT1 varchar(15))
        external name 'Procs.N0206'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x 'INNOVATION';"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y 'TECHNOLOGY';"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0206(?x,?y);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2261""", "verify")

    stmt = """Drop procedure N0206;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0110
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION
#SPJ:			N0112
#SPJ Parameters:	Double IN1/ String OUT1
#SPJ Actions: 		none
#Comments:		Float was passed to Double.
#Modification History: Test2264

def test0110(desc="test0110"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0112 ( in in1 double precision, out out1 varchar(25))
        external name 'Procs.N0112'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0112(1.134674E32,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2264""", "verify")

    stmt = """Drop procedure N0112;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0111
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION
#SPJ:			N0107
#SPJ Parameters:	String IN1/ Time OUT1
#SPJ Actions: 		none
#Comments:		Timestamp value passed to the string.
#Modification History: Test1745

def test0111(desc="test0111"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0107 ( in in1 varchar(30),out out1 TIMESTAMP)
        external name 'Procs.N0107'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0107(time '12:10:10',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0107;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0112
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION
#SPJ:			N0108
#SPJ Parameters:	BigDecimal IN1/ String OUT1
#SPJ Actions: 		none
#Comments:		numeric value with scale passed to BigDecimal.
#Modification History: Test1746

def test0112(desc="test0112"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0108 ( in in1 numeric(18),out out1 varchar(45))
        external name 'Procs.N0108'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0108(123456789.123,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0108;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0113
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for INPUT parameters.
#SPJ:			N4208
#SPJ Parameters:	IN1 Timestamp/Timestamp
#SPJ Actions: 		none
#Comments:		Time for Timestamp
#Modification History: Test1813

def test0113(desc="test0113"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4208 (in in1 TIMESTAMP)
        external name 'Procs.N4208'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N4208(time '10:10:10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N4208;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0114
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for INPUT parameters.
#SPJ:			N4212
#SPJ Parameters:	IN Time/Time
#SPJ Actions: 		none
#Comments:		Time as IN parameter.
#CREATED		:Srinivas Nelluru  on 04/24/2001
#Modification History: Test1918

def test0114(desc="test0114"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4210 (in in1 TIME)
        external name 'Procs.N4210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N4210(Time '10:59:59.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1918""", "verify")

    stmt = """Drop procedure N4210;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0115
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for INPUT parameters.
#SPJ:			N4213
#SPJ Parameters:	IN1 Date / Date
#SPJ Actions: 		none
#Comments:		Date as IN parameter.
#CREATED		:Srinivas Nelluru  on 04/24/2001
#Modification History: Test1919

def test0115(desc="test0115"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4211 (in in1 DATE)
        external name 'Procs.N4211'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N4211(date '2001/10/10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1919""", "verify")

    stmt = """Drop procedure N4211;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0116
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for OUTPUT parameters.
#SPJ:			ProcN4008
#SPJ Parameters:	IN1 Time/Time
#                      OUT1 Timestamp/Timestamp
#SPJ Actions: 		none
#Comments:		Time for Timestamp
#Modification History: Test1615

def test0116(desc="test0116"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4008 (in in1 TIME, out out2 TIMESTAMP)
        external name 'Procs.N4008'
        library qa_spjcall
        parameter style java
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """**** ERROR[3183] Duplicate PARAMETER STYLE clauses were specified.*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0117
#***************************************************************************
#Purpose: 		DATATYPE CASTING and TRUNCATION for OUTPUT parameters.
#SPJ:			ProcN4008
#SPJ Parameters:	IN1 Time/Time
#                      OUT1 Timestamp/Timestamp
#SPJ Actions: 		none
#Comments:		Time for Timestamp
#Modification History: Test1615

def test0117(desc="test0117"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N4008 (in in1 TIME, out out2 TIMESTAMP)
        external name 'Procs.N4008'
        library qa_spjcall
        parameter style java
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """**** ERROR[3183] Duplicate PARAMETER STYLE clauses were specified.*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                  Test0118
#***************************************************************************
#Purpose: 		Data Casting and Truncation.
#SPJ:			N0602
#SPJ Parameters:	IN1	:String / Varchar
#			IN2	:int / integer
#			IN3	:BigDecimal / numeric
#			IN4 	:Date / Date
#			OUT1	:String / Varchar
#SPJ Actions: 		none
#Comments:
#Modification History: Test2157

def test0118(desc="test0118"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0602( in in1 CHAR(50),
        IN IN2 integer, IN IN3 numeric,
        IN IN4 real, IN IN5 DATE,
        out out1 varchar(150) )
        external name 'Procs.N0602'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?a 'AAA Computers';"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?b 464322;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?c 1214632;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?d 1.214E6;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?e '2002-12-31';"""
    output = _dci.cmdexec(stmt)

    stmt = """call N0602(?a,?b,?c,?d,?e,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t2157""", "verify")

    stmt = """Drop procedure N0602;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0119
#***************************************************************************
#Purpose: 		test NULL value input for integer
#SPJ:			N0302
#SPJ Parameters:	IN1 integer / integer
#                  	INOUT1 integer / integer
#	                OUT1 integer / integer
#SPJ Actions:
#Comments:
#Modification History: Test2000

def test0119(desc="test0119"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0302 (IN integer, inout inout1 integer, out out1 integer)
        external name 'Procs.N0302'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x null;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y null;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0302(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0302;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0120
#***************************************************************************
#Purpose: 		test NULL value input for float
#SPJ:			N0315
#SPJ Parameters:	IN1 Real / Float
#                  	INOUT1 Real / Float
#	                OUT1 Real / Float
#SPJ Actions:
#Comments:
#Modification History: Test2001

def test0120(desc="test0120"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0315(in in1 real, inout inout1 real, out out1 real)
        external name 'Procs.N0315'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x null;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y null;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0315(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0315 ;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0121
#***************************************************************************
#Purpose: 		test NULL value input for long
#SPJ:			N0304
#SPJ Parameters:	IN1 largeint / Long
#                  	INOUT1 largeint / Long
#	                OUT1 largeint / Long
#SPJ Actions:
#Comments:
#Modification History: Test2002

def test0121(desc="test0121"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0304 (in in1 largeint ,  inout inout1 largeint, out out1 largeint)
        external name 'Procs.N0304'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """set param ?x null;"""
    output = _dci.cmdexec(stmt)

    stmt = """set param ?y null;"""
    output = _dci.cmdexec(stmt)

    stmt = """Call N0304(?x,?y,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    stmt = """Drop procedure N0304;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0122
#***************************************************************************
#Purpose: 		SQL Host Environment to Java Stored Procedure.
#SPJ:			ProcN0200
#SPJ Parameters:	IN1 Varchar / String
#                      OUT1 Varchar / String
#SPJ Actions: 		none
#Comments:		Varchar of > declared length than expected received(Causes no trncation)
#Modification History: Test1506

def test0122(desc="test0122"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0200(in in1 varchar(18), out out1 varchar(25))
        external name 'Procs.N0200'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0200('NON-STOP DIVISION',?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1506""", "verify")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0200;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0123
#**********************************************************************
#Purpose: 		SQL Host Environment to Java Stored Procedure.
#SPJ:			N0202
#SPJ Parameters:	IN1 numeric / BigDecimal;
#			OUT1 numeric / BigDecimal;
#SPJ Actions: 		none
#Comments:
#Modification History: Test1507

def test0123(desc="test0123"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0202 (in in1 numeric, out out1 numeric)
        external name 'Procs.N0202'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Call N0202(123456789.0,?);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t1507""", "verify")
    _dci.expect_any_substr(output, """*--- SQL operation complete.*""")

    stmt = """Drop procedure N0202;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

#**********************************************************************
#           INVALID  DATATYPES  AND  DATATYPE  MODIFIERS
#**********************************************************************
#                            Test0124
#**********************************************************************
#Purpose: 		Test Invalid datatypes and datatype modifiers.
#SPJ:			N0210
#SPJ Parameters:	IN1 intERVAL / int
#                      OUT1 integer / int
#SPJ Actions: 		none
#Comments:		intERVAL IN
#Modification History: Test1532

def test0124(desc="test0124"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0210 (in in1 intERVAL, out out1 integer)
        external name 'Procs.N0210'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                               Test0125
#***************************************************************************
#Purpose: 		Test Invalid datatypes and datatype modifiers.
#SPJ:			N0204A
#SPJ Parameters:	IN1 PIC_X / short
#                      OUT1 Real / float
#SPJ Actions: 		none
#Comments:		PIC_X IN
#Modification History: Test1533

def test0125(desc="test0125"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0204 (in in1 PIC_X, out out1 real)
        external name 'Procs.N0204'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                 Test0126
#***************************************************************************
#Purpose: 		Test Invalid datatypes and datatype modifiers.
#SPJ:			N0212
#SPJ Parameters:	IN1 CHARVAR / String
#                      OUT1 Real / String
#SPJ Actions: 		none
#Comments:		CHARVAR IN
#Modification History: Test1535

def test0126(desc="test0126"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0212 (in in1 CHARVAR, out out1 real)
        external name 'Procs.N0212'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0127
#***************************************************************************
#Purpose: 		Test Invalid datatypes and datatype modifiers.
#SPJ:			N0316
#SPJ Parameters:	IN Float / double
#                      INOUT1 PIC_X / double
#                      OUT1 Float/Double
#SPJ Actions: 		none
#Comments:		PIC_X INOUT.
#Modification History: Test1543

def test0127(desc="test0127"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0316(in in1 double precision, inout inout1 PIC_X, out out1 double precision)
        external name 'Procs.N0316'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0128
#***************************************************************************
#Purpose: 		Test Invalid datatypes and datatype modifiers.
#SPJ:			N0300
#SPJ Parameters:	IN1 integer / String
#                      INOUT1 CHARVAR/String
#                      OUT1 integer/String
#SPJ Actions: 		none
#Comments:             CHARVAR INOUT
#Modification History: Test1545

def test0128(desc="test0128"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0300 (in in1 CHAR(30),inout inout1 CHARVAR(30), out out1 varchar(45))
        external name 'Procs.N0300'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """*ERROR*""")

    _testmgr.testcase_end(desc)

#***************************************************************************
#                                Test0129
#***************************************************************************
#Purpose: 		Test Invalid datatypes and datatype modifiers.
#SPJ:			N0311
#SPJ Parameters:	IN1 numeric(8,2) / BigDecimal
#      	        INOUT2 numeric(8,2) /BigDecimal
#      	        OUT3 numeric(8,2)) /BigDecimal
#SPJ Actions: 		none
#Comments:		numeric INOUT	**unsigned SPECIFIED**
#Modification History: Test1563

def test0129(desc="test0129"):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """Create procedure N0311 (in in1 numeric,inout inout2 numeric unsigned,out out3 numeric)
        external name 'Procs.N0311'
        library qa_spjcall
        language java
        parameter style java;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, "3208")

    _testmgr.testcase_end(desc)


