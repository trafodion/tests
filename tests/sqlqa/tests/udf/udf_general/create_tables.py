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

    # Set up tables for UDF testing
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
-- this data type is not supported: c_interval interval year to month
c_clob clob,
c_blob blob
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myFullTable values
('CHAR_1', 'char_1', 'char_1', 'CHARVAR_1', 'charvar_1', 'charvar_1', 'VARCHAR_1', 'varchar_1', 'varchar_1', 'NCHAR_1', 'nchar_1', 'nchar_1', 'NCHARVAR_1', 'ncharvar_1', 'ncharvar_1', -1, 1, -1.11, 1.11, -1, 1, -1, -1, 1, -1.11, -1.11, -1.11, date '2001-01-01', time '01:01:01', time '01:01:01.12345', timestamp '2001-01-01 01:01:01.123456', timestamp '2001-01-01 01:01:01.12345', 'clob_1', 'blob_1'),
('CHAR_2', 'char_2', 'char_2', 'CHARVAR_2', 'charvar_2', 'charvar_2', 'VARCHAR_2', 'varchar_2', 'varchar_2', 'NCHAR_2', 'nchar_2', 'nchar_2', 'NCHARVAR_2', 'ncharvar_2', 'ncharvar_2', -2, 2, -2.22, 2.22, -2, 2, -2, -2, 2, -2.22, -2.22, -2.22, date '2002-02-02', time '02:02:02', time '02:02:02.12345', timestamp '2002-02-02 02:02:02.123456', timestamp '2002-02-02 02:02:02.12345', 'clob_2', 'blob_2'),
('CHAR_3', 'char_3', 'char_3', 'CHARVAR_3', 'charvar_3', 'charvar_3', 'VARCHAR_3', 'varchar_3', 'varchar_3', 'NCHAR_3', 'nchar_3', 'nchar_3', 'NCHARVAR_3', 'ncharvar_3', 'ncharvar_3', -3, 3, -3.33, 3.33, -3, 3, -3, -3, 3, -3.33, -3.33, -3.33, date '2003-03-03', time '03:03:03', time '03:03:03.12345', timestamp '2003-03-03 03:03:03.123456', timestamp '2003-03-03 03:03:03.12345', 'clob_3', 'blob_3'),
('CHAR_4', 'char_4', 'char_4', 'CHARVAR_4', 'charvar_4', 'charvar_4', 'VARCHAR_4', 'varchar_4', 'varchar_4', 'NCHAR_4', 'nchar_4', 'nchar_4', 'NCHARVAR_4', 'ncharvar_4', 'ncharvar_4', -4, 4, -4.44, 4.44, -4, 4, -4, -4, 4, -4.44, -4.44, -4.44, date '2004-04-04', time '04:04:04', time '04:04:04.12345', timestamp '2004-04-04 04:04:04.123456', timestamp '2004-04-04 04:04:04.12345', 'clob_4', 'blob_4'),
(null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table myFullDoubleWideTable (
c_char1 char(50),
c_char2 char(50),
c_char_upshift1 char(50) upshift,
c_char_upshift2 char(50) upshift,
c_char_not_casespecific1 char(50) not casespecific,
c_char_not_casespecific2 char(50) not casespecific,
c_char_varying1 char varying(50),
c_char_varying2 char varying(50),
c_char_varying_upshift1 char varying(50) upshift,
c_char_varying_upshift2 char varying(50) upshift,
c_char_varying_not_casespecific1 char varying(50) not casespecific,
c_char_varying_not_casespecific2 char varying(50) not casespecific,
c_varchar1 varchar(50),
c_varchar2 varchar(50),
c_varchar_upshift1 varchar(50) upshift,
c_varchar_upshift2 varchar(50) upshift,
c_varchar_not_casespecific1 varchar(50) not casespecific,
c_varchar_not_casespecific2 varchar(50) not casespecific,
c_nchar1 nchar(50),
c_nchar2 nchar(50),
c_nchar_upshift1 nchar(50) upshift,
c_nchar_upshift2 nchar(50) upshift,
c_nchar_not_casespecific1 nchar(50) not casespecific,
c_nchar_not_casespecific2 nchar(50) not casespecific,
c_nchar_varying1 nchar varying(50),
c_nchar_varying2 nchar varying(50),
c_nchar_varying_upshift1 nchar varying(50) upshift,
c_nchar_varying_upshift2 nchar varying(50) upshift,
c_nchar_varying_not_casespecific1 nchar varying(50) not casespecific,
c_nchar_varying_not_casespecific2 nchar varying(50) not casespecific,
c_numeric1 numeric(9,2),
c_numeric2 numeric(9,2),
c_numeric_unsigned1 numeric(9,2) unsigned,
c_numeric_unsigned2 numeric(9,2) unsigned,
c_decimal1 decimal(9,2),
c_decimal2 decimal(9,2),
c_decimal_unsigned1 decimal(9,2) unsigned,
c_decimal_unsigned2 decimal(9,2) unsigned,
c_integer1 integer,
c_integer2 integer,
c_integer_unsigned1 integer unsigned,
c_integer_unsigned2 integer unsigned,
c_largeint1 largeint,
c_largeint2 largeint,
c_smallint1 smallint,
c_smallint2 smallint,
c_smallint_unsigned1 smallint unsigned,
c_smallint_unsigned2 smallint unsigned,
c_float1 float(10),
c_float2 float(10),
c_real1 real,
c_real2 real,
c_double_precision1 double precision,
c_double_precision2 double precision,
c_date1 date,
c_date2 date,
c_time1 time,           -- default is (0)
c_time2 time,           -- default is (0)
c_time51 time(5),
c_time52 time(5),
c_timestamp1 timestamp, -- default is (6)
c_timestamp2 timestamp, -- default is (6)
c_timestamp51 timestamp(5),
c_timestamp52 timestamp(5)
-- this data type is not supported      c_interval interval year to month
-- BUG this crashes mxosrvr right now LP#1441378: c_clob1 clob,
-- BUG this crashes mxosrvr right now LP#1441378: c_clob2 clob,
-- BUG this crashes mxosrvr right now LP#1441378: c_blob1 blob,
-- BUG this crashes mxosrvr right now LP#1441378: c_blob2 blob
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myFullDoubleWideTable values
('CHAR_1', 'CHAR_1', 'char_1', 'char_1', 'char_1', 'char_1', 'CHARVAR_1', 'CHARVAR_1', 'charvar_1', 'charvar_1', 'charvar_1', 'charvar_1', 'VARCHAR_1', 'VARCHAR_1', 'varchar_1', 'varchar_1', 'varchar_1', 'varchar_1', 'NCHAR_1', 'NCHAR_1', 'nchar_1', 'nchar_1', 'nchar_1', 'nchar_1', 'NCHARVAR_1', 'NCHARVAR_1', 'ncharvar_1', 'ncharvar_1', 'ncharvar_1', 'ncharvar_1', -1, -1, 1, 1, -1.11, -1.11, 1.11, 1.11, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1.11, -1.11, -1.11, -1.11, -1.11, -1.11, date '2001-01-01', date '2001-01-01', time '01:01:01', time '01:01:01', time '01:01:01.12345', time '01:01:01.12345', timestamp '2001-01-01 01:01:01.123456', timestamp '2001-01-01 01:01:01.123456', timestamp '2001-01-01 01:01:01.12345', timestamp '2001-01-01 01:01:01.12345'
-- BUG this crashes mxosrvr right now LP#1441378: , 'clob_1', 'clob_1', 'blob_1', 'blob_1'
),
('CHAR_2', 'CHAR_2', 'char_2', 'char_2', 'char_2', 'char_2', 'CHARVAR_2', 'CHARVAR_2', 'charvar_2', 'charvar_2', 'charvar_2', 'charvar_2', 'VARCHAR_2', 'VARCHAR_2', 'varchar_2', 'varchar_2', 'varchar_2', 'varchar_2', 'NCHAR_2', 'NCHAR_2', 'nchar_2', 'nchar_2', 'nchar_2', 'nchar_2', 'NCHARVAR_2', 'NCHARVAR_2', 'ncharvar_2', 'ncharvar_2', 'ncharvar_2', 'ncharvar_2', -2, -2, 2, 2, -2.22, -2.22, 2.22, 2.22, -2, -2, 2, 2, -2, -2, -2, -2, 2, 2, -2.22, -2.22, -2.22, -2.22, -2.22, -2.22, date '2002-02-02', date '2002-02-02', time '02:02:02', time '02:02:02', time '02:02:02.12345', time '02:02:02.12345', timestamp '2002-02-02 02:02:02.123456', timestamp '2002-02-02 02:02:02.123456', timestamp '2002-02-02 02:02:02.12345', timestamp '2002-02-02 02:02:02.12345'
-- BUG this crashes mxosrvr right now LP#1441378: , 'clob_2', 'clob_2', 'blob_2', 'blob_2'
),
('CHAR_3', 'CHAR_3', 'char_3', 'char_3', 'char_3', 'char_3', 'CHARVAR_3', 'CHARVAR_3', 'charvar_3', 'charvar_3', 'charvar_3', 'charvar_3', 'VARCHAR_3', 'VARCHAR_3', 'varchar_3', 'varchar_3', 'varchar_3', 'varchar_3', 'NCHAR_3', 'NCHAR_3', 'nchar_3', 'nchar_3', 'nchar_3', 'nchar_3', 'NCHARVAR_3', 'NCHARVAR_3', 'ncharvar_3', 'ncharvar_3', 'ncharvar_3', 'ncharvar_3', -3, -3, 3, 3, -3.33, -3.33, 3.33, 3.33, -3, -3, 3, 3, -3, -3, -3, -3, 3, 3, -3.33, -3.33, -3.33, -3.33, -3.33, -3.33, date '2003-03-03', date '2003-03-03', time '03:03:03', time '03:03:03', time '03:03:03.12345', time '03:03:03.12345', timestamp '2003-03-03 03:03:03.123456', timestamp '2003-03-03 03:03:03.123456', timestamp '2003-03-03 03:03:03.12345', timestamp '2003-03-03 03:03:03.12345'
-- BUG this crashes mxosrvr right now LP#1441378: , 'clob_3', 'clob_3', 'blob_3', 'blob_3'
),
('CHAR_4', 'CHAR_4', 'char_4', 'char_4', 'char_4', 'char_4', 'CHARVAR_4', 'CHARVAR_4', 'charvar_4', 'charvar_4', 'charvar_4', 'charvar_4', 'VARCHAR_4', 'VARCHAR_4', 'varchar_4', 'varchar_4', 'varchar_4', 'varchar_4', 'NCHAR_4', 'NCHAR_4', 'nchar_4', 'nchar_4', 'nchar_4', 'nchar_4', 'NCHARVAR_4', 'NCHARVAR_4', 'ncharvar_4', 'ncharvar_4', 'ncharvar_4', 'ncharvar_4', -4, -4, 4, 4, -4.44, -4.44, 4.44, 4.44, -4, -4, 4, 4, -4, -4, -4, -4, 4, 4, -4.44, -4.44, -4.44, -4.44, -4.44, -4.44, date '2004-04-04', date '2004-04-04', time '04:04:04', time '04:04:04', time '04:04:04.12345', time '04:04:04.12345', timestamp '2004-04-04 04:04:04.123456', timestamp '2004-04-04 04:04:04.123456', timestamp '2004-04-04 04:04:04.12345', timestamp '2004-04-04 04:04:04.12345'
-- BUG this crashes mxosrvr right now LP#1441378: , 'clob_4', 'clob_4', 'blob_4', 'blob_4'
),
(null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null
-- BUG this crashes mxosrvr right now LP#1441378: , null, null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)

    stmt = """create table mytable
(a int not null not droppable primary key,
b int,
c int,
d char(50),
e varchar(50));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into mytable values
(1,1,1,'AAA','AAA'),
(2,2,2,'BBB','BBB'),
(3,3,3,'CCC','CCC'),
(4,4,4,'DDD','DDD'),
(5,5,5,'EEE','EEE');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create view myview as select a, b from mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table mytable2 like mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into mytable2 (select * from mytable);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table myonerowtable like mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """insert into myonerowtable values (6,6,6,'FFF','FFF');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

    stmt = """create table myemptytable like mytable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)

