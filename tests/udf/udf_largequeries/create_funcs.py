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

def test001(desc="""create library"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create library qa_udf_lib file """ + defs.qa_udf_lib + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test002(desc="""register UDFs"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create function qa_udf_char
(INVAL char(50))
returns (c_char char(50))
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_upshift
(INVAL char(50) upshift)
returns (c_char_upshift char(50) upshift)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_upshift;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_not_casespecific
(INVAL char(50) not casespecific)
returns (c_char_not_casespecific char(50) not casespecific)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_not_casespecific;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_varying
(INVAL char varying(50))
returns (c_char_varying char varying(50))
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_varying;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_varying_upshift
(INVAL char varying(50) upshift)
returns (c_char_varying_upshift char varying(50) upshift)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_varying_upshift;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_varying_not_casespecific
(INVAL char varying(50) not casespecific)
returns (c_char_varying_not_casespecific char varying(50) not casespecific)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_varying_not_casespecific;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_varchar
(INVAL varchar(50))
returns (c_varchar varchar(50))
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_varchar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_varchar_upshift
(INVAL varchar(50) upshift)
returns (c_varchar_upshift varchar(50) upshift)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_varchar_upshift;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_varchar_not_casespecific
(INVAL varchar(50) not casespecific)
returns (c_varchar_not_casespecific varchar(50) not casespecific)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_varchar_not_casespecific;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar
(INVAL nchar(50))
returns (c_nchar nchar(50))
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_upshift
(INVAL nchar(50) upshift)
returns (c_nchar_upshift nchar(50) upshift)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_upshift;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_not_casespecific
(INVAL nchar(50) not casespecific)
returns (c_nchar_not_casespecific nchar(50) not casespecific)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_not_casespecific;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_varying
(INVAL nchar varying(50))
returns (c_nchar_varying nchar varying(50))
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_varying;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_varying_upshift
(INVAL nchar varying(50) upshift)
returns (c_nchar_varying_upshift nchar varying(50) upshift)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_varying_upshift;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_varying_not_casespecific
(INVAL nchar varying(50) not casespecific)
returns (c_nchar_varying_not_casespecific nchar varying(50) not casespecific)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_varying_not_casespecific;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_numeric
(INVAL numeric(9,2))
returns (c_numeric numeric(9,2))
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_numeric;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_numeric_unsigned
(INVAL numeric(9,2) unsigned)
returns (c_numeric_unsigned numeric(9,2) unsigned)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_numeric_unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_decimal
(INVAL decimal(9,2))
returns (c_decimal decimal(9,2))
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_decimal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_decimal_unsigned
(INVAL decimal(9,2) unsigned)
returns (c_decimal_unsigned decimal(9,2) unsigned)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_decimal_unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_integer
(INVAL integer)
returns (c_integer integer)
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

    stmt = """showddl function qa_udf_integer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_integer_unsigned
(INVAL integer unsigned)
returns (c_integer_unsigned integer unsigned)
language c
parameter style sql
external name 'qa_func_uint32'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_integer_unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_largeint
(INVAL largeint)
returns (c_largeint largeint)
language c
parameter style sql
external name 'qa_func_int64'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_largeint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_smallint
(INVAL smallint)
returns (c_smallint smallint)
language c
parameter style sql
external name 'qa_func_int16'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_smallint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_smallint_unsigned
(INVAL smallint unsigned)
returns (c_smallint_unsigned smallint unsigned)
language c
parameter style sql
external name 'qa_func_uint16'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_smallint_unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_float
(INVAL float(10))
returns (c_float float(10))
language c
parameter style sql
external name 'qa_func_double'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_float;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_real
(INVAL real)
returns (c_real real)
language c
parameter style sql
external name 'qa_func_real'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_real;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_double_precision
(INVAL double precision)
returns (c_double_precision double precision)
language c
parameter style sql
external name 'qa_func_double'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_double_precision;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_date
(INVAL date)
returns (c_date date)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_time
(INVAL time)
returns (c_time time)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_time5
(INVAL time(5))
returns (c_time5 time(5))
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_time5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_timestamp
(INVAL timestamp)
returns (c_timestamp timestamp)
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_timestamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_timestamp5
(INVAL timestamp(5))
returns (c_timestamp5 timestamp(5))
language c
parameter style sql
external name 'qa_func_char'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_timestamp5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_clob
(INVAL clob)
returns (c_clob clob)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_clob;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_blob
(INVAL blob)
returns (c_blob blob)
language c
parameter style sql
external name 'qa_func_vcstruct'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_blob;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_integer_nondeterministic
(INVAL int)
returns (c_integer_nondeterministic int)
language c
parameter style sql
external name 'qa_func_int32'
library qa_udf_lib
not deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_integer_nondeterministic;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'NOT DETERMINISTIC');

    # ------------------------ MVF -------------------------

    stmt = """create function qa_udf_char_mvf
(INVAL char(50))
returns (c_char1 char(50), c_char2 char(50))
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_upshift_mvf
(INVAL char(50) upshift)
returns (c_char_upshift1 char(50) upshift, c_char_upshift2 char(50) upshift)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_upshift_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_not_casespecific_mvf
(INVAL char(50) not casespecific)
returns (c_char_not_casespecific1 char(50) not casespecific, c_char_not_casespecific2 char(50) not casespecific)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_not_casespecific_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_varying_mvf
(INVAL char varying(50))
returns (c_char_varying1 char varying(50), c_char_varying2 char varying(50))
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_varying_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_varying_upshift_mvf
(INVAL char varying(50) upshift)
returns (c_char_varying_upshift1 char varying(50) upshift, c_char_varying_upshift2 char varying(50) upshift)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_varying_upshift_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_char_varying_not_casespecific_mvf
(INVAL char varying(50) not casespecific)
returns (c_char_varying_not_casespecific1 char varying(50) not casespecific, c_char_varying_not_casespecific2 char varying(50) not casespecific)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_char_varying_not_casespecific_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_varchar_mvf
(INVAL varchar(50))
returns (c_varchar1 varchar(50), c_varchar2 varchar(50))
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_varchar_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_varchar_upshift_mvf
(INVAL varchar(50) upshift)
returns (c_varchar_upshift1 varchar(50) upshift, c_varchar_upshift2 varchar(50) upshift)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_varchar_upshift_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_varchar_not_casespecific_mvf
(INVAL varchar(50) not casespecific)
returns (c_varchar_not_casespecific1 varchar(50) not casespecific, c_varchar_not_casespecific2 varchar(50) not casespecific)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_varchar_not_casespecific_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_mvf
(INVAL nchar(50))
returns (c_nchar1 nchar(50), c_nchar2 nchar(50))
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_upshift_mvf
(INVAL nchar(50) upshift)
returns (c_nchar_upshift1 nchar(50) upshift, c_nchar_upshift2 nchar(50) upshift)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_upshift_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_not_casespecific_mvf
(INVAL nchar(50) not casespecific)
returns (c_nchar_not_casespecific1 nchar(50) not casespecific, c_nchar_not_casespecific2 nchar(50) not casespecific)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_not_casespecific_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_varying_mvf
(INVAL nchar varying(50))
returns (c_nchar_varying1 nchar varying(50), c_nchar_varying2 nchar varying(50))
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_varying_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_varying_upshift_mvf
(INVAL nchar varying(50) upshift)
returns (c_nchar_varying_upshift1 nchar varying(50) upshift, c_nchar_varying_upshift2 nchar varying(50) upshift)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_varying_upshift_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_nchar_varying_not_casespecific_mvf
(INVAL nchar varying(50) not casespecific)
returns (c_nchar_varying_not_casespecific1 nchar varying(50) not casespecific, c_nchar_varying_not_casespecific2 nchar varying(50))
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_nchar_varying_not_casespecific_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_numeric_mvf
(INVAL numeric(9,2))
returns (c_numeric1 numeric(9,2), c_numeric2 numeric(9,2))
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_numeric_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_numeric_unsigned_mvf
(INVAL numeric(9,2) unsigned)
returns (c_numeric_unsigned1 numeric(9,2) unsigned, c_numeric_unsigned2 numeric(9,2) unsigned)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_numeric_unsigned_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_decimal_mvf
(INVAL decimal(9,2))
returns (c_decimal1 decimal(9,2), c_decimal2 decimal(9,2))
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_decimal_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_decimal_unsigned_mvf
(INVAL decimal(9,2) unsigned)
returns (c_decimal_unsigned1 decimal(9,2) unsigned, c_decimal_unsigned2 decimal(9,2) unsigned)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_decimal_unsigned_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_integer_mvf
(INVAL integer)
returns (c_integer1 integer, c_integer2 integer)
language c
parameter style sql
external name 'qa_func_int32_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_integer_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_integer_unsigned_mvf
(INVAL integer unsigned)
returns (c_integer_unsigned1 integer unsigned, c_integer_unsigned2 integer unsigned)
language c
parameter style sql
external name 'qa_func_uint32_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_integer_unsigned_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_largeint_mvf
(INVAL largeint)
returns (c_largeint1 largeint, c_largeint2 largeint)
language c
parameter style sql
external name 'qa_func_int64_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_largeint_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_smallint_mvf
(INVAL smallint)
returns (c_smallint1 smallint, c_smallint2 smallint)
language c
parameter style sql
external name 'qa_func_int16_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_smallint_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_smallint_unsigned_mvf
(INVAL smallint unsigned)
returns (c_smallint_unsigned1 smallint unsigned, c_smallint_unsigned2 smallint unsigned)
language c
parameter style sql
external name 'qa_func_uint16_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_smallint_unsigned_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_float_mvf
(INVAL float(10))
returns (c_float1 float(10), c_float2 float(10))
language c
parameter style sql
external name 'qa_func_double_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_float_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_real_mvf
(INVAL real)
returns (c_real1 real, c_real2 real)
language c
parameter style sql
external name 'qa_func_real_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_real_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_double_precision_mvf
(INVAL double precision)
returns (c_double_precision1 double precision, c_double_precision2 double precision)
language c
parameter style sql
external name 'qa_func_double_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_double_precision_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_date_mvf
(INVAL date)
returns (c_date1 date, c_date2 date)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_date_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_time_mvf
(INVAL time)
returns (c_time1 time, c_time2 time)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_time_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_time5_mvf
(INVAL time(5))
returns (c_time51 time(5), c_time52 time(5))
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_time5_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_timestamp_mvf
(INVAL timestamp)
returns (c_timestamp1 timestamp, c_timestamp2 timestamp)
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_timestamp_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_timestamp5_mvf
(INVAL timestamp(5))
returns (c_timestamp51 timestamp(5), c_timestamp52 timestamp(5))
language c
parameter style sql
external name 'qa_func_char_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_timestamp5_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_clob_mvf
(INVAL clob)
returns (c_clob1 clob, c_clob2 clob)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_clob_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_blob_mvf
(INVAL blob)
returns (c_blob1 blob, c_blob2 blob)
language c
parameter style sql
external name 'qa_func_vcstruct_mvf'
library qa_udf_lib
deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_blob_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create function qa_udf_integer_nondeterministic_mvf
(INVAL int)
returns (c_integer_nondeterministic1 int, c_integer_nondeterministic2 int)
language c
parameter style sql
external name 'qa_func_int32_mvf'
library qa_udf_lib
not deterministic
state area size 1024
allow any parallelism
no sql;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl function qa_udf_integer_nondeterministic_mvf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    _dci.expect_any_substr(output, 'NOT DETERMINISTIC');

    _testmgr.testcase_end(desc)

