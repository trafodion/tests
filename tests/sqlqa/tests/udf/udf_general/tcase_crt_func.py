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
    
def test001(desc="""crt func: scalar func name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Run them in our own private schema, not the global schema.
    
    # Register a UDF twice with the same name is an error. The name
    # should be case-insensitive.  Unqalified or partially qualified
    # name should use the current catalog and schema as the default.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # function already exists 
    stmt = """create function """ + defs.my_schema + """.foo
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1390')
   
    # function already exists 
    stmt = """create function """ + defs.my_schema + """.FoO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1390')
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Create function in a schema other than 'TRAFODION' is an error
    stmt = """create function DOESNTEXIST.DOESNTEXIST.FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
   
    # Missing name is an error
    stmt = """create function
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Four-part name is an error
    stmt = """create function A.B.C.FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3011')
    
    # '$' is not allowed in the name
    stmt = """create function \$FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Numbers are not allowed in the name
    stmt = """create function 1234FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Name can be as short as one character, but can't exceed the maximum allowed
    # length for a standard SQL identifier.
    stmt = """create function F
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function F;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create function FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    
    _testmgr.testcase_end(desc)

def test002(desc="""crt func: param list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Generic syntax check
    # Missing input parameter list is an error
    stmt = """create function FOO
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up   
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
 
    # Missing '(' is an error
    stmt = """create function FOO
INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
   
    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
 
    # Missing ')' is an error
    stmt = """create function FOO
(INVAL int
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Missing both '(' and ')' is an error
    stmt = """create function FOO
INVAL int
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # The optional 'IN' keyword should be OK.
    stmt = """create function FOO
(IN INVAL1 int, in INVAL2 int, INVAL3 int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Other than the 'IN' keyword, anything else should be an error.
    stmt = """create function FOO
(OUT INVAL1 int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Wrong separator is an error
    stmt = """create function FOO
(INVAL1 int; INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Input parameter data types
    
    # Missing data type is an error
    stmt = """create function FOO
(INVAL)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Invalid datatype is an eror
    stmt = """create function FOO
(INVAL INVAL)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Input parameter names
    
    # Missing parameter name is supposed to be an error, but it is not enforced.
    stmt = """create function MYUDF
(int)
returns (OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt = """select MYUDF(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # clean up
    stmt = """drop function MYUDF;"""
    output = _dci.cmdexec(stmt)
    
    # Invalid parameter name is an error
    stmt = """create function FOO
(int int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Parameter name length exceed SQL identifier length is an error.
    stmt = """create function FOO
(FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Duplicate input parameter names is an error, but this is not enforced
    # at the registration time.  It returns an error at the run time.
    # LP#1441784
    stmt = """create function MYUDF
(INVAL int, INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12345')

    stmt = """select MYUDF(a, b) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function MYUDF;"""
    output = _dci.cmdexec(stmt)
    
    # The same name for input parameter and output parameter is an error, but
    # this is not enforced at the registration time.  It returns an error at
    # the run time.
    # LP#1441784
    stmt = """create function MYUDF
(INVAL int)
returns (INVAL int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12345')

    stmt = """select MYUDF(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function MYUDF;"""
    output = _dci.cmdexec(stmt)
    
    # Number of input parameters
    
    # It's OK to have no input parameter at all.
    stmt = """create function FOO
()
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # UDF only supports a maximum of 32 parameters (31 inputs + 1 output),
    # but alas, this is now is treated as a runtime error.  Create function
    # does not check it at all.
    
    # Should work, 32 parameters (31 inputs + 1 output)
    stmt = """create function QA_UDF_32_PARAMETERS
(I1 int, I2 int, I3 int, I4 int, I5 int, I6 int, I7 int, I8 int, I9 int,
I10 int, I11 int, I12 int, I13 int, I14 int, I15 int, I16 int, I17 int,
I18 int, I19 int, I20 int, I21 int, I22 int, I23 int, I24 int, I25 int,
I26 int, I27 int, I28 int, I29 int, I30 int, I31 int)
returns (O int)
language c
parameter style sql
external name 'qa_func_32_parameters'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 32 parameters (31 inputs + 1 output) are the maximum supported by a UDF.
    # This should work.  The function sums up all of the input and returns it
    # as the output, so we should see 31 here.
    stmt = """values(QA_UDF_32_PARAMETERS(1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,
1));"""
    output = _dci.cmdexec(stmt)
    # expect 31 '1's.
    _dci.expect_any_substr(output, """31""")
    
    stmt = """drop function QA_UDF_32_PARAMETERS cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Should fail, 33 parameters (32 inputs + 1 output), but it is a runtime
    # error, not a registration error now.
    stmt = """create function QA_UDF_33_PARAMETERS
(I1 int, I2 int, I3 int, I4 int, I5 int, I6 int, I7 int, I8 int, I9 int,
I10 int, I11 int, I12 int, I13 int, I14 int, I15 int, I16 int, I17 int,
I18 int, I19 int, I20 int, I21 int, I22 int, I23 int, I24 int, I25 int,
I26 int, I27 int, I28 int, I29 int, I30 int, I31 int, I32 int)
returns (O int)
language c
parameter style sql
external name 'qa_func_33_parameters'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1550')
    
    # This should fail, function does not exist.
    stmt = """values(QA_UDF_33_PARAMETERS(1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,
1,1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
   
    # This should fail, function does not exist. 
    stmt = """drop function QA_UDF_33_PARAMETERS cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""crt func: return clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Generic syntax check

    # Missing return parameter is an error, but it is not enforced at the
    # registration time.  Error is returned at the run time.
    # LP#1441784
    stmt = """create function MYUDF
(INTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12345')

    stmt = """select MYUDF(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function MYUDF;"""
    output = _dci.cmdexec(stmt)

    # Use the keyword 'returns' should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Use the keyword 'return' should also work.
    stmt = """create function FOO
(INVAL int)
return (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Without the keyword 'returns' or 'return' is an error.
    stmt = """create function FOO
(INVAL int)
(OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
   
    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
 
    # Without '()' for one return parameter is OK.
    stmt = """create function FOO
(INVAL int)
returns OUTVAL int
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Without '()' for more than one return parameters is an error.
    stmt = """create function FOO
(INVAL int)
returns OUTVAL1 int, OUTVAL2 int
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Using '()' for one return parameter should work
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Using '() for more than one return parameters should work
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL1 int, OUTVAL2 int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Missing '(' is an error
    stmt = """create function FOO
(INVAL int)
returns OUTVAL1 int, OUTVAL2 int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Missing ')' is an error
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL1 int, OUTVAL2 int
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # The optional 'OUT' keyword should be OK.
    stmt = """create function FOO
(INVAL int)
returns (OUT OUTVAL1 int, out OUTVAL2 int, OUTVAL3 int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Other than the 'OUT' keyword, anything else should be an error.
    stmt = """create function FOO
(INVAL int)
returns (IN OUTVAL int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Wrong separator is an error
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL1 int; OUTVAL2 int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Return parameter data types
    
    # Missing data type is an error
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Invalid datatype is an eror
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL OUTVAL)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Return parameter names
   
    # Missing return parameter name is supposed to be an error, but it is not 
    # enforced.
    stmt = """create function MYUDF
(INTVAL int)
returns (int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """select MYUDF(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)

    # clean up
    stmt = """drop function MYUDF;"""
    output = _dci.cmdexec(stmt)

    # Invalid parameter name is an error
    stmt = """create function FOO
(INVAL int)
returns (int int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Parameter name length exceed SQL identifier length is an error.
    stmt = """create function FOO
(INVAL int)
returns (FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF int)
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    
    # Duplicate output parameter names is an error, but this is not enforced 
    # right now.
    # LP#1441784
    # BUG comment it out for now.  This function returns only 1 value as 
    # if the 2nd OUTVAL does not exist.  It also seems to cause the drop
    # function to hang.
    stmt = """create function MYUDF
(INVAL int)
returns (OUTVAL int, OUTVAL int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    # BUG output = _dci.cmdexec(stmt)
    # BUG _dci.expect_error_msg(output, '12345')

    # BUG stmt = """select MYUDF(a) from mytable;"""
    # BUG output = _dci.cmdexec(stmt)
    # BUG _dci.expect_error_msg(output)

    # clean up
    # BUG stmt = """drop function MYUDF"""
    # BUG output = _dci.cmdexec(stmt)
   
    # The same name for input parameter and output parameter should be an 
    # error, but this is not enforced right now.
    # LP#1441784
    stmt = """create function MYUDF 
(INVAL int)
returns (INVAL int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '12345')

    stmt = """select MYUDF(a) from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function MYUDF;"""
    output = _dci.cmdexec(stmt)
    
    # Number of return parameters
    
    # UDF needs at least one return parameter.  No return parameter is an error.
    stmt = """create function FOO
(INVAL int)
returns ()
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # UDF needs at least one return parameter.  No return parameter is an error.
    stmt = """create function FOO
(INVAL int)
returns
language c
parameter style sql
external name 'foo'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # The number of inputs + outputs can't exceed 32 for a UDF is tested
    # in A02 already.
    
    _testmgr.testcase_end(desc)

def test004(desc="""crt func: func characteristics"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Required characteristics
    
    # It's an error without the required <function external name>
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3205')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Other than <function external name>, all the rest are optional.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Duplicate characteristics
    
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
language c
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3183')
   
    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
 
    # <function external name>
    
    # A non-string name is an eror
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
external name foo
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # <function language clause>
    
    # C is the only language supported
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language java 
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # C is the only language supported
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c++
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # C is the only language supported, so this one should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
language c
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <scalar function parameter style clause>
    # Only SQL parameter style is supported.  Notice that 'abcd' and 'sqlrow'
    # will get different error.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
parameter style abcd
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Only SQL parameter style is supported.  Notice that 'abcd' and 'sqlrow'
    # will get different error.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
parameter style sqlrow
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # SQL parameter style is supported, so this should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
parameter style sql
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <deterministic characteristic>
    
    # Only '[not] deterministic' is supported
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
no deterministic
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # '[not] deterministic' is supported, so this should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
not deterministic
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # '[not] deterministic' is supported, so this should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
deterministic
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <SQL-data access indication>
    
    # Only 'no sql' is supported in this release.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
contains sql
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Only 'no sql' is supported in this release.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
reads sql data
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Only 'no sql' is supported in this release.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
modifies sql data
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # 'no sql' is supported.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
no sql
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <final call characteristic>
    
    # Only '[no] final call' is supported.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
not final call
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # The design is to support both 'no final call' and 'final call'.  But in
    # this release, 'no final call' is not supported yet.  An error is returned
    # if you specify it.  The ES says so.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
no final call
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # 'final call' is supported, so this should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
final call
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <special attributes clause>
    
    # attribute should be a string
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
attribute abcd
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # attribute <string> should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
attribute 'abcd'
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # attributes <string> should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
attributes 'abcd'
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # attribute (<string>) should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
attribute ('abcd')
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # attributes (<string>) should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
attributes ('abcd')
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # An empty string should work
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
attribute ''
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <state area size>
    
    # No state area is supported
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
no state area
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Only size 0-16000 is supported.  This should fail.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
state area size -1
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # Only size 0-16000 is supported.  This should fail
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
state area size 16001
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # size is 0-16000.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
state area size 0
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # size is 0-16000.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
state area size 1000
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Size is 0-16000.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
state area size 16000
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <parallelism characteristic>
    
    # Only [no parallelism|allow any parallelism] is supported. This should fail.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
not parallelism
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # No parallelism is supported.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
no parallelism
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # Allow any parallelism is supported.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
allow any parallelism
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <execution mode>
    
    # Only '[fast|safe] execution mode' is supported.  This should fail.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
slow execution mode
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # 'fast execution mode' is supported.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
fast execution mode
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # 'safe execution mode' is supported.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
safe execution mode
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <function optimization hint>
    
    # The function characteristic <function optimization hint> is not supported
    # yet.  The ES syntax does not work.  Write tests once it is supported.
    
    # <version tag>
    # version tag expects a string.  This should fail.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
version tag abcd
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # version tag expects a string.  This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
version tag 'abcd'
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # <location clause>
    
    # The ES simply says that <location clause> is similar to
    # 'create procedure' but it does not say more than that.  Write some
    # tests once it is supported.
    
    # -- library expects a string without quotes, this should fail
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
library 'abcd'
external name 'foo'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    # clean up
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    
    # This should work.
    stmt = """create function FOO
(INVAL int)
returns (OUTVAL int)
external name 'foo'
library qa_udf_lib
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop function FOO;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

