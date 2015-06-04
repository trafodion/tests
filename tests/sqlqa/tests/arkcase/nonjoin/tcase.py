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
    
def test001(desc="""Tests for datetime data types DATE, TIME, and TIMESTAMP"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test001
    # jclear
    # 1997-04-02
    # tests for datetime data types DATE, TIME, and TIMESTAMP
    # with UNI0N, INTERSECT (and EXCEPT).  EXCEPT isn't supported yet
    
    stmt = """create table njtbl11 (
dt date,
tm time,
ts timestamp
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table njtbl12 (
dt date,
tm time,
ts timestamp
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into njtbl11 values (
date '1997-04-02',
time '14:33:30',
timestamp '1997-04-02:14:33:30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl11 values (
date '1997-04-02',
time '14:33:30',
timestamp '1997-04-02:14:33:30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl11 values (
date '1999-12-31',
time '23:59:59',
timestamp '1999-12-31:23:59:59'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl11 values (
date '2000-01-01',
time '01:01:01',
timestamp '2000-01-01:01:01:01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    # expect 4 rows with the following values:
    # 	1997-04-02  14:33:30  1997-04-02 14:33:30.000000
    # 	1997-04-02  14:33:30  1997-04-02 14:33:30.000000
    # 	1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #    2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    
    stmt = """insert into njtbl12 values (
date '1984-11-05',
time '10:30:43',
timestamp '1997-04-02:14:33:30'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl12 values (
date '1999-12-31',
time '23:59:59',
timestamp '1999-12-31:23:59:59'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl12 values (
date '2000-01-01',
time '01:01:01',
timestamp '2000-01-01:01:01:01'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #  expect 3 rows with the following values:
    #  	1984-11-05  10:30:43  1997-04-02 14:33:30.000000
    #  	1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #     2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    
    stmt = """select * from njtbl11 
union
select * from njtbl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #  expect 4 rows with the following values:
    #     1997-04-02  14:33:30  1997-04-02 14:33:30.000000
    #     1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #     2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    #     1984-11-05  10:30:43  1997-04-02 14:33:30.000000
    
    stmt = """select * from njtbl11 
union all
select * from njtbl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #  expect 7 rows with the following values:
    #     1997-04-02  14:33:30  1997-04-02 14:33:30.000000
    #     1997-04-02  14:33:30  1997-04-02 14:33:30.000000
    #     1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #     2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    #     1984-11-05  10:30:43  1997-04-02 14:33:30.000000
    #     1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #     2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    
    stmt = """select * from njtbl11 
intersect
select * from njtbl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 2 rows with the following values:
    #     1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #     2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    
    stmt = """select * from njtbl11 
intersect all
select * from njtbl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 2 rows with the following values:
    #     1999-12-31  23:59:59  1999-12-31 23:59:59.000000
    #     2000-01-01  01:01:01  2000-01-01 01:01:01.000000
    
    stmt = """select * from njtbl11 
except
select * from njtbl12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    
    stmt = """drop table njtbl11 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table njtbl12 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Tests for INTERVAL data types YEAR, MONTH, and DAY"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test002
    # jclear
    # 1997-04-02
    # tests for INTERVAL data types YEAR, MONTH, and DAY
    # with UNI0N, INTERSECT (and EXCEPT). EXCEPT isn't supported yet.
    
    stmt = """create table njtbl21 (
ivy interval year (3),
ivm interval month (5),
ivd interval day (7)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table njtbl22 (
ivy interval year (3),
ivm interval month (5),
ivd interval day (7)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into njtbl21 values (
interval '111' year (3),
interval '11111' month (5),
interval '1111111' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl21 values (
interval '222' year (3),
interval '22222' month (5),
interval '2222222' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl21 values (
interval '222' year (3),
interval '22222' month (5),
interval '2222222' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl21 values (
interval '333' year (3),
interval '33333' month (5),
interval '3333333' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    # expect 4 rows with the following values:
    # 	 111   11111   1111111
    # 	 222   22222   2222222
    #     222   22222   2222222
    #     333   33333   3333333
    
    stmt = """insert into njtbl22 values (
interval '444' year (3),
interval '44444' month (5),
interval '4444444' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl22 values (
interval '222' year (3),
interval '22222' month (5),
interval '2222222' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl22 values (
interval '555' year (3),
interval '55555' month (5),
interval '5555555' day (7)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  expect 3 rows with the following values:
    #      444   44444   4444444
    #      222   22222   2222222
    #      555   55555   5555555
    
    stmt = """select * from njtbl21 
union
select * from njtbl22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #  expect 5 rows with the following values:
    #      222   22222   2222222
    #      444   44444   4444444
    #      555   55555   5555555
    #      111   11111   1111111
    #      333   33333   3333333
    
    stmt = """select * from njtbl21 
union all
select * from njtbl22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #  expect 7 rows with the following values:
    #      111   11111   1111111
    #      222   22222   2222222
    #      222   22222   2222222
    #      333   33333   3333333
    #      444   44444   4444444
    #      222   22222   2222222
    #      555   55555   5555555
    
    stmt = """select * from njtbl21 
intersect
select * from njtbl22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 1 rows with the following values:
    #      222   22222   2222222
    
    stmt = """select * from njtbl21 
intersect all
select * from njtbl22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 2 rows with the following values:
    #      222   22222   2222222
    #      222   22222   2222222
    
    stmt = """select * from njtbl21 
except
select * from njtbl22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    
    stmt = """drop table njtbl21 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table njtbl22 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Tests for INTERVAL data types HOUR, MINUTE, and SECOND"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test003
    # jclear
    # 1997-04-02
    # tests for INTERVAL data types HOUR, MINUTE, and SECOND
    # with UNI0N, INTERSECT (and EXCEPT). Except that EXCEPT isn't supported yet.
    
    stmt = """create table njtbl31 (
ivh interval hour (1),
ivm interval minute (8),
ivs interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table njtbl32 (
ivh interval hour (1),
ivm interval minute (8),
ivs interval second
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into njtbl31 values (
interval '1' hour (1),
interval '11111111' minute (8),
interval '11' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl31 values (
interval '2' hour (1),
interval '22222222' minute (8),
interval '22' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl31 values (
interval '2' hour (1),
interval '22222222' minute (8),
interval '22' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl31 values (
interval '3' hour (1),
interval '33333333' minute (8),
interval '33' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    # expect 4 rows with the following values:
    # 	  1   11111111    0
    # 	  2   22222222    0
    # 	  2   22222222    0
    # 	  3   33333333    0
    
    stmt = """insert into njtbl32 values (
interval '4' hour (1),
interval '44444444' minute (8),
interval '44' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl32 values (
interval '2' hour (1),
interval '22222222' minute (8),
interval '22' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl32 values (
interval '5' hour (1),
interval '55555555' minute (8),
interval '55' second
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #  expect 3 rows with the following values:
    #       4   44444444    0
    #       2   22222222    0
    #       5   55555555    0
    
    stmt = """select * from njtbl31 
union
select * from njtbl32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  expect 5 rows with the following values:
    #  	  4   44444444    0
    #  	  1   11111111    0
    #  	  2   22222222    0
    #  	  3   33333333    0
    #  	  5   55555555    0
    
    stmt = """select * from njtbl31 
union all
select * from njtbl32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #  expect 7 rows with the following values:
    #       1   11111111    0
    #       2   22222222    0
    #       2   22222222    0
    #       3   33333333    0
    #       4   44444444    0
    #       2   22222222    0
    #       5   55555555    0
    
    stmt = """select * from njtbl31 
intersect
select * from njtbl32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 1 row with the following values:
    #  	  2   22222222    0
    
    stmt = """select * from njtbl31 
intersect all
select * from njtbl32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 2 rows with the following values:
    #  	  2   22222222    0
    #  	  2   22222222    0
    
    stmt = """select * from njtbl31 
except
select * from njtbl32;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    
    stmt = """drop table njtbl31 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table njtbl32 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Tests for INTERVAL data types YEAR TO MONTH, DAY TO"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # HOUR, and HOUR TO MINUTE
    # test004
    # jclear
    # 1997-04-02
    # tests for INTERVAL data types YEAR TO MONTH, DAY TO HOUR, and HOUR TO MINUTE
    # with UNI0N, INTERSECT (and EXCEPT). EXCEPT isn't supported yet.
    
    stmt = """create table njtbl41 (
ivy interval year (3) to month,
ivm interval day (5) to hour,
ivd interval hour (9) to minute
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table njtbl42 (
ivy interval year (3) to month,
ivm interval day (5) to hour,
ivd interval hour (9) to minute
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into njtbl41 values (
interval '111-11' year (3) to month,
interval '11111:11' day (5) to hour,
interval '1111111:11' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl41 values (
interval '222-02' year (3) to month,
interval '22222:22' day (5) to hour,
interval '222222222:22' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl41 values (
interval '222-02' year (3) to month,
interval '22222:22' day (5) to hour,
interval '222222222:22' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl41 values (
interval '333-03' year (3) to month,
interval '33333:03' day (5) to hour,
interval '333333333:33' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl41;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    # expect 4 rows with the following values:
    # 	 111-11   11111 11     1111111:11
    # 	 222-02   22222 02   222222222:22
    # 	 222-02   22222 02   222222222:22
    # 	 333-03   33333 03   333333333:33
    
    stmt = """insert into njtbl42 values (
interval '444-04' year (3) to month,
interval '44444:04' day (5) to hour,
interval '444444444:44' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl42 values (
interval '222-02' year (3) to month,
interval '22222:22' day (5) to hour,
interval '222222222:22' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into njtbl42 values (
interval '555-05' year (3) to month,
interval '55555:05' day (5) to hour,
interval '555555555:55' hour (9) to minute
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from njtbl42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #  expect 3 rows with the following values:
    #      444-04   44444 04   444444444:44
    #      222-02   22222 02   222222222:22
    #      555-05   55555 05   555555555:55
    
    stmt = """select * from njtbl41 
union
select * from njtbl42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #  expect 5 rows with the following values:
    #  	 222-02   22222 02   222222222:22
    #  	 111-11   11111 11     1111111:11
    #  	 333-03   33333 03   333333333:33
    #  	 444-04   44444 04   444444444:44
    #  	 555-05   55555 05   555555555:55
    
    stmt = """select * from njtbl41 
union all
select * from njtbl42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #  expect 7 rows with the following values:
    #      111-11   11111 11     1111111:11
    #      222-02   22222 02   222222222:22
    #      222-02   22222 02   222222222:22
    #      333-03   33333 03   333333333:33
    #      444-04   44444 04   444444444:44
    #      222-02   22222 02   222222222:22
    #      555-05   55555 05   555555555:55
    
    stmt = """select * from njtbl41 
intersect
select * from njtbl42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 1 rows with the following values:
    #  	 222-02   22222 02   222222222:22
    
    stmt = """select * from njtbl41 
intersect all
select * from njtbl42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    #  expect 2 rows with the following values:
    #  	 222-02   22222 02   222222222:22
    #  	 222-02   22222 02   222222222:22
    
    stmt = """select * from njtbl41 
except
select * from njtbl42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3022')
    
    stmt = """drop table njtbl41 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table njtbl42 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

