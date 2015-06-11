# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc="""drop func"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    # Generic syntax check
    stmt = """
create function FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function """ + defs.my_schema + """.foo cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function """ + defs.my_schema + """.FoO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Drop function in a non-existing catalog or schema is an error.
    stmt = """drop function DOESNTEXIST.DOESNTEXIST.FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1002')
    
    stmt = """drop function DOESNTEXIST.FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # Missing name is an error
    stmt = """drop function;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Four-part name is an error
    stmt = """drop function A.B.C.FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3011')
    
    # '$' is not allowed in the name
    stmt = """drop function \$FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Numbers are not allowed in the name
    stmt = """drop function 1234FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
   
    # Drop a UDF with restrict vs cascade 
    stmt = """create function MY_UDF_INT_MISC_I1
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view mytestview as select MY_UDF_INT_MISC_I1(a) as a from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    stmt = """select * from mytestview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)
  
    # restrict should fail, there is a view that references it.
    stmt = """drop function MY_UDF_INT_MISC_I1 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1047')
    
    # The cascade feature is not supported yet, so we have to drop the view
    # first and then the UDF again.
    # drop function FOO cascade;
    
    stmt = """drop view mytestview;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function MY_UDF_INT_MISC_I1 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""drop schema with UDF defined"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    stmt = """create schema """ + defs.my_schema_temp + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """set schema """ + defs.my_schema_temp + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create a UDF in this schema
    stmt = """create function QA_UDF_SCHEMA ()
returns (OUTVAL char(64))
language c
parameter style sql
external name 'qa_func_schema_1'
-- TRAF external path ?dll_name
library """ + defs.my_schema + """.qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select [first 1] qa_udf_schema() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 1""")
    
    # This should fail, as we still have a UDF defined in this schema.
    stmt = """drop schema """ + defs.my_schema_temp + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1028')
    
    # This should work, cascade will drop everything.
    stmt = """drop schema """ + defs.my_schema_temp + """ cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # reset to the default schema
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    _testmgr.testcase_end(desc)

def test003(desc="""showddl func"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    stmt = """create function MY_UDF_INT_MISC_I2
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """select MY_UDF_INT_MISC_I2(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)
 
    stmt = """showddl function MY_UDF_INT_MISC_I2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """CREATE FUNCTION""")
    
    stmt = """drop function MY_UDF_INT_MISC_I2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""showddl func..action.."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    stmt = """create function MY_UDF_INT_MISC_I3
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select MY_UDF_INT_MISC_I3(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)
    
    # It's an error, as FOO is a UDF, not a UUDF
    stmt = """showddl function MY_UDF_INT_MISC_I3 action MYACTION;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """drop function MY_UDF_INT_MISC_I3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""get funcions"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    stmt = """create function MY_UDF_INT_MISC_I4
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
-- TRAF external path 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """select MY_UDF_INT_MISC_I4(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)
 
    stmt = """get functions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """MY_UDF_INT_MISC_I4""")
    
    stmt = """drop function MY_UDF_INT_MISC_I4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""register UDF in different schemas"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Register 3 UDFs in 3 different schemas.  They all have the same name,
    # but will point to different DLL entries so taht we can make sure that the
    # right one is called in the tset.
    #
    stmt = """create function """ + defs.my_schema0 + """.QA_UDF_SCHEMA ()
returns (OUTVAL char(64))
language c
parameter style sql
external name 'qa_func_schema_0'
-- TRAF external path ?dll_name
library """ + defs.my_schema + """.qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function """ + defs.my_schema1 + """.QA_UDF_SCHEMA ()
returns (OUTVAL char(64))
language c
parameter style sql
external name 'qa_func_schema_1'
-- TRAF external path ?dll_name
library """ + defs.my_schema + """.qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function """ + defs.my_schema2 + """.QA_UDF_SCHEMA ()
returns (OUTVAL char(64))
language c
parameter style sql
external name 'qa_func_schema_2'
-- TRAF external path ?dll_name
library """ + defs.my_schema + """.qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should fail, no UDF is defined in the default schema defs.my_schema
    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + ".mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, """4450""")

    # Reference UDF with catalog + schema
    stmt = """select [first 1] """ + defs.my_schema0 + """.QA_UDF_SCHEMA() from """ + defs.my_schema + ".mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 0""")

    # Reference UDF with catalog + schema
    stmt = """select [first 1] """ + defs.my_schema1 + """.QA_UDF_SCHEMA() from """ + defs.my_schema + ".mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 1""")

    # Reference UDF with schema
    stmt = """select [first 1] """ + defs.my_schema1_no_cat + """.QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 1""")

    # Reference UDF with catalog + schema
    stmt = """select [first 1] """ + defs.my_schema2 + """.QA_UDF_SCHEMA() from """ + defs.my_schema + ".mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 2""")

    # set schema, then reference UDF with no catalog or schema
    stmt = """set schema """ + defs.my_schema0 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 0""")

    stmt = """set schema """ + defs.my_schema1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 1""")

    stmt = """set schema """ + defs.my_schema2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Reference UDF with catalog + schema
    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 2""")

    # Drop the function using the unqualified name, it should drop the one in
    # defs.my_schema0
    stmt = """set schema """ + defs.my_schema0 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop function QA_UDF_SCHEMA cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should fail, it has been droped.
    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, """4450""")

    # Make sure that the other 2 are still there.
    stmt = """set schema """ + defs.my_schema1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 1""")

    stmt = """set schema """ + defs.my_schema2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """SCHEMA 2""")

    # Go back to defs.my_schema0 and drop the one registered in
    # defs.my_schema1 from there.
    stmt = """set schema """ + defs.my_schema0 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # Drop the function using the qualified name, it should drop the one in
    # defs.my_schema1
    stmt = """drop function """ + defs.my_schema1 + """.QA_UDF_SCHEMA cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema """ + defs.my_schema1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should fail, the UDF no longer exists.
    stmt = """select [first 1] QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, """4450""")

    stmt = """drop function """ + defs.my_schema2 + """.QA_UDF_SCHEMA cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # should fail, the UDF no longer exists.
    stmt = """select [first 1] """ + defs.my_schema2 + """.QA_UDF_SCHEMA() from """ + defs.my_schema + """.mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, """4450""")

    # reset back to the default schema
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

