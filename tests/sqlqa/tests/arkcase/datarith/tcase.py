# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc="""a000"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # testA001
    
    stmt = """create table dtarit1 (
dt1 date,
dt2 date,
ivy interval year
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit1 values (
date '1997-01-21',
date '1993-01-21',
interval '3' year
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tmarith1 (
tm1 time,
tm2 time,
ivh interval hour
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tmarith1 values (
time '22:30:00',
time '12:30:00',
interval '10' hour
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA002
    #
    stmt = """create table dtarit2 (
dt   date,
ts   timestamp,
ivyr interval year,
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit2 values (
date '1997-01-21',
timestamp '1993-01-21:10:30:45',
interval '3' year,
interval '6' month,
interval '20' day,
interval '12' hour,
interval '59' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit2 values (
date '2000-01-01',
timestamp '1999-12-31:23:59:59.999999',
interval - '3' year,
interval - '6' month,
interval - '20' day,
interval - '12' hour,
interval - '59' minute,
interval - '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table dtarit2x (
dt   date,
ts   timestamp,
ivyr interval year,
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit2x values (
date '9999-12-31',
timestamp '9999-12-31:23:59:59.999999',
interval '1' year,
interval '2' month,
interval '3' day,
interval '4' hour,
interval '5' minute,
interval '6' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA002b and testA003b
    
    stmt = """create table dtarit2b (
tm   time (6),
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit2b values (
time '14:30:22',
interval '12' hour,
interval '59' minute,
interval '0.000001' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit2b values (
time '00:00:00',
interval - '23' hour,
interval - '59' minute,
interval  '59' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit2b values (
time '23:59:59',
interval '0' hour,
interval '0' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA002c and testA003c
    #
    stmt = """create table dtarit2c (
tm   time,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit2c values (
time '14:30:22',
interval '12' hour,
interval '59' minute,
interval '1' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit2c values (
time '00:00:00',
interval - '23' hour,
interval - '59' minute,
interval  '59' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit2c values (
time '23:59:59',
interval '0' hour,
interval '0' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA003
    #
    stmt = """create table dtarit3 (
dt   date,
ts   timestamp,
ivyr interval year,
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit3 values (
date '1997-01-21',
timestamp '1993-01-21:10:30:45',
interval '3' year,
interval '6' month,
interval '20' day,
interval '12' hour,
interval '59' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit3 values (
date '1997-12-03',
timestamp '2000-01-01:00:00:00',
interval '6' year,
interval '5' month,
interval '4' day,
interval '3' hour,
interval '2' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table dtarit3x (
dt   date,
ts   timestamp,
ivyr interval year,
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit3x values (
date '0001-01-01',
timestamp '0001-01-01:00:00:00',
interval '1' year,
interval '2' month,
interval '3' day,
interval '4' hour,
interval '5' minute,
interval '6' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA005
    #
    
    stmt = """create table dtarit5 (
ivyr interval year (4),
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit5 values (		-- normal values
interval '1997' year (4),
interval '6' month,
interval '15' day,
interval '12' hour,
interval '59' minute,
interval '1' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit5 values (		-- max values
interval '9999' year (4),
interval '31' month,
interval '24' day,
interval - '23' hour,
interval - '59' minute,
interval - '59' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit5 values (		-- min values
interval '0' year,
interval '0' month,
interval '0' day,
interval '0' hour,
interval '0' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA006
    #
    
    stmt = """create table dtarit6 (
ivyr interval year (4),
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit6 values (		-- normal values
interval '1997' year (4),
interval '6' month,
interval '15' day,
interval '12' hour,
interval '59' minute,
interval '1' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit6 values (		-- max values
interval '9999' year (4),
interval '31' month,
interval '24' day,
interval - '23' hour,
interval - '59' minute,
interval - '59' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit6 values (		-- min values
interval '0' year,
interval '0' month,
interval '0' day,
interval '0' hour,
interval '0' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA007
    
    stmt = """create table dtarit7 (
ivyr interval year (4),
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit7 values (		-- normal values
interval '2000' year (4),
interval '10' month,
interval '2' day,
interval '15' hour,
interval '60' minute,
interval '12' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit7 values (		-- max values
interval '9999' year (4),
interval '31' month,
interval '24' day,
interval - '23' hour,
interval - '59' minute,
interval - '59' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit7 values (		-- min values
interval '0' year,
interval '0' month,
interval '0' day,
interval '0' hour,
interval '0' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA008
    #
    stmt = """create table dtarit8 (
ivyr interval year (4),
ivmt interval month,
ivdy interval day,
ivhr interval hour,
ivmn interval minute,
ivsc interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit8 values (		-- normal values
interval '2000' year (4),
interval '10' month,
interval '2' day,
interval '15' hour,
interval '60' minute,
interval '12' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit8 values (		-- max values
interval '9999' year (4),
interval '31' month,
interval '24' day,
interval - '23' hour,
interval - '59' minute,
interval - '59' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit8 values (		-- min values
interval '0' year,
interval '0' month,
interval '0' day,
interval '0' hour,
interval '0' minute,
interval '0' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA009
    #
    stmt = """create table dtarit9a (
yr   largeint,
mt   smallint,
dy   int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dtarit9b (
hr   largeint,
mn   smallint,
sc   int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dtarit9a values (    	-- zero values
0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9a values (    	-- positive values
2, 2, 2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9a values (    	-- nulls
null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9a values (    	-- negative values
-4, -4, -4
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9b values (    	-- zero values
0, 0, 0
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9b values (    	-- positive values
5, 5, 5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9b values (    	-- nulls
null, null, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into dtarit9b values (    	-- negative values
-10, -10, -10
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: DATE - DATE => INTERVAL
    #
    #    +------------+---+-------------+-----------+
    #     1st operand   op  2nd operand   result
    #    +------------+---+-------------+-----------+
    #      datetime     -    datetime     interval
    #    +------------+---+-------------+-----------+
    #
    # For examples of DATE - DATE see C.H.Date, Guide... 4th ed. p.275.
    #
    # Notes: this test is pretty sparse because nothing works yet (Jan 1997)
    
    stmt = """select * from dtarit1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s0')
    
    #  expect 1 row with the following values:
    # 	DT1         DT2         IVY
    # 	----------  ----------  ---
    # 	1997-01-21  1993-01-21   03
    
    stmt = """select (dt1 - dt2) year to month from dtarit1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    #  expect 1 row with the difference : 4
    
    stmt = """select dt1 - ivy from dtarit1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s2')
    #  expect 1 row with the value 1994-01-21
    
    #  DATE - DATE using the timestamp functions
    stmt = """select juliantimestamp (dt1),
juliantimestamp (dt2),
juliantimestamp (dt1) - juliantimestamp (dt2)
from dtarit1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s3')
    #  expect 1 row with the following values:
    #   211720564800000000    211594334400000000       126230400000000
    
    stmt = """select * from tmarith1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s4')
    #  expect 1 row with the following values:
    #  	22:30:00  12:30:00   10
    
    stmt = """select (tm1 - tm2) seconds from tmarith1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s5')
    #  expect 1 row with the difference in seconds: 36000
    
    stmt = """select tm1 - ivh from tmarith1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s6')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: DATE + INTERVAL => date
    #
    #    +------------+----+-------------+-----------+
    #     1st operand   op   2nd operand   result
    #    +------------+----+-------------+-----------+
    #      datetime      +    interval     datetime
    #    +------------+----+-------------+-----------+
    #
    
    stmt = """select * from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s0')
    #  expect 2 rows with the following values:
    #  DT          TS                          IVYR  IVMT  IVDY  IVHR  IVMN  IVSC
    #  ----------  --------------------------  ----  ----  ----  ----  ----  ----
    #
    #  1997-01-21  1993-01-21:10:30:45.000000    03    06    20    12    59    00
    #  2000-01-01  1999-12-31:23:59:59.999999   -03   -06   -20   -12   -59    00
    
    stmt = """select dt, ivyr, dt + ivyr from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s1')
    #  expect 2 rows with the following values:
    #  	1997-01-21    03  2000-01-21
    #  	2000-01-01   -03  1997-01-01
    
    stmt = """select dt, ivmt, dt + ivmt from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s2')
    #  expect 2 rows with the following values:
    #     1997-01-21    06  1997-07-21
    #     2000-01-01   -06  1999-07-01
    
    stmt = """select dt, ivdy, dt + ivdy from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s3')
    #  expect 2 rows with the following values:
    #     1997-01-21    20  1997-02-10
    #     2000-01-01   -20  1999-12-12
    
    stmt = """select ts, ivyr, ts + ivyr * 2 from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s4')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    03  1999-01-21:10:30:45.000000
    #     1999-12-31:23:59:59.999999   -03  1993-12-31:23:59:59.999999
    
    ##expectfile ${test_dir}/a002exp a002s5
    stmt = """select ts, ivmt, ts + ivmt from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    06  1993-07-21:10:30:45.000000
    #     1999-12-31:23:59:59.999999   -06  1999-06-31 23:59:59.999999
    #  the second row gets an error
    
    stmt = """select ts, ivdy, ts + ivdy from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s6')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    20  1993-02-10:10:30:45.000000
    #     1999-12-31:23:59:59.999999   -20  1999-12-11:23:59:59.999999
    
    stmt = """select ts, ivhr, ts + ivhr from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s7')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    12  1993-01-21:22:30:45.000000
    #     1999-12-31:23:59:59.999999   -12  1999-12-31:11:59:59.999999
    
    stmt = """select ts, ivmn, ts + ivmn from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s8')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    59  1993-01-21:11:29:45.000000
    #     1999-12-31:23:59:59.999999   -59  1999-12-31:23:00:59.999999
    
    stmt = """select ts, ivsc, ts + ivsc from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s9')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    00  1993-01-21:10:30:45.000000
    #     1999-12-31:23:59:59.999999    00  1999-12-31:23:59:59.999999
    
    stmt = """select ts, ts + interval '1' second from dtarit2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s10')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000  1993-01-21:10:30:46.000000
    #     1999-12-31:23:59:59.999999  2000-01-01:00:00:00.999999
    
    #
    #  Negative tests: attempt to produce invalid dates and timestamps
    #
    stmt = """select * from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s11')
    #  expect 1 row with the following values:
    #  DT          TS                          IVYR  IVMT  IVDY  IVHR  IVMN  IVSC
    #
    #  ----------  --------------------------  ----  ----  ----  ----  ----  ----------
    # -
    #  9999-12-31  9999-12-31 23:59:59.999999     1     2     3     4     5    6.000000
    
    #  each of the following queries should produce an invalid date error
    ##expectfile ${test_dir}/a002exp a002s12
    stmt = """select dt + ivyr from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s13
    stmt = """select ts + ivyr * 2 from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s14
    stmt = """select dt + ivmt from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s15
    stmt = """select ts + ivmt from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s16
    stmt = """select dt + ivdy from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s17
    stmt = """select ts + ivdy from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s18
    stmt = """select ts + ivhr from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s19
    stmt = """select ts + ivmn from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s20
    stmt = """select ts + ivsc from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a002exp a002s21
    stmt = """select ts + interval '1' second from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    
    #  Negative: attempt to update to an invalid date
    ##expectfile ${test_dir}/a002exp a002s22
    stmt = """update dtarit2x set dt = dt + interval '4' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    #  expect error
    
    ##expectfile ${test_dir}/a002exp a002s23
    stmt = """update dtarit2x set ts = ts + interval '4' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    #  expect error
    
    stmt = """select * from dtarit2x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s24')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a002b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: TIME + INTERVAL => time
    #
    #    +------------+----+-------------+-----------+
    #     1st operand   op   2nd operand   result
    #    +------------+----+-------------+-----------+
    #      datetime      +    interval     datetime
    #    +------------+----+-------------+-----------+
    #
    # Notes: the table dtarit2b is also used for testA003b
    
    stmt = """select * from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs0')
    #  expect 3 rows with the following values:
    #  	TM        IVHR  IVMN  IVSC
    #  	--------  ----  ----  ----
    #  	14:30:22    12    59    00
    #  	00:00:00   -23   -59    59
    #  	23:59:59    00    00    00
    
    stmt = """select tm, ivhr, tm + ivhr from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs1')
    #  expect 3 rows with the following values:
    #  	14:30:22    12  02:30:22
    #  	00:00:00   -23  01:00:00
    #  	23:59:59    00  23:59:59
    
    stmt = """select tm, ivhr, tm + ivhr * 2 from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs2')
    #  expect 3 rows with the following values:
    #     14:30:22    12  14:30:22
    #     00:00:00   -23  02:00:00
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, ivmn, tm + ivmn from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs3')
    #  expect 3 rows with the following values:
    #     14:30:22    59  15:29:22
    #     00:00:00   -59  23:01:00
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, ivsc, tm + ivsc from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs4')
    #  expect 3 rows with the following values:
    #     14:30:22    00  14:30:22
    #     00:00:00   -59  23:59:01
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, tm + interval '40' hour from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs5')
    #  expect 3 rows with the following values:
    #     14:30:22  06:30:22
    #     00:00:00  16:00:00
    #     23:59:59  15:59:59
    
    #  add 24 hours of minutes + 1
    stmt = """select tm, tm + interval '1441' minute (4) from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs6')
    #  expect 3 rows with the following values:
    #     14:30:22  14:31:22
    #     00:00:00  00:01:00
    #     23:59:59  00:00:59
    
    #  add 24 hours of seconds + 1
    stmt = """select tm, tm + interval '86401' second (5) from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002bexp""", 'a002bs7')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a002c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: TIME + INTERVAL => time
    #
    #    +------------+----+-------------+-----------+
    #     1st operand   op   2nd operand   result
    #    +------------+----+-------------+-----------+
    #      datetime      +    interval     datetime
    #    +------------+----+-------------+-----------+
    #
    # Notes: the table dtarit2c is also used for testA003b
    
    stmt = """select * from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs0')
    #  expect 3 rows with the following values:
    #  	TM        IVHR  IVMN  IVSC
    #  	--------  ----  ----  ----
    #  	14:30:22    12    59    01
    #  	00:00:00   -23   -59    59
    #  	23:59:59    00    00    00
    
    stmt = """select tm, ivhr, tm + ivhr from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs1')
    #  expect 3 rows with the following values:
    #  	14:30:22    12  02:30:22
    #  	00:00:00   -23  01:00:00
    #  	23:59:59    00  23:59:59
    
    stmt = """select tm, ivhr, tm + ivhr * 2 from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs2')
    #  expect 3 rows with the following values:
    #     14:30:22    12  14:30:22
    #     00:00:00   -23  02:00:00
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, ivmn, tm + ivmn from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs3')
    #  expect 3 rows with the following values:
    #     14:30:22    59  15:29:22
    #     00:00:00   -59  23:01:00
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, ivsc, tm + ivsc from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs4')
    #  expect 3 rows with the following values:
    #     14:30:22    01  14:30:23
    #     00:00:00    59  00:00:59
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, tm + interval '40' hour from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs5')
    #  expect 3 rows with the following values:
    #     14:30:22  06:30:22
    #     00:00:00  16:00:00
    #     23:59:59  15:59:59
    
    #  add 24 hours of minutes + 1
    stmt = """select tm, tm + interval '1441' minute (4) from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs6')
    #  expect 3 rows with the following values:
    #     14:30:22  14:31:22
    #     00:00:00  00:01:00
    #     23:59:59  00:00:59
    
    #  add 24 hours of seconds + 1
    stmt = """select tm, tm + interval '86401' second (5) from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002cexp""", 'a002cs7')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: DATE - INTERVAL => date
    #
    #    +------------+----+-------------+-----------+
    #     1st operand   op   2nd operand   result
    #    +------------+----+-------------+-----------+
    #      datetime      -    interval     datetime
    #    +------------+----+-------------+-----------+
    #
    
    stmt = """select * from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s0')
    #  expect 2 rows with the following values:
    #  DT          TS                          IVYR  IVMT  IVDY  IVHR  IVMN  IVSC
    #  ----------  --------------------------  ----  ----  ----  ----  ----  ----
    #  1997-01-21  1993-01-21:10:30:45.000000    03    06    20    12    59    00
    #  1997-12-03  2000-01-01:00:00:00.000000    06    05    04    03    02    00
    
    stmt = """select dt, ivyr, dt - ivyr from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s1')
    #  expect 2 rows with the following values:
    #  	1997-01-21    03  1994-01-21
    #  	1997-12-03    06  1991-12-03
    
    stmt = """select dt, ivmt, dt - ivmt from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s2')
    #  expect 2 rows with the following values:
    #     1997-01-21    06  1996-07-21
    #     1997-12-03    05  1997-07-03
    
    stmt = """select dt, ivdy, dt - ivdy from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s3')
    #  expect 2 rows with the following values:
    #     1997-01-21    20  1997-01-01
    #     1997-12-03    04  1997-11-29
    
    stmt = """select ts, ivyr, ts - ivyr * 2 from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s4')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    03  1987-01-21:10:30:45.000000
    #     2000-01-01:00:00:00.000000    06  1988-01-01:00:00:00.000000
    
    stmt = """select ts, ivmt, ts - ivmt from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s5')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    06  1992-07-21:10:30:45.000000
    #     2000-01-01:00:00:00.000000    05  1999-08-01:00:00:00.000000
    
    stmt = """select ts, ivdy, ts - ivdy from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s6')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    20  1993-01-01:10:30:45.000000
    #     2000-01-01:00:00:00.000000    04  1999-12-28:00:00:00.000000
    
    stmt = """select ts, ivhr, ts - ivhr from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s7')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    12  1993-01-20:22:30:45.000000
    #     2000-01-01:00:00:00.000000    03  1999-12-31:21:00:00.000000
    
    stmt = """select ts, ivmn, ts - ivmn from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s8')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    59  1993-01-21:09:31:45.000000
    #     2000-01-01:00:00:00.000000    02  1999-12-31:23:58:00.000000
    
    stmt = """select ts, ivsc, ts - ivsc from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s9')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    00  1993-01-21:10:30:45.000000
    #     2000-01-01:00:00:00.000000    00  2000-01-01:00:00:00.000000
    
    stmt = """select ts, ts - interval '1' second from dtarit3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s10')
    #  expect 2 rows with the following values:
    #     1993-01-21:10:30:45.000000    1993-01-21:10:30:44.000000
    #     2000-01-01:00:00:00.000000    1999-12-31:23:59:59.000000
    
    #
    #  Negative tests: attempt to produce invalid dates and timestamps
    #
    stmt = """select * from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s11')
    #  expect 1 row with the following values:
    #  DT          TS                          IVYR  IVMT  IVDY  IVHR  IVMN  IVSC
    #  ----------  --------------------------  ----  ----  ----  ----  ----  ----
    #
    #  0001-01-01  0001-01-01 00:00:00.000000     1     2     3     4     5    6.000000
    
    #  each of the following queries should produce an invalid date error
    ##expectfile ${test_dir}/a003exp a003s12
    stmt = """select dt - ivyr from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s13
    stmt = """select ts - ivyr * 2 from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s14
    stmt = """select dt - ivmt from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s15
    stmt = """select ts - ivmt from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s16
    stmt = """select dt - ivdy from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s17
    stmt = """select ts - ivdy from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s18
    stmt = """select ts - ivhr from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s19
    stmt = """select ts - ivmn from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s20
    stmt = """select ts - ivsc from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    ##expectfile ${test_dir}/a003exp a003s21
    stmt = """select ts - interval '1' second from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    
    #  Negative: attempt to update to an invalid date
    ##expectfile ${test_dir}/a003exp a003s22
    stmt = """update dtarit3x set dt = dt - interval '4' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    #  expect error
    
    ##expectfile ${test_dir}/a003exp a003s23
    stmt = """update dtarit3x set ts = ts - interval '4' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    #  expect error
    
    stmt = """select * from dtarit3x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s24')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a003b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: TIME - INTERVAL => time
    #
    #    +------------+----+-------------+-----------+
    #     1st operand   op   2nd operand   result
    #    +------------+----+-------------+-----------+
    #      datetime      -    interval     datetime
    #    +------------+----+-------------+-----------+
    #
    # Notes: this test uses the same table as for testA002b
    
    stmt = """select * from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs0')
    #  expect 3 rows with the following values:
    #  	TM        IVHR  IVMN  IVSC
    #  	--------  ----  ----  ----
    #  	14:30:22    12    59    00
    #  	00:00:00   -23   -59    59
    #  	23:59:59    00    00    00
    
    stmt = """select tm, ivhr, tm - ivhr from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs1')
    #  expect 3 rows with the following values:
    #  	14:30:22    12  02:30:22
    #  	00:00:00   -23  23:00:00
    #  	23:59:59    00  23:59:59
    
    stmt = """select tm, ivhr, tm - ivhr * 2 from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs2')
    #  expect 3 rows with the following values:
    #     14:30:22    12  14:30:22
    #     00:00:00   -23  22:00:00
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, ivmn, tm - ivmn from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs3')
    #  expect 3 rows with the following values:
    #     14:30:22    59  13:31:22
    #     00:00:00   -59  00:59:00
    #     23:59:59    00  23:59:59
    
    stmt = """select tm, ivsc, tm - ivsc from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs4')
    #  expect 3 rows with the following values:
    #     14:30:22    00  14:30:22
    #     00:00:00    59  23:59:01
    #     23:59:59    00  23:59:59
    
    #  subtract 1 week of hours + 1
    stmt = """select tm, tm - interval '169' hour (3) from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs5')
    #  expect 3 rows with the following values:
    #     14:30:22  13:30:22
    #     00:00:00  23:00:00
    #     23:59:59  22:59:59
    
    #  subtract 24 hours of minutes + 1
    stmt = """select tm, tm - interval '1441' minute (4) from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs6')
    #  expect 3 rows with the following values:
    #     14:30:22  14:29:22
    #     00:00:00  23:59:00
    #     23:59:59  23:58:59
    
    #  subtract 24 hours of seconds + 1
    stmt = """select tm, tm - interval '86401' second (5) from dtarit2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003bexp""", 'a003bs7')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a003c"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: TIME - INTERVAL => time
    #
    #    +------------+----+-------------+-----------+
    #     1st operand   op   2nd operand   result
    #    +------------+----+-------------+-----------+
    #      datetime      -    interval     datetime
    #    +------------+----+-------------+-----------+
    #
    # Notes: the table dtarit2c is also used for testA003b & 3c
    
    stmt = """select * from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs0')
    
    #  expect 3 rows with the following values:
    #  TM        IVHR  IVMN  IVSC
    #  --------  ----  ----  ----
    #  14:30:22    12    59    01
    #  00:00:00   -23   -59    59
    #  23:59:59    00    00    00
    
    stmt = """select tm, tm - ivhr from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs1')
    #  expect 3 rows with the following values:
    #  	14:30:22  02:30:22
    #  	00:00:00  23:00:00
    #  	23:59:59  23:59:59
    
    stmt = """select tm, tm - ivhr * 2 from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs2')
    #  expect 3 rows with the following values:
    #     14:30:22  14:30:22
    #     00:00:00  22:00:00
    #     23:59:59  23:59:59
    
    stmt = """select tm, tm - ivmn from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs3')
    #  expect 3 rows with the following values:
    #     14:30:22  13:31:22
    #     00:00:00  00:59:00
    #     23:59:59  23:59:59
    
    stmt = """select tm, ivsc, tm - ivsc from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs4')
    #  expect 3 rows with the following values:
    #     14:30:22  14:30:21
    #     00:00:00  23:59:01
    #     23:59:59  23:59:59
    
    stmt = """select tm, tm - interval '40' hour from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs5')
    #  expect 3 rows with the following values:
    #     14:30:22  22:30:22
    #     00:00:00  08:00:00
    #     23:59:59  07:59:59
    
    #  subtract 24 hours of minutes + 1
    stmt = """select tm, tm - interval '1441' minute (4) from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs6')
    #  expect 3 rows with the following values:
    #  	14:30:22  14:29:22
    #  	00:00:00  23:59:00
    #  	23:59:59  23:58:59
    
    #  subtract 24 hours of seconds + 1
    stmt = """select tm, tm - interval '86401' second (5) from dtarit2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003cexp""", 'a003cs7')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL + INTERVAL => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     +    interval     interval
    #       +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s0')
    
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 1997    06    15    12    59    01
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    
    #
    #  SELECT's
    #
    stmt = """select ivyr, ivyr + interval '10' year
from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s1')
    #  expect 3 rows with the following values:
    #  	 1997    2007
    #  	 9999   10009
    #  	   00      10
    
    stmt = """select ivmt, ivmt + interval '10' month
from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s2')
    #  expect 3 rows with values 16, 41, 10
    #       06      16
    #       31      41
    #       00      10
    
    stmt = """select ivdy, ivdy + interval '100' day (3)
from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s3')
    #  expect 3 rows with the following values:
    #       15     115
    #       24     124
    #       00     100
    
    stmt = """select ivhr, ivhr + interval '20' hour
from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s4')
    #  expect 3 rows with the following values:
    #       12      32
    #      -23    - 03
    #
    stmt = """select ivmn, ivmn + interval '1' minute
from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s5')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a005b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  date arithmetic tests: INTERVAL + INTERVAL => INTERVAL
    #
    #        +------------+---+-------------+-----------+
    #         1st operand   op  2nd operand   result
    #        +------------+---+-------------+-----------+
    #          interval     +    interval     interval
    #        +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005bexp""", 'a005bs0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 1997    06    15    12    59    01
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    #
    stmt = """select ivsc, ivsc + interval '1.5' second
from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005bexp""", 'a005bs1')
    # expect 3 rows with the following values:
    #      01      2.5
    #     -59    -57.5
    #      00      1.5
    #
    # UPDATE's
    #
    
    ##expectfile ${test_dir}/a005bexp a005bs1a
    stmt = """update dtarit5 set
IVYR = IVYR + interval '25' year,
IVMT = IVMT + interval '18' month,
IVDY = IVDY + interval '40' day,
IVHR = IVHR + interval '24' hour,
IVMN = IVMN + interval '60' minute,
IVSC = IVSC + interval '3.99' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """select * from dtarit5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005bexp""", 'a005bs2')
    # expect 3 rows with the following values:
    # 	 2022    24    55    36   119    4.990000
    # 	10024    49    64     1     1  -55.010000
    # 	   25    18    40    24    60    3.990000
    
    _testmgr.testcase_end(desc)

def test011(desc="""a006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL - INTERVAL => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     -    interval     interval
    #       +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 1997    06    15    12    59    01
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    #
    #  SELECT's
    #
    stmt = """select ivyr, ivyr - interval '10' year
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s1')
    #  expect 3 rows with the following values:
    #  	 1997    1987
    #  	 9999    9989
    #  	   00  -   10
    
    stmt = """select ivmt, ivmt - interval '10' month
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s2')
    #  expect 3 rows with the following values:
    #       06    - 04
    #       31      21
    #       00    - 10
    
    stmt = """select ivdy, ivdy - interval '100' day (3)
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s3')
    #  expect 3 rows with the following values:
    #       15   -  85
    #       24   -  76
    #       00   - 100
    
    stmt = """select ivhr, ivhr - interval '20' hour
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s4')
    #  expect 3 rows with the following values:
    #       12    - 08
    #      -23    - 43
    #       00    - 20
    
    stmt = """select ivmn, ivmn - interval '1' minute
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s5')
    #  expect 3 rows with the following values:
    #       59      58
    #      -59    - 60
    #       00    - 01
    
    stmt = """select ivsc, ivsc - interval '1.5' second
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s6')
    #  expect 3 rows with the following values:
    #  	  01     0.500000
    #  	 -59  - 60.500000
    #  	  00     1.500000
    #
    #  UPDATE's
    #
    stmt = """select * from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s7')
    #  expect 3 rows with the following values:
    #     IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #     -----  ----  ----  ----  ----  ----------
    #
    #      1997     6    15    12    59    1.000000
    #      9999    31    24   -23   -59  -59.000000
    #         0     0     0     0     0    0.000000
    
    #  XXXXXX this causes a crash
    ##expectfile ${test_dir}/a006exp a006s8
    #$err_msg 8411 " Conversion of Source Type:INTERVAL MINUTE(REC_INT_MINUTE) Source Value:0xFFFF"
    stmt = """update dtarit6 set
IVYR = IVYR - interval '25' year,
IVMT = IVMT - interval '18' month,
IVDY = IVDY - interval '40' day,
IVHR = IVHR - interval '24' hour,
IVMN = IVMN - interval '60' minute,
IVSC = IVSC - interval '3.99' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  XXXXXX commented out because of the crash
    stmt = """select * from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s9')
    
    _testmgr.testcase_end(desc)

def test012(desc="""a006b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL - INTERVAL => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     -    interval     interval
    #       +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 1997    06    15    12    59    01
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    #
    #  SELECT's
    #
    stmt = """select ivyr, ivyr - interval '10' year
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs1')
    #  expect 3 rows with the following values:
    #  	 1997    1987
    #  	 9999    9989
    #  	   00  -   10
    
    stmt = """select ivmt, ivmt - interval '10' month
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs2')
    #  expect 3 rows with the following values:
    #       06    - 04
    #       31      21
    #       00    - 10
    
    stmt = """select ivdy, ivdy - interval '100' day (3)
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs3')
    #  expect 3 rows with the following values:
    #       15   -  85
    #       24   -  76
    #       00   - 100
    
    stmt = """select ivhr, ivhr - interval '20' hour
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs4')
    #  expect 3 rows with the following values:
    #       12    - 08
    #      -23    - 43
    #       00    - 20
    
    stmt = """select ivmn, ivmn - interval '1' minute
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs5')
    #  expect 3 rows with the following values:
    #       59      58
    #      -59    - 60
    #       00    - 01
    
    stmt = """select ivsc, ivsc - interval '1.5' second
from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs6')
    #  expect 3 rows with the following values:
    #  	  01     0.500000
    #  	 -59  - 60.500000
    #  	  00     1.500000
    #
    #  UPDATE's
    #
    stmt = """select * from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs7')
    #  expect 3 rows with the following values:
    #     IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #     -----  ----  ----  ----  ----  ----------
    #
    #      1997     6    15    12    59    1.000000
    #      9999    31    24   -23   -59  -59.000000
    #         0     0     0     0     0    0.000000
    
    #  XXXXXX this causes a crash
    ##expectfile ${test_dir}/a006bexp a006bs8
    #$err_msg 8411 " Conversion of Source Type:INTERVAL MINUTE(REC_INT_MINUTE) Source Value:0xFFFF"
    stmt = """update dtarit6 set
IVYR = IVYR - interval '25' year,
IVMT = IVMT - interval '18' month,
IVDY = IVDY - interval '40' day,
IVHR = IVHR - interval '24' hour,
IVMN = IVMN - interval '60' minute,
IVSC = IVSC - interval '3.99' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    #  XXXXXX commented out because of the crash
    stmt = """select * from dtarit6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006bexp""", 'a006bs9')
    
    _testmgr.testcase_end(desc)

def test013(desc="""a007"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL * NUMBER => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     *    number       interval
    #       +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 2000    10    02    15    60    12
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    
    #  SELECT queries
    #
    stmt = """select ivyr, ivyr * 3
from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s1')
    #  expect 3 rows with the following values:
    #      2000    6000
    #      9999   29997
    #        00      00
    
    stmt = """select ivmt, ivmt * 0
from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s2')
    #  expect 3 rows with the following values:
    #        10    00
    #        31    00
    #        00    00
    
    stmt = """select ivdy, ivdy * 100
from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s3')
    #  expect 3 rows with the following values:
    #       02     200
    #       24    2400
    #       00      00
    
    stmt = """select ivhr, ivhr * 10
from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s4')
    #  expect 3 rows with the following values:
    #       15     150
    #      -23   - 230
    #       00      00
    
    stmt = """select ivmn, ivmn * 7
from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s5')
    
    _testmgr.testcase_end(desc)

def test014(desc="""a007b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL * NUMBER => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     *    number       interval
    #       +------------+---+-------------+-----------+
    #
    # these are bad cases separated from testA007
    #
    
    #  SELECT queries
    #
    stmt = """select * from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007bexp""", 'a007bs0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 2000    10    02    15    60    12
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    
    #
    stmt = """select ivsc, ivsc * 0.02
from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007bexp""", 'a007bs1')
    #  expect 3 rows with the following values:
    #  	  12       0
    #  	 -59     - 1
    #  	   0       0
    
    #  UPDATE queries
    #
    #  these updates cause a crash
    ##expectfile ${test_dir}/a007bexp a007bs2
    #$err_msg 8411 " Conversion of Source Type:INTERVAL YEAR(REC_INT_YEAR) Source Value:0x00000000"
    stmt = """update dtarit7 
set ivyr = ivyr * 1.5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """update dtarit7 
set ivmt = ivmt * 0.5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """update dtarit7 
set ivdy = ivdy * .2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """update dtarit7 
set ivhr = ivhr * .10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """update dtarit7 
set ivmn = ivmn * 0.7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """update dtarit7 
set ivsc = ivsc * 0.10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    # - -- this one writes garbage to the table
    # -
    stmt = """select * from dtarit7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007bexp""", 'a007bs3')
    
    _testmgr.testcase_end(desc)

def test015(desc="""a008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL / NUMBER => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     /    number       interval
    #       +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 2000    10    02    15    60    12
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    
    #  SELECT queries
    #
    stmt = """select ivyr, ivyr / 3
from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s1')
    #  expect 3 rows with the following values:
    #  	 2000                  666
    #  	 9999                 3333
    #  	   00                   00
    
    ##expectfile ${test_dir}/a008exp a008s2
    stmt = """select ivmt, ivmt / 0
from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    #  expect division by 0 error
    
    stmt = """select ivdy, ivdy / .100
from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s3')
    #  expect 3 rows with the following values:
    #       02    20
    #       24   240
    #       00    00
    
    stmt = """select ivhr, ivhr / 10
from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s4')
    #  expect 3 rows with the following values:
    #       15                   01
    #      -23  -                02
    #       00                   00
    
    stmt = """select ivmn, ivmn / 7
from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s5')
    
    _testmgr.testcase_end(desc)

def test016(desc="""a008b"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: INTERVAL / NUMBER => INTERVAL
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         interval     /    number       interval
    #       +------------+---+-------------+-----------+
    #
    # these are bad cases separated from testA008
    #
    
    #  SELECT queries
    
    stmt = """select * from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008bexp""", 'a008bs0')
    #  expect 3 rows with the following values:
    #  	IVYR   IVMT  IVDY  IVHR  IVMN  IVSC
    #  	-----  ----  ----  ----  ----  ----
    #  	 2000    10    02    15    60    12
    #  	 9999    31    24   -23   -59   -59
    #  	   00    00    00    00    00    00
    
    #
    stmt = """select ivsc, ivsc / 0.02
from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008bexp""", 'a008bs1')
    # expect 3 rows with the following values:
    # 	  12     600
    # 	 -59   -2950
    # 	   0       0
    
    # UPDATE queries
    #
    stmt = """update dtarit8 
set ivyr = ivyr / 2.5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    stmt = """update dtarit8 
set ivmt = ivmt / 1.2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    ##expectfile ${test_dir}/a008bexp a008bs2
    #$err_msg 8411 " Conversion of Source Type:INTERVAL DAY(REC_INT_DAY) Source Value:0x0000"
    stmt = """update dtarit8 
set ivdy = ivdy / .2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    ##expectfile ${test_dir}/a008bexp a008bs3
    #$err_msg 8411 " Conversion of Source Type:INTERVAL HOUR(REC_INT_HOUR) Source Value:0x0000"
    stmt = """update dtarit8 
set ivhr = ivhr / .10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """update dtarit8 
set ivmn = ivmn / 0.7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    ##expectfile ${test_dir}/a008bexp a008bs4
    #$err_msg 8411 " Conversion of Source Type:INTERVAL SECOND(REC_INT_SECOND) Source Value:0xFFFFFFFFEE6AA840"
    stmt = """update dtarit8 
set ivsc = ivsc / 0.20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # -
    stmt = """select * from dtarit8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008bexp""", 'a008bs5')
    
    _testmgr.testcase_end(desc)

def test017(desc="""a009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # date arithmetic tests: NUMBER * INTERVAL => NUMBER
    #
    #       +------------+---+-------------+-----------+
    #        1st operand   op  2nd operand   result
    #       +------------+---+-------------+-----------+
    #         number       *    interval      number
    #       +------------+---+-------------+-----------+
    #
    
    stmt = """select * from dtarit9a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s0')
    #  expect 4 rows with the following values
    #  	YR                    MT      DY
    #  	--------------------  ------  -----------
    #  	                   0       0            0
    #  	                   2       2            2
    #  	                   ?       ?            ?
    #  	                  -4      -4           -4
    
    #  SELECT queries
    #
    #  positive
    stmt = """select yr, yr * interval '10' year from dtarit9a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s1')
    #  expect 4 rows with the following values:
    #  	YR                    (EXPR)
    #  	--------------------  -------------------
    #  	                   0                   00
    #  	                   2                   20
    #  	                   ?  ?
    #  	                  -4  -                40
    
    stmt = """select mt, mt * interval '5' month from dtarit9a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s2')
    #  expect 4 rows with the following values:
    #  	MT      (EXPR)
    #  	------  --------
    #  	     0        00
    #  	     2        10
    #  	     ?  ?
    #  	    -4  -     20
    
    stmt = """select dy, dy * interval '20' day from dtarit9a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s3')
    #  expect 4 rows with the following values:
    #     DY           (EXPR)
    #     -----------  -------------
    #               0             00
    #               2             40
    #               ?  ?
    #              -4  -          80
    
    #  arithmetic with negative numbers
    #  select yr, yr * interval '-7' year from dtarit9a;
    #  expect 4 rows with the following values:
    #     YR                    (EXPR)
    #     --------------------  -------------------
    #                        0                   00
    #                        2  -                14
    #                        ?  ?
    #                       -4                   28
    
    #  select mt, mt * interval '-3' month from dtarit9a;
    #  expect 4 rows with the following values:
    #     MT      (EXPR)
    #     ------  --------
    #          0        00
    #          2  -      6
    #          ?  ?
    #         -4        12
    
    #  select dy, dy * interval '-20' day from dtarit9a;
    #  expect 4 rows with the following values:
    #     DY           (EXPR)
    #     -----------  -------------
    #               0             00
    #               2  -          40
    #               ?  ?
    #              -4             80
    
    stmt = """select * from dtarit9b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s4')
    #  expect 4 rows with the following values:
    #  HR                    MN      SC
    #  --------------------  ------  -----------
    #
    #                     0       0            0
    #                     5       5            5
    #                     ?       ?            ?
    #                   -10     -10          -10
    
    #  positive numbers
    stmt = """select hr, hr * interval '10' hour from dtarit9b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s5')
    #  expect 4 rows with the following values:
    #     HR                    (EXPR)
    #     --------------------  -------------------
    #                        0                   00
    #                        5                   50
    #                        ?  ?
    #                      -10  -               100
    
    stmt = """select mn, mn * interval '5' minute from dtarit9b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s6')
    #  expect 4 rows with the following values:
    #     MN      (EXPR)
    #     ------  --------
    #          0        00
    #          5        25
    #          ?  ?
    #        -10  -     50
    
    stmt = """select sc, sc * interval '20' second from dtarit9b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a009exp""", 'a009s7')
    
    #                  End of test case DATARITH
    _testmgr.testcase_end(desc)

