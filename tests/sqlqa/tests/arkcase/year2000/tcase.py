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
    
def test001(desc="""Tables for the Year2000 tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # PREUNT
    # johncl
    # 12/03/96
    # tables for the Year2000 tests
    #
    # create catalog;
    # create schema year2k;
    # test001
    
    stmt = """create table datetbl (dt  date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test002
    stmt = """create table date2tbl (dt  date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test003
    stmt = """create table dategt (dt  date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dategt values (
date '2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dategt values (
date '1999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dategt values (
date '1000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dategt values (
null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dategt values (
date '2000-02-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # test004
    stmt = """create table tstbl (ts  timestamp (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test005
    stmt = """create table ts2tbl (ts  timestamp (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test006
    stmt = """create table tsgt (ts  timestamp (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tsgt values (
timestamp '2000-01-01 00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tsgt values (
timestamp '1999-12-31:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tsgt values (
null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tsgt values (
timestamp '2000-01-01 00:00:00.001');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tsgt values (
timestamp '1000-01-01 00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tsgt values (
timestamp '2000-02-29:12:30:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # test007
    stmt = """create table datecast (dt date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table datestr (dtstr varchar (20)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test008
    stmt = """create table tscast (ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tstmpstr (tsstr varchar (30)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test009
    stmt = """create table dow (dt date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dow values (
date '2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dow values (
date '2000-02-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table dowts (ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dowts values (
timestamp '2000-01-01:00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dowts values (
timestamp '2000-02-29 00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table wod (dy int) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test010
    stmt = """create table jtstamp (
dt      date,
jts     largeint
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table control (
dt date,
julnum largeint
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into control values (
date '2000-01-01',
2451544
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into control values (
date '2000-02-29',
2451603
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from control;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a00s0')
    
    # test011
    stmt = """create table minmaxdt (dt date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table minmaxts (ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table control2 (num largeint) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test012
    stmt = """create table leapdt (
dt date
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into leapdt values (
date '1999-02-28'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # test013
    stmt = """create table leapts (
ts timestamp
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into leapts values (
timestamp '1999-01-01:00:00:00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # test014
    stmt = """create table leapyr (
dt date,
ts timestamp
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into leapyr values (
date '1999-03-01',
timestamp '1999-03-01:00:00:00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tbldate (
coldate     DATE
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tbltstmp (
coltstamp     TIMESTAMP
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table dates (				-- test017
num int,
dt  date
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwdates 
as select * from dates;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into dates values
(1, date '1999-12-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dates values
(2, date '1999-12-30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dates values
(3, date '1999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dates values
(4, date '2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dates values
(5, date '2000-01-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dates values
(6, date '2000-01-03');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into dates values
(7, date '2000-01-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create table tmstamp (				-- test018
num int,
ts  timestamp
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwtstamp 
as select * from tmstamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tmstamp values
(1, timestamp '1999-12-29:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tmstamp values
(2, timestamp '1999-12-30:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tmstamp values
(3, timestamp '1999-12-31:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tmstamp values
(4, timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tmstamp values
(5, timestamp '2000-01-02:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tmstamp values
(6, timestamp '2000-01-03:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tmstamp values
(7, timestamp '2000-01-04:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Year 2000 tests: DATE datatype"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test001
    # johncl
    # 11/25/96
    # Year 2000 tests: DATE datatype
    #
    # 1. test adding 1 year to  1999-01-01 to roll over to 2000-01-01
    # 2. test adding 1 month to 1999-12-01 to roll over to 2000-01-01
    # 3. test adding 1 day to   1999-12-31 to roll over to 2000-01-01
    # 4. test subtracting 1 day from   2000-01-01 to roll back to 1999-12-31
    # 5. test subtracting 1 month from 2000-01-31 to roll back to 1999-12-31
    # 6. test subtracting 1 year from  2000-12-31 to roll back to 1999-12-31
    #
    #
    # 1. test adding 1 year to roll over to 2000-01-01
    #
    # start with 1999-01-01
    
    stmt = """insert into datetbl values (date '1999-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 year to get 2000-01-01
    stmt = """update datetbl set
dt = dt + interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    # expect one row with the following value:
    # 	2000-01-01
    
    # cleanup
    stmt = """delete from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 2. test adding 1 month to roll over to 2000-01-01
    #
    # start with 1999-12-01
    stmt = """insert into datetbl values (date '1999-12-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 month to get 2000-01-01
    stmt = """update datetbl set
dt = dt + interval '1' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    # expect one row with the following value:
    # 	2000-01-01
    
    # cleanup
    stmt = """delete from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 3. test adding 1 day to roll over to 2000-01-01
    #
    # start with 1999-12-31
    stmt = """insert into datetbl values (date '1999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 day to get 2000-01-01
    stmt = """update datetbl set
dt = dt + interval '1' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    # expect one row with the following value:
    # 	2000-01-01
    
    #
    # 4. test subtracting 1 day to roll back to 1999-12-31
    #
    # starting with 2000-01-01
    #
    # subtract 1  day to get 1999-12-31
    stmt = """update datetbl set
dt = dt - interval '1' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    # expect one row with the following value:
    # 	1999-12-31
    
    # cleanup
    stmt = """delete from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 5. test subtracting 1 month to roll back to 1999-12-31
    #
    # start with 2000-01-31
    stmt = """insert into datetbl values (date '2000-01-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 1  month to get 1999-12-31
    stmt = """update datetbl set
dt = dt - interval '1' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    # expect one row with the following value:
    # 	1999-12-31
    
    # cleanup
    stmt = """delete from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 6. test subtracting 1 year to roll back to 1999-12-31
    #
    # start with 2000-12-31
    stmt = """insert into datetbl values (date '2000-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 1  year to get 1999-12-31
    stmt = """update datetbl set
dt = dt - interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from datetbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Year 2000 tests: DATE datatype: 60 year rollover and back"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test002
    # johncl
    # 12/02/96
    # Year 2000 tests: DATE datatype: 60 year rollover and back
    #
    # 1. test adding 61 years to 1939-01-01 to roll over to 2000-01-01
    # 2. test adding 721 months to 1999-12-01 to roll over to 2000-01-01
    # 3. test adding 60 years of days to 1939-12-31 to roll over to 2000-01-01
    # 4. subtract 60 years of days from 2000-01-01 to roll back to 1939-12-31
    # 5. subtract 721 months from 2000-01-31 to roll back to 1939-12-31
    # 6. subtract 61 years from 2000-12-31 to roll back to 1939-12-31
    # 7. subtract 60 years of days from 2060-01-01 to roll back to 1999-12-31
    # 8. subtract 721 months from 2060-01-31 to roll back to 1999-12-31
    # 9. subtract 61 years from 2060-12-31 to roll back to 1999-12-31
    #
    #
    # 1. test adding 1 year to roll over to 2000-01-01
    #
    # start with 1939-01-01
    
    stmt = """insert into date2tbl values (date '1939-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 61 years to get 2000-01-01
    stmt = """update date2tbl set
dt = dt + interval '61' year (2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    # expect one row with the following value:
    # 	2000-01-01
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 2. test adding 721 months to roll over to 2000-01-01
    #
    # start with 1939-12-01
    stmt = """insert into date2tbl values (date '1939-12-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 721 months to get 2000-01-01
    stmt = """update date2tbl set
dt = dt + interval '721' month (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    # expect one row with the following value:
    # 	2000-01-01
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 3. test adding 60 years of days to 1939-12-31 to roll over to 2000-01-01
    # There are 15 leap years between 1939 and 2000:
    #     1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968,
    #     1972, 1976, 1980, 1984, 1988, 1992, 1996,
    #	    60 yrs * 365 = 21900 + 15 leap days + 1 day = 21916
    #
    # start with 1939-12-31
    stmt = """insert into date2tbl values (date '1939-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 day to get 2000-01-01
    stmt = """update date2tbl set
dt = dt + interval '21916' day (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    # expect one row with the following value:
    # 	2000-01-01
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 4. subtract 60 years of days from 2000-01-01 to roll back to 1939-12-31
    #
    # start with 2000-01-01
    stmt = """insert into date2tbl values (date '2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    # subtract 1  day to get 1999-12-31
    stmt = """update date2tbl set
dt = dt - interval '21916' day (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    # expect one row with the following value:
    # 	1939-12-31
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 5. subtract 721 months from 2000-01-31 to roll back to 1939-12-31
    #
    # start with 2000-12-31
    stmt = """insert into date2tbl values (date '2000-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #  subtract 721 months to get 1939-12-31
    stmt = """update date2tbl set
dt = dt - interval '721' month (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    # expect one row with the following value:
    # 	1939-12-31
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 6. subtract 61 years from 2000-12-31 to roll back to 1939-12-31
    #
    # start with 2000-12-31
    stmt = """insert into date2tbl values (date '2000-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 61 years to get 1939-12-31
    stmt = """update date2tbl set
dt = dt - interval '61' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    # expect one row with the following value:
    # 	1939-12-31
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 7. subtract 60 years of days from 2060-01-01 to roll back to 1999-12-31
    # There are 16 leap years between 2000 and 2061
    #     2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028,
    #     2032, 2036, 2040, 2044, 2048, 2052, 2056, 2060,
    #	    60 yrs * 365 = 21900 + 16 leap days = 21916
    #
    # start with 2060-01-01
    stmt = """insert into date2tbl values (date '2060-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #
    # subtract 1  day to get 1999-12-31
    stmt = """update date2tbl set
dt = dt - interval '21916' day (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    # expect one row with the following value:
    # 	1999-12-31
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 8. subtract 721 months from 2060-01-31 to roll back to 1999-12-31
    #
    # start with 2060-01-31
    stmt = """insert into date2tbl values (date '2060-01-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 721 months to get 1999-12-31
    stmt = """update date2tbl set
dt = dt - interval '721' month (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    # expect one row with the following value:
    # 	1999-12-31
    
    # cleanup
    stmt = """delete from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 9. subtract 61 yearS from 2060-12-31 to roll back to 1999-12-31
    #
    # start with 2060-12-31
    stmt = """insert into date2tbl values (date '2060-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 61 years to get 1999-12-31
    stmt = """update date2tbl set
dt = dt - interval '61' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from date2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Year 2000 tests: DATE datatype comparison operators"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test003
    # johncl
    # 12/02/96
    # Year 2000 tests: DATE datatype comparison operators
    #
    # 1. test < operator
    # 2. test <= operator
    # 3. test > operator
    # 4. test >= operator
    #
    
    stmt = """select * from dategt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #  expect 5 rows
    #
    #  1. test < operator
    #
    stmt = """select * from dategt 
where dt < date '2000-01-01'
order by dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #  expect 2 rows with the following values in this order:
    #  	1000-01-01
    #  	1999-12-31
    
    #  2. test <= operator
    #
    stmt = """select * from dategt 
where dt <= date '2000-01-01'
order by dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  expect 3 rows with the following values in this order:
    #     1000-01-01
    #     1999-12-31
    #     2000-01-01
    
    #  3. test > operator
    #
    stmt = """select * from dategt 
where dt > date '2000-01-01';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #  expect 1 row with this value:	2000-02-29
    
    #  4. test >= operator
    #
    stmt = """select * from dategt 
where dt >= date '2000-01-01'
order by dt desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    _testmgr.testcase_end(desc)

def test005(desc="""Year 2000 tests. Test the TIMESTAMP datatype."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test004
    # johncl
    # 11/25/96
    # Year 2000 tests
    # test the TIMESTAMP datatype
    #
    # 1. add 1 year to 1999-01-01 00:00:00.000 to get 2000-01-01 00:00:00.000
    # 2. add 1 month to 1999-12-01 00:00:00.00 to get 2000-01-01 00:00:00.000
    # 3. add 1 day to 1999-12-31 00:00:00.000 to get 2000-01-01 00:00:00.000
    # 4. add 1 hour to 1999-12-31:23 00:00.000 to get 2000-01-01 00:00:00.000
    # 5. add 1 minute to 1999-12-31 23:59:00.00 to get 2000-01-01 00:00:00.000
    # 6. add 1 second to 1999-12-31 23:59:59.000 to get 2000-01-01 00:00:00.000
    # 7. add 1 thousandth of a second to 1999-12-31 23:59:59.999
    #    		to get 2000-01-01 00:00:00.000
    # 8. subtract 1 thousandth of a second from 2000-01-01 00:00:00.000
    # 		to get 1999-12-31 23:59:59.999
    # 9. subtract 1 second from 2000-01-01 00:00:00.000
    # 		to get 1999-12-31 23:59:59.000
    # 10. subtract 1 minute from 2000-01-01 00:00:00.000
    #              to get 1999-12-31 23:59:00.000
    # 11. subtract 1 hour from 2000-01-01 00:00:00.000
    #              to get 1999-12-31 23:00:00.000
    # 12. subtract 1 day from 2000-01-01 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    # 13. subtract 1 month from 2000-01-31 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    # 14. subtract 1 year from from 2000-12-31 00:00:00.000
    # 		to get 1999-12-31 00:00:00.000
    # 1. add 1 year to 1999-01-01 00:00:00.000 to make 2000-01-01 00:00:00.000
    #
    # start with 1999-01-01 00:00:00.000
    
    stmt = """insert into tstbl values (timestamp '1999-01-01:00:00:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 year to get 2000-01-01...
    stmt = """update tstbl set
ts = ts + interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 2. add 1 month to 1999-12-01 00:00:00.00 to make 2000-01-01 00:00:00.000
    #
    # start with 1999-12-01:00:00:00.00
    stmt = """insert into tstbl values (timestamp '1999-12-01:00:00:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 month to get 2000-01-01...
    stmt = """update tstbl set
ts = ts + interval '1' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 3. add 1 day to 1999-12-31 00:00:00.000 to make 2000-01-01 00:00:00.000
    #
    # start with 1999-12-31:00:00:00.000
    stmt = """insert into tstbl values (timestamp '1999-12-31:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 day to get 2000-01-01...
    stmt = """update tstbl set
ts = ts + interval '1' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 4. add 1 hour to 1999-12-31:23 00:00.000 to make 2000-01-01 00:00:00.000
    #
    # start with 1999-12-31:23:00:00.000
    stmt = """insert into tstbl values (timestamp '1999-12-31:23:00:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 hour to get 2000-01-01...
    stmt = """update tstbl set
ts = ts + interval '1' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 5. add 1 minute to 1999-12-31 23:59:00.00 to make 2000-01-01 00:00:00.000
    #
    # start with 1999-12-31:23:59:00.00
    stmt = """insert into tstbl values (timestamp '1999-12-31:23:59:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 minute to get 2000-01-01...
    stmt = """update tstbl set
ts = ts + interval '1' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 6. add 1 second to 1999-12-31 23:59:59.000 to make 2000-01-01 00:00:00.000
    #
    # start with 1999-12-31:23:59:59.000
    stmt = """insert into tstbl values (timestamp '1999-12-31:23:59:59.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 second to get 2000-01-01...
    stmt = """update tstbl set
ts = ts + interval '1' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 7. add 1 thousandth of a second to 1999-12-31 23:59:59.999
    #    		to make 2000-01-01 00:00:00.000
    #
    # start with 1999-12-31:23:59:59.999
    stmt = """insert into tstbl values (timestamp '1999-12-31:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 1 thousandth of a second to get 2000-01-01...
    stmt = """update tstbl set
---     ts = ts + interval '00.001' second;
ts = ts + interval '0.001' second (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 8. subtract 1 thousandth from 2000-01-01 00:00:00.000
    #		to get 1999-12-31 23:59:59.999
    #
    # start with 2000-01-01:00:00:00.000
    stmt = """insert into tstbl values (timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 1 thousandth to get 1999-12-31...
    stmt = """update tstbl set
---     ts = ts - interval '00.001' second;
ts = ts - interval '0.001' second (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    # expect one row with the following value:
    # 	1999-12-31 23:59:59.999
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 9. subtract 1 second from 2000-01-01 00:00:00.000
    #		to get 1999-12-31 23:59:59.000
    
    # start with 2000-01-01:00:00:00.000
    stmt = """insert into tstbl values (timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 1 second to get 1999-12-31...
    stmt = """update tstbl set
ts = ts - interval '1' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    # expect one row with the following value:
    # 	1999-12-31 23:59:59.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 10. subtract 1 minute from 2000-01-01 00:00:00.000
    #              to get 1999-12-31 23:59:00.000
    #
    # start with 2000-01-01 00:00:00.000
    stmt = """insert into tstbl values (
timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-01-01 00:00:00.000');		XXXXXX
    
    # subtract 1  minute to get 1999-12-31...
    stmt = """update tstbl set
ts = ts - interval '1' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    # expect one row with the following value:
    # 	1999-12-31 23:59:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 11. subtract 1 hour from 2000-01-01 00:00:00.000
    #              to get 1999-12-31 23:00:00.000
    #
    # start with 2000-01-01 00:00:00.000
    stmt = """insert into tstbl values (
timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-01-01 00:00:00.000');		XXXXXX
    
    # subtract 1  hour to get 1999-12-31...
    stmt = """update tstbl set
ts = ts - interval '1' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    # expect one row with the following value:
    # 	1999-12-31 23:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 12. subtract 1 day from 2000-01-01 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    #
    # start with 2000-01-01 00:00:00.000
    stmt = """insert into tstbl values (
timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-01-01 00:00:00.000');		XXXXXX
    
    # subtract 1  day to get 1999-12-31...
    stmt = """update tstbl set
ts = ts - interval '1' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    # expect one row with the following value:
    # 	1999-12-31 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 13. subtract 1 month from 2000-01-31 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    #
    # start with 2000-01-31 00:00:00.000
    stmt = """insert into tstbl values (
timestamp '2000-01-31:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-01-31 00:00:00.000');		XXXXXX
    
    # subtract 1 month to get 1999-12-31...
    stmt = """update tstbl set
ts = ts - interval '1' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    # expect one row with the following value:
    # 	1999-12-31 00:00:00.000
    
    # cleanup
    stmt = """delete from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 14. subtract 1 year from from 2000-12-31 00:00:00.000
    #		to get 1999-12-31 00:00:00.000
    #
    # start with 2000-12-31 00:00:00.000
    stmt = """insert into tstbl values (
timestamp '2000-12-31:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-12-31 00:00:00.000');		XXXXXX
    
    # subtract 1 year to get 1999-12-31...
    stmt = """update tstbl set
ts = ts - interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tstbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Test the TIMESTAMP datatype: 60 year roll forward and back"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test005
    # johncl
    # 11/25/96
    # Year 2000 tests
    # test the TIMESTAMP datatype: 60 year roll forward and back
    #
    # 1. add 61 years to 1939-01-01 00:00:00.000 to get 2000-01-01 00:00:00.000
    # 2. add 721 months to 1939-12-01 00:00:00.00 to make 2000-01-01 00:00:00.000
    # 3. add 60 years of days to 1939-12-31 00:00:00.000 to get 2000-01-01...
    # 4. add 1 year of hours to 1939-12-31:23 00:00.000 to get 2000-01-01...
    # 5. add 1 year of minutes + 1 to 1998-12-31 23:59:00.00 to make 2000-01-01...
    # 6. add 1 month of seconds + 1 to 1999-12-01 23:59:59.000 to get 2000-01-01...
    # 7. subtract 1 month of seconds from 2000-01-31 23:59:59
    # 		to get 1999-12-31 23:59:59
    # 8. subtract 1 year of minutes from 2000-12-31 23:59:00
    #              to get 1999-12-31 23:59:00
    # 9. subtract 1 year of hours from 2000-12-31 23:00:00.000
    #              to get 1999-12-31 23:00:00.000
    # 10. subtract 60 years of days from 2060-01-01 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    # 11. subtract 721 months from 2060-01-31 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    # 12. subtract 61 years from from 2060-12-31 00:00:00.000
    # 		to get 1999-12-31 00:00:00.000
    
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # 1. add 61 years to 1939-01-01 00:00:00.000 to get 2000-01-01 00:00:00.000
    #
    # start with 1939-01-01 00:00:00.000
    stmt = """insert into ts2tbl values (timestamp '1939-01-01:00:00:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 61 years to get 2000-01-01...
    stmt = """update ts2tbl set
ts = ts + interval '61' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 2. add 721 months to 1939-12-01 00:00:00.00 to make 2000-01-01 00:00:00.000
    #
    # start with 1939-12-01:00:00:00.00
    stmt = """insert into ts2tbl values (timestamp '1939-12-01:00:00:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 721 months to get 2000-01-01...
    stmt = """update ts2tbl set
ts = ts + interval '721' month (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 3. add 60 years of days to 1939-12-31 00:00:00.000 to get 2000-01-01...
    # There are 15 leap years between 1939 and 2000:
    #     1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968,
    #     1972, 1976, 1980, 1984, 1988, 1992, 1996,
    #	    60 yrs * 365 = 21900 + 15 leap days + 1 day = 21916
    #
    # start with 1939-12-31:00:00:00.000
    stmt = """insert into ts2tbl values (
timestamp '1939-12-31:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '1939-12-31 00:00:00');		XXXXXX
    
    # add 21916 days to get 2000-01-01...
    stmt = """update ts2tbl set
ts = ts + interval '21916' day (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 4. add 1 year of hours to 1999-01-01:23 00:00.000 to get 2000-01-01...
    #
    # start with 1999-01-01 00:00:00.000
    stmt = """insert into ts2tbl values (timestamp '1999-01-01:00:00:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 8760 hour to get 2000-01-01...
    stmt = """update ts2tbl set
ts = ts + interval '8760' hour (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 5. add 1 year of minutes + 1 to 1998-12-31 23:59:00.00 to make 2000-01-01...
    #
    # start with 1998-12-31:23:59:00.00
    stmt = """insert into ts2tbl values (timestamp '1998-12-31:23:59:00.00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 525600 + 1 minutes to get 2000-01-01...
    stmt = """update ts2tbl set
ts = ts + interval '525601' minute (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 6. add 1 month of seconds + 1 to 1999-12-01 23:59:59.000 to get 2000-01-01...
    #	30 days x 24 hours x 60 mins x 60 secs + 1 = 2592001
    #
    # start with 1999-12-01:23:59:59.000
    stmt = """insert into ts2tbl values (timestamp '1999-12-01:23:59:59.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # add 2592001 seconds to get 2000-01-01...
    stmt = """update ts2tbl set
ts = ts + interval '2592001' second(7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    # expect one row with the following value:
    # 	2000-01-01 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 7. subtract 1 month of seconds from 2000-01-31 23:59:59
    # 		to get 1999-12-31 23:59:59
    #     31 days x 24 hours x 60 mins x 60 secs = 2678400
    #
    # start with 2000-01-31 23:59:59
    stmt = """insert into ts2tbl values (
timestamp '2000-01-31 23:59:59');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # subtract 1 month of seconds to get 1999-12-31...
    stmt = """update ts2tbl set
ts = ts - interval '2678400' second(7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    # expect one row with the following value:
    # 	1999-12-31 23:59:59.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 8. subtract 1 year of minutes from 2000-12-31 23:59:00
    #              to get 1999-12-31 23:59:00
    #	366 days x 24 hours x 60 mins = 527040 minutes
    #
    # start with 2000-12-31 23:59:00
    stmt = """insert into ts2tbl values (
timestamp '2000-12-31:23:59:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-12-31 23:59:00');		XXXXXX
    
    # subtract 527040 minutes to get 1999-12-31...
    stmt = """update ts2tbl set
ts = ts - interval '527040' minute (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    # expect one row with the following value:
    # 	1999-12-31 23:59:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 9. subtract 1 year of hours from 2000-12-31 23:00:00.000
    #              to get 1999-12-31 23:00:00.000
    #	366 days x 24 = 8784
    #
    # start with 2000-12-31 23:00:00.000
    stmt = """insert into ts2tbl values (
timestamp '2000-12-31:23:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-12-31 23:00:00.000');		XXXXXX
    
    # subtract 8784 hours to get 1999-12-31...
    stmt = """update ts2tbl set
ts = ts - interval '8784' hour (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    # expect one row with the following value:
    # 	1999-12-31 23:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 10. subtract 60 years of days from 2060-01-01 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    # There are 15 leap years between 1939 and 2000:
    #     1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968,
    #     1972, 1976, 1980, 1984, 1988, 1992, 1996,
    #          60 yrs * 365 = 21900 + 15 leap days + 1 day = 21916
    #
    # start with 2060-01-01 00:00:00.000
    stmt = """insert into ts2tbl values (
timestamp '2060-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2060-01-01 00:00:00.000');		XXXXXX
    
    # subtract 21916 days to get 1999-12-31...
    stmt = """update ts2tbl set
ts = ts - interval '21916' day (5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    # expect one row with the following value:
    # 	1999-12-31 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 11. subtract 721 months from 2060-01-31 00:00:00.000
    #              to get 1999-12-31 00:00:00.000
    #
    # start with 2060-01-31 00:00:00.000
    stmt = """insert into ts2tbl values (
timestamp '2060-01-31:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2060-01-31 00:00:00.000');		XXXXXX
    
    # subtract 721 months to get 1999-12-31...
    stmt = """update ts2tbl set
ts = ts - interval '721' month (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    # expect one row with the following value:
    # 	1999-12-31 00:00:00.000
    
    # cleanup
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 12. subtract 61 years from from 2060-12-31 00:00:00.000
    # 		to get 1999-12-31 00:00:00.000
    #
    # start with 2060-12-31 00:00:00.000
    stmt = """insert into ts2tbl values (
timestamp '2060-12-31:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2060-12-31 00:00:00.000');		XXXXXX
    
    # subtract 61 years to get 1999-12-31...
    stmt = """update ts2tbl set
ts = ts - interval '61' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    # expect one row with the following value:
    # 	1999-12-31 00:00:00.000
    #
    stmt = """delete from ts2tbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Test the TIMESTAMP datatype comparison operators"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test006
    # johncl
    # 12/02/96
    # Year 2000 tests
    # test the TIMESTAMP datatype comparison operators
    #
    # 1. test < operator
    # 2. test <= operator
    # 3. test > operator
    # 4. test >= operator
    #
    #
    
    stmt = """select * from tsgt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #  expect 6 rows
    #
    #  1. test < operator
    #
    stmt = """select * from tsgt 
where ts < timestamp '2000-01-01:00:00:00.000'
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #  expect 2 rows with the following values in this order:
    #  	1000-01-01 00:00:00.000
    #  	1999-12-31 23:59:59.999
    
    #  2. test <= operator
    #
    stmt = """select * from tsgt 
where ts <= timestamp '2000-01-01:00:00:00.000'
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #  expect 3 rows with the following values in this order:
    #  	1000-01-01 00:00:00.000
    #  	1999-12-31 23:59:59.999
    #  	2000-01-01 00:00:00.000
    
    #  3. test > operator
    #
    stmt = """select * from tsgt 
where ts > timestamp '2000-01-01:00:00:00.000'
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    #  expect 2 row with the following values:
    #  	2000-01-01 00:00:00.001
    #  	2000-02-29 12:30:00.000
    
    #  4. test >= operator
    #
    stmt = """select * from tsgt 
where ts >= timestamp '2000-01-01:00:00:00.000'
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    _testmgr.testcase_end(desc)

def test008(desc="""Test CAST() on the DATE datatype."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test007
    # johncl
    # 12/02/96
    #
    # test CAST() on the DATE datatype
    
    stmt = """insert into datestr values ('2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into datestr values ('1999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into datestr values ('1000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into datestr values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into datestr values ('2000-02-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from datestr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    stmt = """insert into datecast 
select cast (dtstr as date) from datestr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from datecast 
order by dt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    _testmgr.testcase_end(desc)

def test009(desc="""Test CAST() on the TIMESTAMP datatype."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test008
    # johncl
    # 12/02/96
    #
    # test CAST() on the TIMESTAMP datatype
    
    stmt = """insert into tstmpstr values (
'2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     '2000-01-01:00:00:00');		XXXXXX
    stmt = """insert into tstmpstr values (
'1999-12-31:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tstmpstr values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tstmpstr values (
'2000-01-01:00:00:00.001');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tstmpstr values (
'1000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     '1000-01-01:00:00:00');		XXXXXX
    stmt = """insert into tstmpstr values (
'2000-02-29:12:30:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # -     '2000-02-29:12:30:00');		XXXXXX
    
    stmt = """select * from tstmpstr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """insert into tscast 
select cast (tsstr as timestamp)
from tstmpstr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    # -     select cast (tsstr as timestamp (3))
    # -         from tstmpstr;    XXXXXX
    
    stmt = """select * from tscast 
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    _testmgr.testcase_end(desc)

def test010(desc="""Test the DAYOFWEEK function on DATE & TIMESTAMP types"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test009
    # johncl
    # 11/27/96
    # Year 2000
    # Test the DAYOFWEEK function on DATE & TIMESTAMP types
    # 	Saturday 01-01-2000
    # 	Tuesday 29-02-2000
    #
    # 1. select day of week from a DATE
    # 2. insert day of week from a DATE
    # 3. select day of week from a TIMESTAMP
    # 4. insert day of week from a TIMESTAMP
    #  1. select day of week from a DATE
    
    stmt = """select dayofweek (dt) from dow;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    # expect 2 rows with the values 7 and 3.
    
    #
    # 2. insert day of week from a DATE
    
    stmt = """insert into wod select dayofweek (dt) from dow;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into wod values (dayofweek (date '1999-12-31'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from wod;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #  expect 3 rows with the values 7, 3 and 6.
    
    #
    #  1. select day of week from a TIMESTAMP
    
    stmt = """select dayofweek (ts) from dowts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    # expect 2 rows with the values 7 and 3.
    
    #
    # 2. insert day of week from a TIMESTAMP
    
    stmt = """insert into wod select dayofweek (ts) from dowts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into wod values (dayofweek (date '1999-12-31'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from wod;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    _testmgr.testcase_end(desc)

def test011(desc="""Test the JULIANTIMESTAMP function."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test010
    # johncl
    # 11/27/96
    # Year 2000 tests
    # test the JULIANTIMESTAMP function
    #
    # The Julian number for 1/1/2000 is 2451544
    # The Juliantimestamp for 2000-01-01:00:00:00.000 is
    #	211813444800000000
    # The Julian number for 29/2/2000 is 2451603
    # The Juliantimestamp for 2000-02-29:00:00:00.000 is
    #	211818542400000000
    #
    # 1. insert using juliantimestamp of a date column
    # 2. select using juliantimestamp of a date column
    #
    # 1. insert using juliantimestamp of a date column
    
    stmt = """insert into jtstamp 
select dt, juliantimestamp (dt)
from control;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select * from jtstamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    #  this one fails 12-03-1996
    #  expect 2 rows with the following values:
    #  	2000-01-01      211813444800000000
    #  	2000-02-29      211818542400000000
    
    #  2. select using juliantimestamp of a date column
    stmt = """select juliantimestamp (dt) from jtstamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    
    _testmgr.testcase_end(desc)

def test012(desc="""Test MIN, MAX, AVG and SUM functions on datetime datatypes"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test011
    # johncl
    # 11/27/96
    # Year 2000 tests
    # Test MIN, MAX, AVG and SUM functions on datetime datatypes
    #     1. DATE
    #     2. Timestamp
    #
    #
    
    # The Julian number for 1/1/2000 is 2451544
    # The juliantimestamp for 1/1/2000 is 211813444800000000
    # The Julian number for 29/2/2000 is 2451603
    # The juliantimestamp for 29/2/2000 is 211818542400000000
    # The Julian number for 1/1/1900 is 2415020
    # The juliantimestamp for 1/1/1900 is 208657771200000000
    # The Julian number for 29/2/2004 is 2453064
    # The juliantimestamp for 29/2/2004 is 211944772800000000
    
    stmt = """insert into control2 values (211813444800000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into control2 values (211818542400000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into control2 values (208657771200000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into control2 values (211944772800000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select avg (num) from control2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    #  expect 1 row with the following value:
    # 	  211058632800000000
    
    stmt = """select sum (num) from control2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    # expect 1 row with the following value:
    #	  844234531200000000
    
    #
    #     1. DATE
    #
    stmt = """insert into minmaxdt values (date '2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into minmaxdt values (date '2000-02-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select min (dt) from minmaxdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    #  expect 1 row with the following value:
    #  	2000-01-01
    
    stmt = """select max (dt) from minmaxdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    # expect 1 row with the following value:
    # 	2000-02-29
    
    stmt = """insert into minmaxdt values (date '1900-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into minmaxdt values (date '2004-02-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select min (dt) from minmaxdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #  expect 1 row with the following value:
    #  	1900-01-01
    
    stmt = """select max (dt) from minmaxdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    #  expect 1 row with the following value:
    #  	2004-02-29
    
    #  Try AVG & SUM functions
    
    stmt = """select avg (juliantimestamp (dt)) from minmaxdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #  expect 1 row with the following value:
    # 	  211058632800000000
    
    stmt = """select sum (juliantimestamp (dt)) from minmaxdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    # expect 1 row with the following value:
    #	  844234531200000000
    
    #
    # 2. TIMESTAMP
    
    stmt = """insert into minmaxts values (
timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into minmaxts values (
timestamp '2000-02-29:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select min (ts) from minmaxts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    #  expect 1 row with the following value:
    #  	2000-01-01 00:00:00.000000
    
    stmt = """select max (ts) from minmaxts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    # expect 1 row with the following value:
    # 	2000-02-29 00:00:00.000000
    
    stmt = """insert into minmaxts values (
timestamp '1900-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into minmaxts values (
timestamp '2004-02-29:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select avg (juliantimestamp (ts)) from minmaxts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s10')
    #  this one fails 12-03-1996
    #  expect 1 row with the following value:
    # 	  211058632800000000
    
    stmt = """select sum (juliantimestamp (ts)) from minmaxts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s11')
    
    _testmgr.testcase_end(desc)

def test013(desc="""Year 2000 tests: 2000 as leapyear. Data type DATE."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test012
    # johncl
    # 11/26/96
    #
    # Year 2000 tests: 2000 as leapyear
    # data type DATE
    #
    # 1. span normal year to leap year: 1999 to 29th Feb 2000
    #    a) forwards: add 365+1 days to Feb 28 1999 to get Feb 29 2000
    #    b) backwards: subtract 1 year from Feb 29 2000 to get Feb 28 1999
    #
    # 2. span normal year to leap year: 1999 to 29th Feb 2000
    #    a) forwards: add 365 days to Mar 1 1999 to get Feb 29 2000
    #    b) backwards: subtract 365+1 days from Feb 29 2000 to get Feb 28 1999
    #
    # 3. span 2 leap years: 28th Feb to @9th Feb 2004
    #    a) forwards: add 5 years + 2 days to 1999-02-28 to get Feb 29 2004
    #    b) backwards: subtract 5 years + 2 days from 2004-02-29 to get Feb 28 1999
    #
    # 4. span the extra day: 20th Jan to 31st Dec 2000 spans the extra day
    #    a) forwards: add 346 days to 20th Jan 2000 to produce 31st Dec 2000.
    #    b) backwards: subtract 344 days from 31st Dec to produce Jan 20th 2000
    #
    # 1a. add 366 days to Mar 1 1999
    
    stmt = """update leapdt set
dt = dt + interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    #  expect 1 row with the following values:
    #  	2000-02-29
    
    #  1b. subtract 1 year from Feb 29 2000
    stmt = """update leapdt set
dt = dt - interval '1' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8416')
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    # expect 1 row with the following values:
    # 	1999-02-28
    # BUG: it actually gets 2000-02-29 (no change)
    
    stmt = """delete from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 2a. add 365 days to Mar 1 1999
    
    stmt = """insert into leapdt values (
date '1999-03-01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapdt set
dt = dt + interval '365' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    # expect 1 row with the following values:
    # 	2000-02-29
    
    # 2b. subtract 366 days from Feb 29 2000
    stmt = """update leapdt set
dt = dt - interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    # expect 1 row with the following values:
    # 	1999-02-28  1999-02-28 00:00:00.000000
    
    #
    # 3a. add 5 years + 2 days to 1999-02-28 to get Feb 29 2004
    stmt = """update leapdt set
dt = dt + interval '366' day (3)	-- to 2000 (leap year)
+ interval '365' day (3)	-- to 2001
+ interval '365' day (3)	-- to 2001
+ interval '365' day (3)	-- to 2001
+ interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # to 2001 (leap year)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    # expect 1 row with the following values:
    # 	2004-02-29
    
    # 3b. subtract 5 years + 2 days from 2004-02-29 to get Feb 28 1999
    stmt = """update leapdt set
dt = dt - interval '1827' day (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    # expect 1 row with the following values:
    # 	1999-02-28
    
    stmt = """delete from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 4a. add 346 days to 20th Jan 2000 to produce 31st Dec 2000.
    stmt = """insert into leapdt values (
date '2000-01-20'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapdt set
dt = dt + interval '346' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    # expect 1 row with the following value:
    # 	2000-12-31
    
    # 4b. subtract 344 days from 31st Dec to produce Jan 20th 2000
    stmt = """update leapdt set
dt = dt - interval '346' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapdt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    
    _testmgr.testcase_end(desc)

def test014(desc="""Year 2000 tests: 2000 as leapyear. Data type TIMESTAMP."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test013
    # johncl
    # 11/26/96
    #
    # Year 2000 tests: 2000 as leapyear
    # data type TIMESTAMP
    #
    # 1 - 7 span normal year to leap year: 1999 to 29th Feb 2000
    #		backwards & forwards
    # 1a. add 1 year + 1 month + 28 days to 1999-01-01  to get Feb 29 2000
    #  b. subtract 424 days from Feb 29 2000
    # 2a. add 13 months to 1999-01-29 to get 2000-02-29
    #  b. subtract 13 months from 2000-02-29 to get 1999-01-29
    # 3a. add 1 year & 1 day to 1999-02-28 to get 2000-02-29
    #  b. subtract 1 year & 1 day from 2000-02-29 to get 1999-02-28
    # 4a. add 1 year + 1 hour to 1999-02-28 23:00:00 to get 2000-02-29
    #  b. subtract 1 year + 1 hour from 2000-02-29 to get 1999-02-28 23:00:00
    # 5a. add 1 year + 1 minute to 1999-02-28 23:59:00 to get 2000-02-29
    #  b. subtract 1 year + 1 minute from 2000-02-29 to get 1999-02-28 23:59:00
    # 6a. add 1 year + 1 second to 1999-02-28 23:59:59.000 to get 2000-02-29
    #  b. subtract 1 year + 1 second from 2000-02-29 to get 1999-02-28 23:59:59.000
    # 7a. add 1 year + 1 thousandth of a second to 1999-02-28 23:59:59.999
    #              to get 2000-02-29
    #  b. subtract 1 year + 1 thousandth of a second to 2000-02-29
    #		to get 1999-02-28 23:59:59.999
    #
    # 8 - 12 span normal year from the leap day: 29th Feb 2000 going backwards
    #
    # 8. subtract 1 year from Feb 29 2000 to get Feb 28 1999
    # 9. subtract 12 months from Feb 29 2000
    # 10. subtract 365 & 366 days from 2000-02-29
    # 11. subtract 366 days of hours from 2000-02-29 to get 1999-02-28
    # 12. subtract 366 days of minutes from 2000-02-29 to get 1999-02-28
    #
    # 1997-02-26 removed tests 7a, 7b, 8, & 9 to a separate file because
    #            they fail
    #
    # 1a. add 1 year + 1 month + 28 days (365 + 31 + 28) to 1999-01-01
    # 		to get 2000-02-29
    
    stmt = """update leapts set
ts = ts + interval '424' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    # expect 1 row with the following values:
    # 	2000-02-29 00:00:00.000000
    
    # 1b. subtract 424 days from Feb 29 2000
    stmt = """update leapts set
ts = ts - interval '424' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    # expect 1 row with the following values:
    # 	1999-01-01 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 2a. add 13 months to 1999-01-29 to get 2000-02-29
    
    stmt = """insert into leapts values (
timestamp '1999-01-29:00:00:00.000'
---     timestamp '1999-01-29:00:00:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts + interval '13' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    # expect 1 row with the following values:
    # 	2000-02-29 00:00:00.000000
    
    # 2b. subtract 13 months from 2000-02-29 to get 1999-01-29
    stmt = """update leapts set
ts = ts - interval '13' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    # expect 1 row with the following values:
    # 	1999-01-29 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 3a. add 1 year & 1 day to 1999-02-28 to get 2000-02-29
    
    stmt = """insert into leapts values (
timestamp '1999-02-28:00:00:00.000'
---     timestamp '1999-02-28:00:00:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts + interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    # expect 1 row with the following values:
    # 	2000-02-29 00:00:00.000000
    
    # 3b. subtract 1 year & 1 day from 2000-02-29 to get 1999-02-28
    stmt = """update leapts set
ts = ts - interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
    # expect 1 row with the following values:
    # 	1999-02-28 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 4a. add 1 year + 1 hour to 1999-02-28 23:00:00 to get 2000-02-29
    #	(365 days x 24 hours = 8760 hours)
    
    stmt = """insert into leapts values (
timestamp '1999-02-28:23:00:00.000'
---     timestamp '1999-02-28 23:00:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts + interval '8761' hour (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    # expect 1 row with the following values:
    # 	2000-02-29 00:00:00.000000
    
    # 4b. subtract 1 year + 1 hour from 2000-02-29 to get 1999-02-28 23:00:00
    stmt = """update leapts set
ts = ts - interval '8761' hour (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    # expect 1 row with the following values:
    # 	1999-02-28 23:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 5a. add 1 year + 1 minute to 1999-02-28 23:59:00 to get 2000-02-29
    #      (365 days x 24 hours x 60 minutes = 525600 minutes)
    
    stmt = """insert into leapts values (
timestamp '1999-02-28:23:59:00.000'
---     timestamp '1999-02-28 23:59:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts + interval '525601' minute (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
    # expect 1 row with the following values:
    # 	2000-02-29 00:00:00.000000
    
    # 5b. subtract 1 year + 1 minute from 2000-02-29 to get 1999-02-28 23:59:00
    stmt = """update leapts set
ts = ts - interval '525601' minute (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s9')
    # expect 1 row with the following values:
    # 	1999-02-28 23:59:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 6a. add 1 year + 1 second to 1999-02-28 23:59:59.000 to get 2000-02-29
    # (365 days x 24 hours x 60 minutes x 60 seconds = 31536000 seconds)
    
    stmt = """insert into leapts values (
timestamp '1999-02-28:23:59:59.000'
---     timestamp '1999-02-28 23:59:59'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts + interval '31536001' second (8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s10')
    # expect 1 row with the following values:
    # 	2000-02-29 00:00:00.000000
    
    # 6b. subtract 1 year + 1 second from 2000-02-29 to get 1999-02-28 23:59:59.000
    stmt = """update leapts set
ts = ts - interval '31536001' second (8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s11')
    # expect 1 row with the following values:
    # 	1999-02-28 23:59:59.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # tests 7a, 7b, 8 & 9 moved to test013b
    #
    #
    # 10. subtract 365 & 366 days from 2000-02-29
    
    stmt = """insert into leapts values (
timestamp '2000-02-29:00:00:00.000'
---     timestamp '2000-02-29 00:00:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts - interval '365' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s12')
    # expect 1 row with the following values:
    # 	1999-03-01 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """insert into leapts values (
timestamp '2000-02-29:00:00:00.000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts - interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s13')
    # expect 1 row with the following values:
    # 	1999-02-28 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 11. subtract 366 days of hours from 2000-02-29 to get 1999-02-28
    #	(366 x 24 hours = 8784 hours)
    
    stmt = """insert into leapts values (
timestamp '2000-02-29:00:00:00.000'
---     timestamp '2000-02-29 00:00:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts - interval '8784' hour (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s14')
    # expect 1 row with the following values:
    # 	1999-02-28 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 12. subtract 366 days of minutes from 2000-02-29 to get 1999-02-28
    #	(366 x 24 x 60 mins = 527040 minutes)
    
    stmt = """insert into leapts values (
timestamp '2000-02-29:00:00:00.000'
---     timestamp '2000-02-29 00:00:00'		XXXXXX
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update leapts set
ts = ts - interval '527040' minute (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s15')
    # expect 1 row with the following values:
    # 	1999-02-28 00:00:00.000000
    
    stmt = """delete from leapts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test015(desc="""Year 2000 tests: 2000 as leapyear. DATE and TIMESTAMP"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test014
    # johncl
    # 11/26/96
    #
    # Year 2000 tests: 2000 as leapyear
    # data types DATE and TIMESTAMP
    #
    # 1. span normal year to leap year: 1999 to 29th Feb 2000
    #    forwards: add 365 days to Mar 1 1999 to get Feb 29 2000
    #    backwards: subtract 365+1 days from Feb 29 2000 to get Feb 28 1999
    #
    # 2. span 2 leap years: 28th Feb to @9th Feb 2004
    #    forwards: add 5 years + 2 days to 1999-02-28 to get Feb 29 2004
    #    backwards: subtract 5 years + 2 days from 2004-02-29 to get Feb 28 1999
    #
    # 3. span the extra day: 20th Jan to 31st Dec 2000 spans the extra day
    #    forwards: add 346 days to 20th Jan 2000 to produce 31st Dec 2000.
    #    backwards: subtract 344 days from 31st Dec to produce Jan 20th 2000
    #
    # 1a. add 365 days to Mar 1 1999
    
    stmt = """update leapyr set
dt = dt + interval '365' day (3),
ts = ts + interval '365' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    # expect 1 row with the following values:
    # 	2000-02-29  2000-02-29 00:00:00.000000
    
    # 1b. subtract 366 days from Feb 29 2000
    stmt = """update leapyr set
dt = dt - interval '366' day (3),
ts = ts - interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    # expect 1 row with the following values:
    # 	1999-02-28  1999-02-28 00:00:00.000000
    
    #
    # 2a. add 5 years + 2 days to 1999-02-28 to get Feb 29 2004
    stmt = """update leapyr set
dt = dt + interval '366' day (3)	-- to 2000 (leap year)
+ interval '365' day (3)	-- to 2001
+ interval '365' day (3)	-- to 2001
+ interval '365' day (3)	-- to 2001
+ interval '366' day (3),	-- to 2001 (leap year)
ts = ts + interval '366' day (3)
+ interval '365' day (3)
+ interval '365' day (3)
+ interval '365' day (3)
+ interval '366' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    # expect 1 row with the following values:
    # 	2004-02-29  2004-02-29 00:00:00.000000
    
    # 2b. subtract 5 years + 2 days from 2004-02-29 to get Feb 28 1999
    stmt = """update leapyr set
dt = dt - interval '1827' day (4),
ts = ts - interval '1827' day (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    # expect 1 row with the following values:
    # 	1999-02-28  1999-02-28 00:00:00.000000
    
    stmt = """delete from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #
    # 3a. add 346 days to 20th Jan 2000 to produce 31st Dec 2000.
    stmt = """insert into leapyr values (
date '2000-01-20',
timestamp '2000-01-20:00:00:00.000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #-     timestamp '2000-01-20:00:00:00'		XXXXXX
    
    stmt = """update leapyr set
dt = dt + interval '346' day (3),
ts = ts + interval '346' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    # expect 1 row with the following values:
    # 	2000-12-31  2000-12-31 00:00:00.000000
    
    # 3b. subtract 344 days from 31st Dec to produce Jan 20th 2000
    stmt = """update leapyr set
dt = dt - interval '346' day (3),
ts = ts - interval '346' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from leapyr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    
    _testmgr.testcase_end(desc)

def test016(desc="""Tests sorting datatype DATE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test015
    # johncl
    # 12/04/96
    # Year 2000 tests
    # Tests sorting datatype DATE
    # 	insert 84 random dates from 1950 - 2050
    #	select with order by
    #	select with order by ascending
    #	select with order by descending
    # insert 84 rows
    
    stmt = """insert into tbldate values (date '1964-09-18');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2010-07-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1973-01-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2018-11-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1954-10-07');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1963-02-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2035-08-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1971-06-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2043-12-06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1979-10-14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2052-04-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1988-02-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1950-08-10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1996-06-18');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1958-12-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2004-10-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1967-04-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2013-02-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1975-08-17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2021-06-25');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2029-10-27');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1992-04-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2038-02-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2000-08-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2046-07-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2008-12-25');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2054-11-03');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2017-04-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1953-03-06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2025-08-30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1961-07-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2034-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1969-11-09');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2042-05-05');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1978-03-13');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2050-09-06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1986-07-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1994-11-16');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2040-09-24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2003-03-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2049-01-26');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1978-10-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2051-04-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1987-02-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2000-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1949-08-16');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1995-06-25');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1957-12-18');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2003-10-27');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1966-04-21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2012-02-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1974-08-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2020-07-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1982-12-25');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1991-04-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2037-03-06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1999-08-30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2045-07-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2008-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2053-11-09');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2016-05-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1952-03-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2024-09-05');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2000-02-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1960-07-14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2033-01-07');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1968-11-15');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2041-05-11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1977-03-19');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2049-09-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1948-01-14');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1993-11-22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1956-05-17');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2002-03-26');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1964-09-18');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2010-07-28');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1973-01-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2018-11-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1954-10-07');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2027-04-02');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1963-02-08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '2035-08-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbldate values (date '1971-06-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count (*) from tbldate;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    #  expect count = 84
    
    stmt = """select * from tbldate 
where coldate >  date '1989-12-31'
and coldate <= date '2001-01-01'
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    #  expect 11 rows with the following values in this order:
    #  	1991-04-28
    #  	1992-04-21
    #  	1993-11-22
    #  	1994-11-16
    #  	1995-06-25
    #  	1996-06-18
    #  	1999-08-30
    #  	1999-12-31
    #  	2000-01-01
    #  	2000-02-29
    #  	2000-08-23
    
    stmt = """select * from tbldate 
where coldate >= date '1989-12-31'
and coldate <  date '2010-01-01'
order by coldate desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    #  expect 17 rows with the following values in this order:
    #     2008-12-25
    #     2008-01-01
    #     2004-10-20
    #     2003-10-27
    #     2003-03-20
    #     2002-03-26
    #     2000-08-23
    #     2000-02-29
    #     2000-01-01
    #     1999-12-31
    #     1999-08-30
    #     1996-06-18
    #     1995-06-25
    #     1994-11-16
    #     1993-11-22
    #     1992-04-21
    #     1991-04-28
    
    stmt = """select count (*) from tbldate 
where coldate >= date '2000-01-01'
ORDER BY 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    # ORDER BY is intentional
    #  expect count = 42
    
    stmt = """select count (*) from tbldate 
where coldate  < date '2000-01-01'
ORDER BY 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    
    _testmgr.testcase_end(desc)

def test017(desc="""Tests sorting datatype TIMESTAMP"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test016
    # johncl
    # 12/04/96
    # Tests sorting datatype TIMESTAMP
    #      insert 84 random timestamps from 1950 - 2050
    #      select with order by
    #      select with order by ascending
    #      select with order by descending
    # insert 84 rows
    
    stmt = """insert into tbltstmp values (
timestamp '2054-11-03:07:04:05.486');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2017-04-28:21:33:10.739');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1953-03-06:18:02:07.992');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2025-08-30:10:31:04.893');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1961-07-08:04:00:01.146');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2034-01-01:23:29:58.399');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2042-05-05:09:27:52.905');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1978-03-13:01:56:57.158');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2050-09-06:20:25:54.059');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1986-07-15:12:54:51.312');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1949-01-07:06:23:48.565');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1994-11-16:23:52:45.818');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2040-09-24:17:21:42.071');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2003-03-20:09:50:39.324');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2049-01-26:03:19:36.577');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1978-10-20:06:35:04.573');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2051-04-15:00:04:01.474');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1987-02-21:17:33:58.727');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1949-08-16:11:02:55.980');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1995-06-25:03:31:52.233');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1957-12-18:22:00:57.486');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2003-10-27:14:29:54.739');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2012-02-28:00:27:48.893');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1974-08-23:19:56:45.146');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2020-07-01:11:25:42.399');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1982-12-25:05:54:39.652');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2028-11-02:22:23:44.905');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1991-04-28:16:52:41.158');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2037-03-06:08:21:38.059');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1999-08-30:02:50:35.312');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2000-02-29:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2045-07-08:19:19:32.565');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2008-01-01:13:48:29.818');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2053-11-09:07:17:26.071');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2016-05-04:22:46:23.324');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1952-03-12:18:15:28.225');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2024-09-05:10:44:25.478');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1960-07-14:04:13:22.731');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1968-11-15:15:11:16.237');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2041-05-11:07:40:13.490');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1977-03-19:01:09:10.391');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2049-09-12:18:38:15.644');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1985-07-21:12:07:12.897');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1948-01-14:04:36:09.150');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1993-11-22:23:05:06.403');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1956-05-17:15:34:03.656');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2002-03-26:09:03:00.909');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1964-09-18:01:32:57.810');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2010-07-28:20:01:02.063');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1973-01-20:12:30:59.316');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2018-11-29:06:59:56.569');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2000-01-01:00:00:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1954-10-07:23:28:53.822');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2027-04-02:17:57:50.075');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2035-08-04:03:55:44.229');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1999-12-31:23:59:59.999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1971-06-12:20:24:49.482');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2043-12-06:14:53:46.735');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1979-10-14:08:22:43.988');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2052-04-08:00:51:40.241');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1988-02-15:19:20:37.142');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1950-08-10:11:49:34.395');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1996-06-18:05:18:31.648');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1958-12-12:22:47:36.901');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2004-10-20:16:16:33.154');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1967-04-15:08:45:30.407');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2013-02-21:02:14:27.308');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1975-08-17:19:43:24.561');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2021-06-25:13:12:21.814');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2029-10-27:23:10:23.320');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1992-04-21:16:39:20.573');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2038-02-28:10:08:17.826');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2000-08-23:02:37:14.727');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2046-07-02:21:06:11.980');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2008-12-25:13:35:08.233');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2054-11-03:07:04:05.486');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2017-04-28:20:33:10.739');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1953-03-06:18:02:07.992');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2025-08-30:10:31:04.893');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1961-07-08:04:00:01.146');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2034-01-01:23:29:58.399');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '1969-11-09:15:58:55.652');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2042-05-05:09:27:52.905');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbltstmp values (
timestamp '2050-09-06:20:25:54.059');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count (*) from tbltstmp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    #  expect count = 84
    
    stmt = """select * from tbltstmp 
where coltstamp >  timestamp '1989-12-31:23:59:59.999'
and coltstamp <= timestamp '2001-01-01:00:00:00.00'
order by 1 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    #  expect 11 rows with the following values in this order:
    # 	1991-04-28 16:52:41.158000
    # 	1992-04-21 16:39:20.573000
    # 	1993-11-22 23:05:06.403000
    # 	1994-11-16 23:52:45.818000
    # 	1995-06-25 03:31:52.233000
    # 	1996-06-18 05:18:31.648000
    # 	1999-08-30 02:50:35.312000
    # 	1999-12-31 23:59:59.999000
    # 	2000-01-01 00:00:00.000000
    # 	2000-02-29 00:00:00.000000
    # 	2000-08-23 02:37:14.727000
    
    stmt = """select * from tbltstmp 
where coltstamp >= timestamp '1989-12-31:23:59:59.999'
and coltstamp <  timestamp '2010-01-01:00:00:00.00'
order by coltstamp desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    #  expect 17 rows with the following values in this order:
    #  	2008-12-25 13:35:08.233000
    #  	2008-01-01 13:48:29.818000
    #  	2004-10-20 16:16:33.154000
    #  	2003-10-27 14:29:54.739000
    #  	2003-03-20 09:50:39.324000
    #  	2002-03-26 09:03:00.909000
    #  	2000-08-23 02:37:14.727000
    #  	2000-02-29 00:00:00.000000
    #  	2000-01-01 00:00:00.000000
    #  	1999-12-31 23:59:59.999000
    #  	1999-08-30 02:50:35.312000
    #  	1996-06-18 05:18:31.648000
    #  	1995-06-25 03:31:52.233000
    #  	1994-11-16 23:52:45.818000
    #  	1993-11-22 23:05:06.403000
    #  	1992-04-21 16:39:20.573000
    #  	1991-04-28 16:52:41.158000
    
    stmt = """select count (*) from tbltstmp 
where coltstamp >= timestamp '2000-01-01:00:00:00.000'
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    #  order by is intentional. Expect count = 45 rows
    stmt = """select count (*) from tbltstmp 
where coltstamp  < timestamp '2000-01-01:00:00:00.000'
order by 1 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    
    _testmgr.testcase_end(desc)

def test018(desc="""Tests the CASE statement with the DAYOFWEEK function on DATE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test017.sql
    # jclear
    # 1997-05-01
    # Tests the CASE statement with the DAYOFWEEK function on DATE
    # values in a view spanning the end of 1999 and beginning of 2000.
    #
    
    stmt = """select * from vwdates;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    #  expect 7 rows with the following values:
    #  	1  1999-12-29
    #  	2  1999-12-30
    #  	3  1999-12-31
    #  	4  2000-01-01
    #  	5  2000-01-02
    #  	6  2000-01-03
    #  	7  2000-01-04
    
    stmt = """select dt,
case dayofweek (dt)
when 1 then 'Sunday'
when 2 then 'Monday'
when 3 then 'Tuesday'
when 4 then 'Wednesday'
when 5 then 'Thursday'
when 6 then 'Friday'
when 7 then 'Saturday'
else null
end
from vwdates;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    
    _testmgr.testcase_end(desc)

def test019(desc="""Tests the CASE statement with the DAYOFWEEK function on TIMESTAMP"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test018.sql
    # jclear
    # 1997-05-01
    # Tests the CASE statement with the DAYOFWEEK function on TIMESTAMP
    # values in a view spanning the end of 1999 and beginning of 2000.
    #
    
    stmt = """select * from vwtstamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    #  expect 7 rows with the following values:
    #           1  1999-12-29 23:59:59.999
    #           2  1999-12-30 23:59:59.999
    #           3  1999-12-31 23:59:59.999
    #           4  2000-01-01 00:00:00.000
    #           5  2000-01-02 00:00:00.000
    #           6  2000-01-03 00:00:00.000
    #           7  2000-01-04 00:00:00.000
    
    stmt = """select ts,
case dayofweek (ts)
when 1 then 'Sunday'
when 2 then 'Monday'
when 3 then 'Tuesday'
when 4 then 'Wednesday'
when 5 then 'Thursday'
when 6 then 'Friday'
when 7 then 'Saturday'
else null
end
from vwtstamp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s1')
    
    _testmgr.testcase_end(desc)

