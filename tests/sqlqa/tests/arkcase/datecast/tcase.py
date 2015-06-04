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
    
    # PREUNT
    # johncl
    # 02/11/97
    # set up for the datetime cast() tests
    
    # table tbA001a
    stmt = """create table tbA001a (dt date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA001a AS
select * from tbA001a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tbA001a values
(date '1997-02-11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA001a values
(date '0001-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA001a values
(date '9999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create index idxdt 
on tbA001a (dt);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA001a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s0')
    
    # table tbA001b
    stmt = """create table tbA001b (str char (10)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA001b AS
select * from tbA001b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tbA001b values
('1997-02-11');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA001b values
('0001-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA001b values
('9999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from vwA001b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s1')
    
    stmt = """create index idxstr1b 
on tbA001b (str);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # table tbA002a
    stmt = """create table tbA002a (tm time) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA002a AS
select * from tbA002a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tbA002a values
(time '11:35:29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA002a values
(time '00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA002a values
(time '23:59:59');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """drop index idxtm;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idxtm 
on tbA002a (tm);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA002a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s2')
    
    # table tbA002b
    stmt = """create table tbA002b (str char (8)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA002b AS
select * from tbA002b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tbA002b values
('11:35:29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA002b values
('00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA002b values
('23:59:59');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create index idxstr2b 
on tbA002b (str);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA002b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s3')
    
    # table tbA003a
    stmt = """create table tbA003a (ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA003a AS
select * from tbA003a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tbA003a values
(timestamp '1997-02-11:11:35:29.123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA003a values
(timestamp '0001-01-01:00:00:00.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA003a values
(timestamp '9999-12-31:23:59:59.999999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create index idxts3a 
on tbA003a (ts);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA003a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s4')
    
    # table tbA003b
    stmt = """create table tbA003b (str char (30)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA003b AS
select * from tbA003b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into tbA003b values
('1997-02-11:11:35:29.123000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA003b values
('0001-01-01:00:00:00.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA003b values
('9999-12-31:23:59:59.999999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create index idxstr3b 
on tbA003b (str);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA003b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s5')
    
    # table tbA004a
    stmt = """create table tbA004a (
ivyr        interval year,
ivmn        interval month,
ivdy        interval day,
ivhr        interval hour,
ivmt        interval minute,
--  ivsc        interval second to fraction(6),
ivsc        interval second,
--  ivsc6       interval second to fraction(6)
ivsc6       interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA004a AS
select * from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/a000exp a000s6
    stmt = """insert into tbA004a values (
interval '1997' year(4),
interval '02' month,
interval '11' day,
interval '15' hour,
interval '45' minute,
interval '14' second,
interval '23.123456' second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    stmt = """insert into tbA004a values (
interval '0000' year(4),
interval '00' month,
interval '00' day,
interval '00' hour,
interval '00' minute,
interval '00' second,
interval '00.000000' second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA004a values (
interval - '30' year,
interval - '12' month,
interval - '31' day,
interval - '24' hour,
interval - '60' minute,
interval - '59' second,
interval - '59.999999' second(6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # XXXXXX seconds get lost here
    # select * from vwA004a;
    
    # table tbA005a:
    stmt = """create table tbA005a (
inum integer,
dnum numeric (8,6)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #     dnum decimal (6,6)
    
    stmt = """insert into tbA005a 
values (99, 23.123456);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create view vwA005a AS
select * from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s7')
    
    # table tbA006a:
    stmt = """create table tbA006a (ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA006a AS
select * from tbA006a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from vwA006a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s8')
    
    stmt = """insert into tbA006a 
values (timestamp '1997-02-12:10:30:15.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA006a 
values (timestamp '9999-12-31:23:59:59.999999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into tbA006a 
values (timestamp '0001-01-01:00:00:00.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create index idxts6a 
on tbA006a (ts);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA006a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s9')
    
    # table tbA007a
    stmt = """create table tbA007a (tm time) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA007a AS
select * from tbA007a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from vwA007a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s10')
    
    stmt = """insert into tbA007a values (time '13:49:22.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbA007a values (time '23:59:59.999999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbA007a values (time '00:00:00.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """drop index idxtm;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idxtm 
on tbA007a (tm);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA007a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s12')
    
    # table tbA008a
    stmt = """create table tbA008a (dt date) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwA008a AS
select * from tbA008a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from vwA008a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s13')
    
    stmt = """insert into tbA008a values (date '1997-02-12');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbA008a values (date '9999-12-31');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbA008a values (date '0001-01-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """create index idxdt08 
on tbA008a (dt);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from vwA008a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a000exp""", 'a000s14')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA001
    # johncl
    # 02/11/97
    # Datetime cast() tests:	CAST (DATE AS char (n))
    #				CAST (string AS DATE)
    #
    #
    
    stmt = """select * from vwA001a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s0')
    #  expect 3 rows with the following values:
    #  	1997-02-11
    #  	0001-01-01
    #  	9999-12-31
    
    stmt = """select CAST (dt AS char(10))
from vwA001a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s1')
    #  expect the same 3 values cast as string expressions
    
    stmt = """select * from vwA001b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s2')
    #  expect 3 rows with the following values:
    #  	1997-02-11
    #  	0001-01-01
    #  	9999-12-31
    
    stmt = """select CAST (str AS date)
from vwA001b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001exp""", 'a001s3')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA002
    # johncl
    # 02/11/97
    # Datetime cast() tests:	CAST (TIME AS char (n))
    #				CAST (string AS TIME)
    #
    
    #
    stmt = """select * from vwA002a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s0')
    #  expect 3 rows with the following values:
    #  	11:35:29
    #  	00:00:00
    #  	23:59:59
    
    stmt = """select CAST (tm AS char (10))
from vwA002a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s1')
    #  expect the same 3 values cast as string expressions
    
    stmt = """select * from vwA002b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s2')
    #  expect 3 rows with the following values:
    #  	11:35:29
    #  	00:00:00
    #  	23:59:59
    
    stmt = """select CAST (str AS time)
from vwA002b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a002exp""", 'a002s3')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA003
    # johncl
    # 02/11/97
    # Datetime cast() tests:	CAST (TIMESTAMP AS char (n))
    #	    			CAST (string AS TIMESTAMP)
    #
    #
    
    stmt = """select * from vwA003a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s0')
    #  expect 3 rows with the following values:
    #  	1997-02-11 11:35:29.123000
    #  	0001-01-01 00:00:00.000000
    #  	9999-12-31 23:59:59.999999
    
    stmt = """select CAST (ts AS char (26))
from vwA003a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s1')
    #  expect the same 3 values cast as string expressions
    
    stmt = """select * from vwA003b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s2')
    #  expect 3 rows with the following values:
    #  	1997-02-11:11:35:29.123000
    #  	0001-01-01:00:00:00.000000
    #  	9999-12-31:23:59:59.999999
    
    stmt = """select CAST (str AS timestamp)
from vwA003b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a003exp""", 'a003s3')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA004
    # johncl
    # 02/11/97
    # Datetime cast() tests:
    #          CAST (INTERVAL year AS int)
    #          CAST (INTERVAL month AS int)
    #          CAST (INTERVAL day AS int)
    #          CAST (INTERVAL hour AS int)
    #          CAST (INTERVAL minute AS int)
    #          CAST (INTERVAL second AS int)
    #          CAST (INTERVAL second (6) AS dec(6,2))
    #
    
    #
    stmt = """select * from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s0')
    #  expect 3 rows with the following values:
    #       IVYR  IVMN  IVDY  IVHR  IVMT  IVSC        IVSC6
    #       ----  ----  ----  ----  ----  ----------  --------------
    #
    #       1997     2    11    15    45   14.000000       23.123456
    #          0     0     0     0     0    0.000000        0.000000
    #        -30   -12   -31   -24   -60  -59.000000  -    59.999999
    
    #      ivyr     interval year,
    stmt = """select CAST (ivyr AS int)
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s1')
    #  expect 3 rows with the following values cast as int expressions:
    #              1997
    #                 0
    #               -30
    
    # -     ivmn    interval month,
    stmt = """select CAST (ivmn AS int)
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s2')
    #  expect 3 rows with the following values cast as int expressions:
    #               2
    #               0
    #             -12
    
    # -     ivdy    interval day,
    stmt = """select CAST (ivdy AS int)
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s3')
    #  expect 3 rows with the following values cast as int expressions:
    #              11
    #               0
    #             -31
    
    # -     ivhr    interval hour,
    stmt = """select CAST (ivhr AS int)
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s4')
    #  expect 3 rows with the following values cast as int expressions:
    #              15
    #               0
    #             -24
    
    # -     ivmt    interval minute,
    stmt = """select CAST (ivmt AS int)
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s5')
    #  expect 3 rows with the following values cast as int expressions:
    #              45
    #               0
    #             -60
    
    # -     ivsc    interval second,
    stmt = """select CAST (ivsc AS int)
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s6')
    #  expect 3 rows with the following values cast as int expressions:
    #              14
    #               0
    #             -59
    
    # -     ivsc6   interval second(6)
    stmt = """select CAST (ivsc6 AS dec(6,2))
from tbA004a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a004exp""", 'a004s7')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a005"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA005
    # johncl
    # 02/12/97
    # Datetime cast() tests:
    #          CAST (int AS INTERVAL year)
    #          CAST (int AS INTERVAL month)
    #          CAST (int AS INTERVAL day)
    #          CAST (int AS INTERVAL hour)
    #          CAST (int AS INTERVAL minute)
    #          CAST (int AS INTERVAL second)
    #          CAST (decimal AS INTERVAL second (6))
    #
    
    #
    stmt = """select * from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s0')
    
    stmt = """select CAST (inum as INTERVAL YEAR)
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s1')
    #  expect expression value 99
    
    stmt = """select CAST (inum as INTERVAL month)
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s2')
    #  expect expression value 99
    
    stmt = """select CAST (inum as INTERVAL day)
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s3')
    #  expect expression value 99
    
    stmt = """select CAST (inum as INTERVAL hour)
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s4')
    #  expect expression value 99
    
    stmt = """select CAST (inum as INTERVAL minute)
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s5')
    #  expect expression value 99
    
    stmt = """select CAST (inum as INTERVAL second)
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s6')
    #  expect expression value 99
    
    stmt = """select CAST (dnum as INTERVAL second(6))
from tbA005a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a005exp""", 'a005s7')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a006"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA006
    # johncl
    # 02/12/97
    # datetime cast() tests
    # 	CAST (TIMESTAMP AS DATE)
    # 	CAST (TIMESTAMP AS TIME)
    
    stmt = """select * from vwA006a 
order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s0')
    #  expect 3 rows with the following values in this order:
    #  	0001-01-01 00:00:00.000000
    #  	1997-02-12 10:30:15.123456
    #  	9999-12-31 23:59:59.999999
    
    stmt = """select CAST (ts AS DATE) from vwA006a 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s1')
    #  expect 3 rows with the following values in this order:
    #     0001-01-01
    #     1997-02-12
    #     9999-12-31
    
    stmt = """select CAST (ts AS TIME) from vwA006a 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a006exp""", 'a006s2')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a007"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA007
    # johncl
    # 02/12/97
    # datetime cast() tests:
    #          CAST (TIME AS TIMESTAMP)
    #          CAST (TIME AS DATE)
    
    #
    stmt = """select * from vwA007a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a007exp""", 'a007s0')
    #  expect 3 rows with the following values in any order:
    #  	13:49:22
    #  	23:59:59
    #  	00:00:00
    
    stmt = """select CAST (tm AS TIMESTAMP) from vwA007a 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    #  expect 3 rows with the current date followed by the following
    #  timestamp values in this order:
    #  00:00:00.000000	<-- the date should be the current date
    #  13:49:22.000000	<-- the date should be the current date
    #  23:59:59.000000	<-- the date should be the current date
    
    stmt = """select CAST (tm AS DATE) from vwA007a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a008"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA008
    # johncl
    # 02/12/97
    # datetime cast() tests:
    #          CAST (DATE AS TIME)
    #          CAST (DATE AS TIMESTAMP)
    
    #
    stmt = """select * from vwA008a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s0')
    #  expect 3 rows with the following values in any order:
    #     1997-02-12
    #     9999-12-31
    #     0001-01-01
    
    stmt = """select CAST (dt AS TIMESTAMP) from vwA008a 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a008exp""", 'a008s1')
    #  expect 3 rows with the following values in this order:
    #  	0001-01-01 00:00:00.000000
    #  	1997-02-12 00:00:00.000000
    #  	9999-12-31 00:00:00.000000
    
    stmt = """select CAST (dt AS TIME) from vwA008a 
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4035')
    
    _testmgr.testcase_end(desc)

