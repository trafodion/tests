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
    
def test001(desc="""alt func: scalar func name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    # Alter a non-existing function is an error.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
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
  
    # TRAF: alter function on UDF is not supported at all. 
    stmt = """alter function """ + defs.my_schema + """.foo
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
   
    # alter function in a non-existing catalog or schema is an error.
    stmt = """alter function DOESNTEXIST.DOESNTEXIST.FOO
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4222')
   
    # TRAF: alter function on UDF is not supported at all. 
    stmt = """alter function DOESNTEXIST.FOO
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # Missing name is an error
    stmt = """alter function
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Four-part name is an error
    stmt = """alter function A.B.C.FOO
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3011')
    
    # '$' is not allowed in the name
    stmt = """alter function \$FOO
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Numbers are not allowed in the name
    stmt = """alter function 1234FOO
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""alt func: <func characteristics> (syntax)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # The DDL ES is extremely vague about which characteristic can
    # be altered, so we can only do our best and try them one by one.
    
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
pass through inputs (value 'MMMM' text,
value 'NNNN' text)
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
    
    # <function external name>
    
    # A non-string name is an eror
    stmt = """alter function FOO
external name foo1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
   
    # This should work
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
external name 'foo1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # <function language clause>
    
    # language can not be altered
    stmt = """alter function FOO
language c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # <scalar function parameter style clause>
    
    # parameter style can not be altered
    stmt = """alter function FOO
parameter style sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # <deterministic characteristic>
    
    # Only '[not] deterministic' is supported
    stmt = """alter function FOO
no deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # '[not] deterministic' is supported, so this should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
not deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # '[not] deterministic' is supported, so this should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
deterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # <SQL-data access indication>
    
    # Only 'no sql' is supported in this release.
    
    # SQL-data access indicatin cannot be altered.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # <final call characteristic>
    
    # The design is to support both 'no final call' and 'final call'.  But in
    # this release, 'no final call' is not supported yet.  An error is returned
    # if you specify it.  The ES says so.
    
    # SQL-data access indication cannot be altered.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
final call;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # <special attributes clause>
    
    # attribute should be a string
    stmt = """alter function FOO
attribute abcd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # attribute <string> should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
attribute 'abcd';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # attributes <string> should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
attributes 'abcd';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # attribute (<string>) should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
attribute ('abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # attributes (<string>) should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
attributes ('abcd');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # An empty string should work
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
attribute '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # <state area size>
    
    # No state area is supported
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
no state area;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1010') 
    
    # Only size 0-16000 is supported.  This should fail.
    stmt = """alter function FOO
state area size -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Only size 0-16000 is supported.  This should fail
    stmt = """alter function FOO
state area size 16001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # size is 0-16000.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
state area size 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # size is 0-16000.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
state area size 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # Size is 0-16000.  This should work.
    # TRAF: alter function on UDF is not supported at all. 
    stmt = """alter function FOO
state area size 16000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    # <parallelism characteristic>
    
    # Only [no parallelism|allow any parallelism] is supported. This should fail.
    stmt = """alter function FOO
not parallelism;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # No parallelism is supported.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
no parallelism;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1010')
    
    # Allow any parallelism is supported.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
allow any parallelism;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1010')
    
    # <execution mode>
    
    # Only '[fast|safe] execution mode' is supported.  This should fail.
    stmt = """alter function FOO
slow execution mode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # 'fast execution mode' is supported.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
fast execution mode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1010')
    
    # 'safe execution mode' is supported.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
safe execution mode;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '1010')
    
    # <function optimization hint>
    
    # <version tag>
    # version tag expects a string.  This should fail.
    stmt = """alter function FOO
version tag abcd;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # version tag expects a string.  This should work.
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function FOO
version tag 'abcd';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""alt func: <func characteristics> (runtime)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Set up a UDF that has bogus external name
    stmt = """create function MY_INT_ALT_FUNC_I
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
    
    # Alter it to use real qa_udf_integer, and change a few characteristics
    # TRAF: alter function on UDF is not supported at all.
    stmt = """alter function MY_INT_ALT_FUNC_I
external name 'qa_func_int32'
-- TRAF external path ?dll_name
library qa_udf_lib
not deterministic
state area size 2048
no parallelism;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1010')
   
    # TRAF: alter function on UDF is not supported at all.
    # Make sure that the characterstics are altered
    # stmt = """showddl function MY_INT_ALT_FUNC_I;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_any_substr(output, """NOT DETERMINISTIC""")
    # stmt = """showddl function MY_INT_ALT_FUNC_I;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_any_substr(output, """STATE AREA SIZE 2048""")
    # stmt = """showddl function MY_INT_ALT_FUNC_I;"""
    # output = _dci.cmdexec(stmt)
    # dci.expect_any_substr(output, """NO PARALLELISM""")
    
    # Run it to make sure that the external name are altered
    # stmt = """values (MY_INT_ALT_FUNC_I(1));"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_selected_msg(output)
    
    stmt = """drop function MY_INT_ALT_FUNC_I cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

