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

def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table myShortTable (c1 int, c2 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myShortTable values (1,1),(2,2),(3,3),(4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '4')

    stmt = """select * from myShortTable ORDER BY c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)

    stmt = """create table myFullTable (
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
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myFullTable values
('CHAR_1', 'char_1', 'char_1', 'CHARVAR_1', 'charvar_1', 'charvar_1', 'VARCHAR_1', 'varchar_1', 'varchar_1', 'NCHAR_1', 'nchar_1', 'nchar_1', 'NCHARVAR_1', 'ncharvar_1', 'ncharvar_1', -1, 1, -1.11, 1.11, -1, 1, -1, -1, 1, -1.11, -1.11, -1.11, date '2001-01-01', time '01:01:01', time '01:01:01.12345', timestamp '2001-01-01 01:01:01.123456', timestamp '2001-01-01 01:01:01.12345', interval '01-01' year to month, 'clob_1', 'blob_1'
),
('CHAR_2', 'char_2', 'char_2', 'CHARVAR_2', 'charvar_2', 'charvar_2', 'VARCHAR_2', 'varchar_2', 'varchar_2', 'NCHAR_2', 'nchar_2', 'nchar_2', 'NCHARVAR_2', 'ncharvar_2', 'ncharvar_2', -2, 2, -2.22, 2.22, -2, 2, -2, -2, 2, -2.22, -2.22, -2.22, date '2002-02-02', time '02:02:02', time '02:02:02.12345', timestamp '2002-02-02 02:02:02.123456', timestamp '2002-02-02 02:02:02.12345', interval '02-02' year to month, 'clob_2', 'blob_2'
),
('CHAR_3', 'char_3', 'char_3', 'CHARVAR_3', 'charvar_3', 'charvar_3', 'VARCHAR_3', 'varchar_3', 'varchar_3', 'NCHAR_3', 'nchar_3', 'nchar_3', 'NCHARVAR_3', 'ncharvar_3', 'ncharvar_3', -3, 3, -3.33, 3.33, -3, 3, -3, -3, 3, -3.33, -3.33, -3.33, date '2003-03-03', time '03:03:03', time '03:03:03.12345', timestamp '2003-03-03 03:03:03.123456', timestamp '2003-03-03 03:03:03.12345', interval '03-03' year to month, 'clob_3', 'blob_3'
),
('CHAR_4', 'char_4', 'char_4', 'CHARVAR_4', 'charvar_4', 'charvar_4', 'VARCHAR_4', 'varchar_4', 'varchar_4', 'NCHAR_4', 'nchar_4', 'nchar_4', 'NCHARVAR_4', 'ncharvar_4', 'ncharvar_4', -4, 4, -4.44, 4.44, -4, 4, -4, -4, 4, -4.44, -4.44, -4.44, date '2004-04-04', time '04:04:04', time '04:04:04.12345', timestamp '2004-04-04 04:04:04.123456', timestamp '2004-04-04 04:04:04.12345', interval '04-04' year to month, 'clob_4', 'blob_4'
),
(null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
   
    stmt = """select * from myFullTable ORDER BY c_integer_unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5) 

    stmt = """create table myFullPositionTable (
C00_CHAR char(50),
C01_CHAR char(50) upshift,
C02_CHAR char(50) not casespecific,
C03_VARCHAR char varying(50),
C04_VARCHAR char varying(50) upshift,
C05_VARCHAR char varying(50) not casespecific,
C06_VARCHAR varchar(50),
C07_VARCHAR varchar(50) upshift,
C08_VARCHAR varchar(50) not casespecific,
C09_CHAR nchar(50),
C10_CHAR nchar(50) upshift,
C11_CHAR nchar(50) not casespecific,
C12_VARCHAR nchar varying(50),
C13_VARCHAR nchar varying(50) upshift,
C14_VARCHAR nchar varying(50) not casespecific,
C15_NUMERIC numeric(9,2),
C16_NUMERIC_UNSIGNED numeric(9,2) unsigned,
C17_DECIMAL_LSE decimal(9,2),
C18_DECIMAL_UNSIGNED decimal(9,2) unsigned,
C19_INT integer,
C20_INT_UNSIGNED integer unsigned,
C21_LARGEINT largeint,
C22_SMALLINT smallint,
C23_SMALLINT_UNSIGNED smallint unsigned,
C24_DOUBLE_PRECISION float(10),
C25_REAL real,
C26_DOUBLE_PRECISION double precision,
C27_DATE date,
C28_TIME time,            -- default is (0)
C29_TIME time(5),
C30_TIMESTAMP timestamp,  -- default is (6)
C31_TIMESTAMP timestamp(5),
C32_INTERVAL interval year to month,
C33_VARCHAR clob,
C34_VARCHAR blob
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myFullPositionTable values (
'0',
'1',
'2',
'3',
'4',
'5',
'6',
'7',
'8',
_ucs2'9',
_ucs2'10',
_ucs2'11',
_ucs2'12',
_ucs2'13',
_ucs2'14',
15.15,
16.16,
17.17,
18.18,
19,
20,
21,
22,
23,
24,
25,
26,
date '2027-01-01',
time '01:01:28',
time '01:01:29.12345',
timestamp '2030-01-01 01:01:30.123456',
timestamp '2031-01-01 01:01:31.12345',
interval '32-01' year to month,
'33',
'34'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """select * from myFullPositionTable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)

    _testmgr.testcase_end(desc)

