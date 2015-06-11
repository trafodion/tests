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

# This testcase verifies UDF invocation

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc="""Create library"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create library qaTmudfLib file """ + defs.qa_tmudf_lib + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

def test002(desc="""Register TMUDFs"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table_mapping function qaTmudfGeneral
(test_what char(100),
test_parm char(100))
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl table_mapping function qaTmudfGeneral;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table_mapping function qaTmudfInParms(
test_what char(100),
test_parm char(100),
P02_CHAR char(50),
P03_CHAR char(50) upshift,
P04_CHAR char(50) not casespecific,
P05_VARCHAR char varying(50),
P06_VARCHAR char varying(50) upshift,
P07_VARCHAR char varying(50) not casespecific,
P08_VARCHAR varchar(50),
P09_VARCHAR varchar(50) upshift,
P10_VARCHAR varchar(50) not casespecific,
P11_CHAR nchar(50),
P12_CHAR nchar(50) upshift,
P13_CHAR nchar(50) not casespecific,
P14_VARCHAR nchar varying(50),
P15_VARCHAR nchar varying(50) upshift,
P16_VARCHAR nchar varying(50) not casespecific,
P17_NUMERIC numeric(9,2),
P18_NUMERIC_UNSIGNED numeric(9,2) unsigned,
P19_DECIMAL_LSE decimal(9,2),
P20_DECIMAL_UNSIGNED decimal(9,2) unsigned,
P21_INT integer,
P22_INT_UNSIGNED integer unsigned,
P23_LARGEINT largeint,
P24_SMALLINT smallint,
P25_SMALLINT_UNSIGNED smallint unsigned,
P26_DOUBLE_PRECISION float(10),
P27_REAL real,
P28_DOUBLE_PRECISION double precision,
P29_DATE date,
P30_TIME time,           -- default is (0)
P31_TIME time(5),
P32_TIMESTAMP timestamp, -- default is (6)
P33_TIMESTAMP timestamp(5),
P34_INTERVAL interval year to month,
P35_VARCHAR clob,
P36_VARCHAR blob
)
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl table_mapping function qaTmudfInParms;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table_mapping function qaTmudfOutParms(
test_what char(100),
test_parm char(100))
returns (
c_char char(50),
c_char_upshift char(50) upshift,
c_char_not_casespecific char(50) not casespecific,
c_char_varying char varying(50),
c_char_varying_upshift char varying(50) upshift,
c_char_varying_not_casespecific char varying(50) not casespecific,
c_varchar varchar(50),
c_varchar_upshift varchar(50) upshift,
c_varchar_not_casespecific varchar(50) not casespecific,
c_nchar nchar(50),
c_nchar_upshift nchar(50) upshift,
c_nchar_not_casespecific nchar(50) not casespecific,
c_nchar_varying nchar varying(50),
c_nchar_varying_upshift nchar varying(50) upshift,
c_nchar_varying_not_casespecific nchar varying(50) not casespecific,
c_numeric numeric(9,2),
c_numeric_unsigned numeric(9,2) unsigned,
c_decimal decimal(9,2),
c_decimal_unsigned decimal(9,2) unsigned,
c_integer integer,
c_integer_unsigned integer unsigned,
c_largeint largeint,
c_smallint smallint,
c_smallint_unsigned smallint unsigned,
c_float float(10),
c_real real,
c_double_precision double precision,
c_date date,
c_time time,           -- default is (0)
c_time5 time(5),
c_timestamp timestamp, -- default is (6)
c_timestamp5 timestamp(5),
c_interval interval year to month,
c_clob clob,
c_blob blob
)
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl table_mapping function qaTmudfOutParms;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table_mapping function qaTmudfOutParmsWithExtras(
test_what char(100),
test_parm char(100))
returns (
c_del_char char(50),
c_del_char_upshift char(50) upshift,
c_del_char_not_casespecific char(50) not casespecific,
c_del_char_varying char varying(50),
c_del_char_varying_upshift char varying(50) upshift,
c_del_char_varying_not_casespecific char varying(50) not casespecific,
c_del_varchar varchar(50),
c_del_varchar_upshift varchar(50) upshift,
c_del_varchar_not_casespecific varchar(50) not casespecific,
c_del_nchar nchar(50),
c_del_nchar_upshift nchar(50) upshift,
c_del_nchar_not_casespecific nchar(50) not casespecific,
c_del_nchar_varying nchar varying(50),
c_del_nchar_varying_upshift nchar varying(50) upshift,
c_del_nchar_varying_not_casespecific nchar varying(50) not casespecific,
c_del_numeric numeric(9,2),
c_del_numeric_unsigned numeric(9,2) unsigned,
c_del_decimal decimal(9,2),
c_del_decimal_unsigned decimal(9,2) unsigned,
c_del_integer integer,
c_del_integer_unsigned integer unsigned,
c_del_largeint largeint,
c_del_smallint smallint,
c_del_smallint_unsigned smallint unsigned,
c_del_float float(10),
c_del_real real,
c_del_double_precision double precision,
c_del_date date,
c_del_time time,           -- default is (0)
c_del_time5 time(5),
c_del_timestamp timestamp, -- default is (6)
c_del_timestamp5 timestamp(5),
c_del_interval interval year to month,
c_del_clob clob,
c_del_blob blob,
c_char char(50),
c_char_upshift char(50) upshift,
c_char_not_casespecific char(50) not casespecific,
c_char_varying char varying(50),
c_char_varying_upshift char varying(50) upshift,
c_char_varying_not_casespecific char varying(50) not casespecific,
c_varchar varchar(50),
c_varchar_upshift varchar(50) upshift,
c_varchar_not_casespecific varchar(50) not casespecific,
c_nchar nchar(50),
c_nchar_upshift nchar(50) upshift,
c_nchar_not_casespecific nchar(50) not casespecific,
c_nchar_varying nchar varying(50),
c_nchar_varying_upshift nchar varying(50) upshift,
c_nchar_varying_not_casespecific nchar varying(50) not casespecific,
c_numeric numeric(9,2),
c_numeric_unsigned numeric(9,2) unsigned,
c_decimal decimal(9,2),
c_decimal_unsigned decimal(9,2) unsigned,
c_integer integer,
c_integer_unsigned integer unsigned,
c_largeint largeint,
c_smallint smallint,
c_smallint_unsigned smallint unsigned,
c_float float(10),
c_real real,
c_double_precision double precision,
c_date date,
c_time time,           -- default is (0)  
c_time5 time(5),
c_timestamp timestamp, -- default is (6)
c_timestamp5 timestamp(5),
c_interval interval year to month,
c_clob clob,
c_blob blob
)
external name 'QA_TMUDF'
language cpp
library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """showddl table_mapping function qaTmudfOutParmsWithExtras;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """get table_mapping functions for library qaTmudfLib;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'QATMUDFGENERAL')
    _dci.expect_any_substr(output, 'QATMUDFINPARMS')
    _dci.expect_any_substr(output, 'QATMUDFOUTPARMS')
    _dci.expect_any_substr(output, 'QATMUDFOUTPARMSWITHEXTRAS')

    _testmgr.testcase_end(desc)

