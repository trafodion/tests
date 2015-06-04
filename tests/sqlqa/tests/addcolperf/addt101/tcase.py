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

import time
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
    
def test001(desc="""a01 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a01table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fixed length columns only
    stmt = """create table a01table (
ordering int no default not null
, sma1 smallint
)
store by (ordering);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a01table values (1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # add fixed length column, no default
    stmt = """alter table a01table add column int2 int unsigned;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a01table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a01table values (2,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table (ordering, sma1) values (3, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table values (4,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a01table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s01')
    
    # add a variable length column, default literal
    stmt = """alter table a01table add column int3 int default 3000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a01table (ordering, int2) values (5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a01table values (6,6,6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a01table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s02')
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a02table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fixed length columns only
    stmt = """create table a02table (
ordering int no default not null
, ch1 char(1)
, ch2 char(3) default 'ch2'
, ch3 char(1)
, sma smallint
)
store by (ordering);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a02table values (1,'a','aaa','a', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # default null
    stmt = """alter table a02table add column px2 PIC X(1) default '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a02table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a02table values (2,'b','bbb','b',2,'2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table (ordering, ch1) values (3,'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a02table values (4,'d','ddd','d', 4, '4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a02table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s01')
    
    # add vairable length colum with default
    # default or not should not cause data missing
    stmt = """alter table a02table add column cv1 varchar(1) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a02table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s02')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # verify that adding variable column is not the cause for missing data
    
    stmt = """drop table a03table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fixed length columns only
    stmt = """create table a03table (
ordering int no default not null
, ch1 char(1)
, px1 pic 9(7)v9(2)
)
store by (ordering);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a03table values (1,'a',1.0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # default null
    stmt = """alter table a03table add column cv1 varchar(1) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a03table values (2,'b',2.0,'2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a03table (ordering, px1) values (3,3.0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a03table values (4,'d',4.0,'4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a03table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s01')
    
    # add column with different data type, default null
    stmt = """alter table a03table add column px2 int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a03table (ordering, cv1) values (5, '5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a03table values (6,'f',6.0,'6',6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a03table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s02')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a04table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fixed length columns only
    stmt = """create table a04table (
ordering int no default not null
, ch1 char(1)
, ch2 char(3)
, num numeric(4,2)
, "dec" decimal(2)
)
store by (ordering);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a04table values (1,'a','aaa',1.01,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # try different data type with default value
    stmt = """alter table a04table add column px2 largeint default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from a04table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a04table values (2,'b','bbb',2.02, 2, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a04table (ordering, ch1) values (3,'c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a04table values (4, 'd', 'ddd', 4.04, 4, 4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a04table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s01')
    
    # add variable length column, default null
    stmt = """alter table a04table add column cv1 varchar(1) default 'z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a04table (ordering, "dec", px2) values (5, 5, 5000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into a04table values (6, 'f', 'fff', 6.06, 6, 6,'f');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a04table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s02')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a05table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fixed length columns only
    stmt = """create table a05table (
ordering int no default not null
, ch1 char(1)
)
store by (ordering);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a05table values (1,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # default current_time, null, and literal
    stmt = """alter table a05table add column px2 date default date '2005-12-31';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a05table add column px3 time default current_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a05table add column px4 largeint  default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a05table add column px5 dec(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a05table add column px6 char(3)  default 'ABC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a05table add column px7 interval year to month
default interval '07-07' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a05table add column px8 interval day(4) to second(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a05table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a05table (ordering, ch1, px3, px7) values
(2,'b',time '12:02:22', interval '12-11' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a05table (ordering, px5, px6) values (3,3,'aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a05table values (4,'d',date '2004-01-01',
time '16:00:00', 9000, 4, 'XYZ', interval '04-01' year to month,
interval '04:04:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a05table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 4)
    
    # default null
    stmt = """alter table a05table add column cv1 varchar(8) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s1 from
insert into a05table values (5,'e', date '2006-03-31', time '14:49:30',
9900, 5, 'MVH', interval '06-03' year to month,
interval '05:05:00:00.5534' day(4) to second(4), 'X');"""
    output = _dci.cmdexec(stmt)
    # explain s1;
    # explain options 'f' s1;
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # should activate pcode
    stmt = """prepare s2 from
insert into a05table (ordering, cv1, px8) values (6, 'row_6',
interval '6666:16:20:20.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    # explain s2;
    
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """prepare u1 from
update a05table set cv1 = 'update',
px3 = time '11:48:00',
px2 = date '1988-04-29'
where ordering <= 3;"""
    output = _dci.cmdexec(stmt)
    # explain u1;
    # explain options 'f' u1;
    stmt = """execute u1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare d1 from
delete from a05table where cv1 = 'update' and ch1 is null;"""
    output = _dci.cmdexec(stmt)
    # explain d1;
    # explain options 'f' d1;
    stmt = """execute d1;"""
    output = _dci.cmdexec(stmt)
    
    # px3 in record 6 is undeterministrc during to current_time
    stmt = """select * from a05table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 5)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a06 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Will it make any difference regarding missing data if table started
    # with variable columns only?
    
    stmt = """drop table a06table;"""
    output = _dci.cmdexec(stmt)
    
    # table start with variable columns only
    stmt = """create table a06table (
ordering varchar(1)
, ch1 varchar(2)
, ch2 varchar(3)
, ch3 varchar(4)
)
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a06table values ('1','a','aa','aaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # add fixed length column, default null
    stmt = """alter table a06table add column px1 PIC X(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a06table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a06table values ('2','b','bb','bbb','2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a06table (ordering, ch3) values ('3','c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a06table values ('4','d','dd','ddd','4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a06table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s01')
    
    # add variable column, default null
    stmt = """alter table a06table add column cv1 varchar(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a06table (ch3, cv1) values ('f', '5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a06table values ('6','g','gg','ggg','6','6');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """alter table a06table add column cv2 varchar(3) default 'DBA';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a06table (ch3,cv2) values ('h','ZZZ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a06table (ch3,px1) values ('i','8');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a06table values ('9','j','jj','jjj','9','9','JJJ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a06table order by ordering,cv2,cv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s02')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a07 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # What if add variable column, fixed column, then variable column -
    # will data missing?
    # start table with variable columns, then add variable column, fix
    # column
    
    stmt = """drop table a07table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with variable columns only
    stmt = """create table a07table (
ordering varchar(1) default 'z'
, ch1 varchar(1)
)
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a07table values ('1','a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # add variable column, default null
    stmt = """alter table a07table add column cv1 varchar(1) default 'z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select * from a07table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a07table values ('2','b','2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a07table (ordering, ch1) values ('3','c');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a07table values ('4','d','4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a07table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s01')
    
    stmt = """alter table a07table add column px1 PIC X(1) default '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a07table (cv1,px1) values ('5','5');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into a07table values ('6','e','6','6');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a07table order by ordering;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s02')
    
    stmt = """insert into a07table values ('7','f','7','7');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """select * from a07table order by ordering;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """alter table a07table add cv2 varchar(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a07table (cv2) values ('ZZZ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a07table (cv1,px1) values ('9','9');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a07table order by ordering,cv1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s03')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a08 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # start table with variable columns only, add fix columns, then
    # variable column, and mixture of fix and variable columns
    
    stmt = """drop table a08table;"""
    output = _dci.cmdexec(stmt)
    
    # start table with variable columns only
    stmt = """create table a08table (
vch1 varchar(3)
, vch2 varchar(1)
)
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a08table values ('000','a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """alter table a08table add column px2 date default date '1000-01-31';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a08table add column px3 time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a08table add column px4 largeint default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a08table add column px5 char(3) default 'ABC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a08table add column px6 interval year to month
default interval '01-01' year to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a08table add column px7 interval day(4) to second(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a08table order by vch1,vch2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a08table (vch1, vch2, px2, px4) values
('111','k',date '2006-01-01',111100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a08table (vch1, vch2, px4) values ('222','l',20000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a08table values ('333','m',date '2003-01-01',
time '16:00:00', 6000, 'XYZ', interval '16-01' year to month,
interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a08table order by vch1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s01')
    
    stmt = """alter table a08table add column vch3 varchar(8) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a08table (px2,px3,px4,px5) values
(date '2000-02-28', time '14:24:00', 9000, 'A08');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a08table (vch2,px6,vch3) values
('5', interval '15-05' year to month, 'ZZZ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a08table order by vch1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s02')
    
    stmt = """alter table a08table add column int9 int;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into a08table (vch2, px4) values ('x',5000);"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into a08table (vch1, px2,px5) values ('999',date '1996-03-29','999');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """alter table a08table add column vch4 varchar(3) default 'end';"""
    output = _dci.cmdexec(stmt)
    
    # NE: Missing NULL values after alter add column to a no partition table
    stmt = """select * from a08table order by vch1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s03')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a09 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # start table with variable, then fix columns, add varible column,
    # thn fix columns, then variable column
    
    stmt = """drop table a09table;"""
    output = _dci.cmdexec(stmt)
    
    # table starts with fix and variable columns
    stmt = """create table a09table (
vch1 varchar(3)
, int2 int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table values ('000',1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """alter table a09table add column vch2 varchar(1) default '#';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a09table add column px3 largeint default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a09table add column px4 char(3) default 'ABC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a09table add column px5 interval day(4) to second(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a09table order by vch1,int2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a09table (vch1, px3) values ('111', 111000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a09table (int2, vch2, px4) values (3, 'g', 'GGG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a09table values ('444', 4, '4', 222000, 'XYZ',
interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a09table order by vch1,int2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s01')
    
    stmt = """alter table a09table add column vch3 varchar(8) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a09table values ('555', 5, '5', 555000, '555',
interval '15:15:00:00.5555' day(4) to second(4), 'row_5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a09table (px3, px4, vch2) values (123456, 'PX4','p');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a09table (int2, px5, vch3) values
(6, interval '16:16:00:00.1234' day(4) to second(4), 'VCH3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a09table order by vch1,int2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s02')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a10 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # start table with fix and variable columns, then add fix columns,
    # then varable colums
    # import and rollback
    
    stmt = """drop table a10table;"""
    output = _dci.cmdexec(stmt)
    
    # a10.1: table starts with fix and variable columns
    stmt = """create table a10table (
int1 int
, vch2 varchar(3)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a10table values (1, '000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a10.2:
    stmt = """alter table a10table add column px3 largeint default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a10.3:
    stmt = """alter table a10table add column px4 char(3) default 'ABC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a10.4:
    stmt = """alter table a10table add column px5 interval day(4) to second(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a10table order by int1,vch2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into a10table (vch2, px3) values ('111', 111000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a10table (int1, px4) values (3, 'GGG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a10table values (4, '444', 222000, 'XYZ',
interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a10table order by int1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s01')
    
    # a10.5:
    stmt = """alter table a10table add column vch3 varchar(8) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a10table (px3,px4) values (123456, 'PX4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a10table (int1,px5, vch3) values
(6, interval '16:16:00:00.1234' day(4) to second(4), 'VCH3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a10table order by int1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s02')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(15)
    
    stmt = """insert into a10table (int1,px5, vch3) values
(5, interval '15:15:00:00.1234' day(4) to second(4), 'VCH5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a10table order by int1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s03')
    
    # a10.6:
    # TRAF: DDL in TX is not supported yet.  Move the alter table .. add column out of TX
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """alter table a10table add sma1 smallint unsigned default 65535;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column vch4 varchar(1) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column vch5 varchar(2) default 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # a10.7:
    stmt = """insert into a10table (px3, vch4, sma1) values (10000,'1',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (int1, vch3, px4, vch4) values (11,'row11', '111','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (vch5, px5) values
('12', interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # NE: Missing NULL values after alter add column to a no partition table
    stmt = """select * from a10table order by int1,vch2,sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s04')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # TRAF: DDL in TX is not supported yet.  Drop column to mimic the behavior of rollback.   
    stmt = """alter table a10table drop column sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table drop column vch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table drop column vch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    time.sleep(5)
    
    stmt = """select * from a10table order by int1,vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s03')
    
    # a10.8:
    stmt = """alter table a10table add sma1 smallint unsigned default 65535;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column vch4 varchar(1) default 'X';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column vch5 varchar(2) default 'xx';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a10.9:
    stmt = """insert into a10table (px3, vch4, sma1) values (20000,'2',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (int1, vch3, px4, vch4) values (6,'row11', '222','2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (vch5, px5) values
('22', interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a10.10:
    stmt = """alter table a10table add "Sma1" smallint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column "vch4" varchar(1) default 'z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column "vch4*" varchar(2) default 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column "vch%5" varchar(3) default 'zzz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a10.11:
    stmt = """insert into a10table (px3, vch4, sma1) values (10001,'1',101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (px3, "vch4", "Sma1") values (20000,'2',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (int1, "vch%5", px4, "vch4*") values
(33,'333', '111','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a10table values
(101,'101',10001,'WXY',
interval '101:00:00:00.4444' day(4) to second(4), 'WXY',
1001, 'A', 'aa',-1001,'a','AA','zz2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # NE: Missing NULL values after alter add column to a no partition table
    stmt = """select * from a10table order by int1,vch2,vch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s05')
    
    # a10.12:
    stmt = """alter table a10table add "SQL" numeric(4) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table a10table add column "modify" varchar(6) default 'modify';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a10.13:
    stmt = """insert into a10table ("Sma1", "vch4*", vch5) values
(2002, '%_', 'hh');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a10table ("SQL", sma1, "vch%5", "modify") values
(3003, 30003, 'sql', 'update');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into a10table values
(104,'104',10004,'XXY',
interval '104:00:00:00.4444' day(4) to second(4), 'XXY',
1004, 'D', 'dd',-1004,'d','DD','zz4', 4444, 'second');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # NE: Missing NULL values after alter add column to a no partition table
    stmt = """select * from a10table order by int1,vch2,px3,sma1,vch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s06')
    
    # a10.14:
    stmt = """alter table a10table add "ems" decimal(4,2) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a10table add column col17 pic s9(3) default -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a10table add column col18 pic v9(2) comp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a10table add column col19 varchar(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a10.15:
    stmt = """insert into a10table values
(123,'123',123,'123',interval '123:00:00:00.1111' day(4) to second(4),'123',123,'a','aa',123,'a','aa','aaa',123,'tandem',12.3,-123,0.12,'a'),
(124,'124',124,'124',interval '124:00:00:00.1111' day(4) to second(4),'124',124,'b','bb',124,'b','bb','bbb',124,'compaq',12.4,-124,0.12,'b'),
(125,NULL,125,NULL,NULL,'125',125,'c','cc',125,'c','cc','ccc',125,NULL,12.4,-125,0.12,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """invoke a10table;"""
    output = _dci.cmdexec(stmt)
    
    # a10.16:
    # TRAF: DDL in TX is not supported yet.  Move the alter table .. add column out of TX
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """alter table a10table add column col20 varchar(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """insert into a10table ("ems", "SQL", col17) values
(12.60, 126, -126);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into a10table (int1, vch5, col17, col19, col20)
values (130, 'zz', -130, 'z', 'z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # NE: Missing NULL values after alter add column to a no partition table
    stmt = """select * from a10table order by int1,vch2,px3,sma1,vch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s07')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # TRAF: DDL in TX is not supported yet.  Drop column to mimic the behavior of rollback.   
    stmt = """alter table a10table drop column col20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    time.sleep(5)
    
    # a10.17:
    stmt = """insert into a10table values
(127,NULL,NULL,'127',interval '127:00:00:00.1111' day(4) to second(4),'127',127,'e','ee',127,'e','ee','eee',127,'compaq',12.7,-127,NULL,'e'),
(128,NULL,128,NULL,NULL,'128',128,'f','ff',128,'f','ff','fff',128,NULL,12.4,-128,NULL,NULL),
(129,'129',129,'129',interval '129:00:00:00.1111' day(4) to second(4),'129',129,'g','gg',129,'g','gg','ggg',129,'oracle',12.6,-129,0.26,'g');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """insert into a10table (int1, vch5, col17, col19)
values (131, 'xx', -131, 'x');"""
    output = _dci.cmdexec(stmt)
    
    # NE: Missing NULL values after alter add column to a no partition table
    stmt = """select * from a10table order by int1,vch2,px3,sma1,vch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s08')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a11 verify missing data after add variable column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # table starts with fix columns. Add mix columns.
    # rollback command
    # Defaults are:
    # xch2=?, px3=100, px4=ABC, px5=?, vch3=Z,
    # sma1=65535, vch4=X, vch5=xx, Sma1=?, "vch4"=z, "vch4*"=zz, "vch%5"=zzz
    # "SQL"=?, "modify"=modify, "ems"=?, col17=-1, col18=?, col19=?
    
    stmt = """drop table a11table;"""
    output = _dci.cmdexec(stmt)
    
    # a11.1: table starts with fix and variable columns
    stmt = """create table a11table (
int1 int not null not droppable
, xch2  char(3)
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.2:
    stmt = """insert into a11table values (1, '000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.3: add column 1 - fix
    stmt = """alter table a11table add column px3 largeint default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.4: add column 2 - fix
    stmt = """alter table a11table add column px4 char(3) default 'ABC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.5: add column 3 - fix
    stmt = """alter table a11table add column px5 interval day(4) to second(4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    
    # a11.6:
    stmt = """insert into a11table (int1, xch2, px3) values (6, '111', 111000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.7:
    stmt = """insert into a11table (int1, px4) values (7, 'GGG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.8:
    stmt = """insert into a11table values (8, '444', 222000, 'XYZ',
interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s01')
    
    # a11.9: add column 4 - variable
    stmt = """alter table a11table add column vch3 varchar(8) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.10:
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.11:
    stmt = """insert into a11table (int1, px3,px4) values (11, 123456, 'PX4');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # a11.12:
    stmt = """insert into a11table (int1,px5, vch3) values
(12, interval '16:16:00:00.1234' day(4) to second(4), 'VCH3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s02')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    time.sleep(5)
    
    # a11.13:
    stmt = """insert into a11table (int1,px5, vch3) values
(13, interval '15:15:00:00.1234' day(4) to second(4), 'VCH5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    
    # a11.14:
    # TRAF: DDL in TX is not supported yet.  Move the alter table .. add column out of TX
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # a11.15: add column 5 - fix
    stmt = """alter table a11table add sma1 smallint unsigned default 65535;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.16: add column 6 - variable
    stmt = """alter table a11table add column vch4 varchar(1) default 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.17: add column 7 - variable
    stmt = """alter table a11table add column vch5 varchar(2) default 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # a11.18:
    stmt = """insert into a11table (int1, px3, vch4, sma1) values (18,10000,'1',100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.19:
    stmt = """insert into a11table (int1, vch3, px4, vch4) values (19,'row11', '111','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.20:
    stmt = """insert into a11table (int1, vch5, px5) values
(20, '12', interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s04')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # TRAF: DDL in TX is not supported yet.  Drop column to mimic the behavior of rollback.   
    stmt = """alter table a11table drop column sma1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table a11table drop column vch4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """alter table a11table drop column vch5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    time.sleep(5)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s03')
    
    # a11.21: add column 5 - fix
    stmt = """alter table a11table add sma1 smallint unsigned default 65535;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.22: add column 6 - variable
    stmt = """alter table a11table add column vch4 varchar(1) default 'X';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.23: add column 7 - variable
    stmt = """alter table a11table add column vch5 varchar(2) default 'xx';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.24:
    stmt = """insert into a11table (int1, px3, vch4, sma1) values (24, 20000,'2',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.25:
    stmt = """insert into a11table (int1, vch3, px4, vch4) values (25,'row11', '222','2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.26:
    stmt = """insert into a11table (int1, vch5, px5) values
(26, '22', interval '16:16:00:00.1234' day(4) to second(4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.27: add column 8 - fix
    stmt = """alter table a11table add "Sma1" smallint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.28: add column 9 - variable
    stmt = """alter table a11table add column "vch4" varchar(1) default 'z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.29: add column 10 - variable
    stmt = """alter table a11table add column "vch4*" varchar(2) default 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.30: add column 11 - variable
    stmt = """alter table a11table add column "vch%5" varchar(3) default 'zzz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.31:
    stmt = """insert into a11table (int1, px3, vch4, sma1) values (31, 10001,'1',101);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # a11.32:
    stmt = """insert into a11table (int1, px3, "vch4", "Sma1") values (32, 20000,'2',200);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    # a11.33:
    stmt = """insert into a11table (int1, "vch%5", px4, "vch4*") values
(33,'333', '111','X');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.34:
    stmt = """insert into a11table values
(34,'101',10001,'WXY',
interval '101:00:00:00.4444' day(4) to second(4), 'WXY',
1001, 'A', 'aa',-1001,'a','AA','zz2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # expected 12 rows selected
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s05')
    
    # a11.35: add column 12 - fix
    stmt = """alter table a11table add "SQL" numeric(4) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.36: add column 13 - variable
    stmt = """alter table a11table add column "modify" varchar(6) default 'modify';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.37:
    stmt = """insert into a11table (int1, "Sma1", "vch4*", vch5) values
(37,2002, '%_', 'hh');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.38:
    stmt = """insert into a11table (int1, "SQL", sma1, "vch%5", "modify") values
(38, 3003, 30003, 'sql', 'update');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.39:
    stmt = """insert into a11table values
(39,'104',10004,'XXY',
interval '104:00:00:00.4444' day(4) to second(4), 'XXY',
1004, 'D', 'dd',-1004,'d','DD','zz4', 4444, 'second');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s06')
    
    stmt = """select int1, "Sma1", "vch4*", vch5 from a11table where int1 > 35 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s06a')
    
    stmt = """select int1, "SQL", sma1, "vch%5", "modify"
from a11table where int1 > 35 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s06b')
    
    # a11.40: add column 14 - fix
    stmt = """alter table a11table add "ems" decimal(4,2) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.41: add column 15 - fix
    stmt = """alter table a11table add column col17 pic s9(3) default -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.42: add column 16 - fix
    stmt = """alter table a11table add column col18 pic v9(2) comp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.43: add column 17 - variable
    stmt = """alter table a11table add column col19 varchar(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a11.44:
    stmt = """insert into a11table values
(123,'123',123,'123',interval '123:00:00:00.1111' day(4) to second(4),'123',123,'a','aa',123,'a','aa','aaa',123,'tandem',12.3,-123,0.12,'a'),
(124,'124',124,'124',interval '124:00:00:00.1111' day(4) to second(4),'124',124,'b','bb',124,'b','bb','bbb',124,'compaq',12.4,-124,0.12,'b'),
(125,NULL,125,NULL,NULL,'125',125,'c','cc',125,'c','cc','ccc',125,NULL,12.4,-125,0.12,NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """invoke a11table;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s44')
    
    # a11.45:
    # TRAF: DDL in TX is not supported yet.  Move the alter table .. add column out of TX
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    # a11.46: add column 18 - variable
    stmt = """alter table a11table add column col20 varchar(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # a11.47:
    stmt = """insert into a11table (int1, "ems", "SQL", col17) values
(47, 12.60, 126, -126);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a11.48:
    stmt = """insert into a11table (int1, vch5, col17, col19, col20)
values (48, 'zz', -130, 'z', 'z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s07')
    
    stmt = """select int1, "SQL", "ems", col17, col18, col19, col20
from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
  
    # TRAF: DDL in TX is not supported yet.  Drop column to mimic the behavior of rollback. 
    stmt = """alter table a11table drop column col20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    time.sleep(5)
    
    # verify data after rollback
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s44')
    
    # ERROR[4001] Column COL20 is not found.
    stmt = """select int1, "SQL", "ems", col17, col18, col19, col20 from a11table;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    # a11.49:
    stmt = """insert into a11table values
(127,NULL,NULL,'127',interval '127:00:00:00.1111' day(4) to second(4),'127',127,'e','ee',127,'e','ee','eee',127,'compaq',12.7,-127,NULL,'e'),
(128,NULL,128,NULL,NULL,'128',128,'f','ff',128,'f','ff','fff',128,NULL,12.4,-128,NULL,NULL),
(129,'129',129,'129',interval '129:00:00:00.1111' day(4) to second(4),'129',129,'g','gg',129,'g','gg','ggg',129,'oracle',12.6,-129,0.26,'g');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    # a11.50:
    stmt = """insert into a11table (int1, vch5, col17, col19)
values (50, 'AA', -131, 'A');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from a11table order by int1,xch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s08')
    
    stmt = """select int1, "Sma1", "vch4*", vch5 from a11table where int1 > 35 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s08a')
    
    stmt = """select int1, "SQL", sma1, "vch%5", "modify"
from a11table where int1 > 35 order by int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s08b')
    
    _testmgr.testcase_end(desc)

def test012(desc="""a12 syntax test"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table a12tab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table a12tab2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table a12tab1 (
int1 int not null not droppable
, vch2 varchar(3)
, primary key (int1) not droppable
)
location """ + gvars.g_disc1 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table a12tab2 (
int1 int not null
, vch2 varchar(3)
)
store by ( int1 )
location """ + gvars.g_disc2 + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into a12tab1 values (1, '111'), (2, '222');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into a12tab2 (select * from a12tab1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """select * from a12tab1 order by int1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from a12tab2 order by int1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """alter table a12tab1 add column c3 largeint default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a12.1: c3 already defined
    # ERROR[1080] The create request has duplicate references to column C3.
    stmt = """alter table a12tab1 add column c3 char(3) default 'ABC';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1080')
    
    # a12.2: defaults is incorrect
    stmt = """alter table a12tab1 add column c4 int defaults 200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # a12.3: ERROR[4023] The degree of each row value constructor (2) must equal
    #        the degree of the target table column list (3).
    stmt = """insert into a12tab1 values (3, '333');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4023')
    
    stmt = """insert into a12tab1 values (3, '333', 333);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # a12.4: ERROR[1042] All PRIMARY KEY or UNIQUE constraint columns must
    #        be NOT NULL.
    stmt = """alter table a12tab1 add c5 int unique;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    # a12.5: ?? possible ERROR??
    stmt = """alter table a12tab1 add c6 int check (c6 > 1000) default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # a12.6: ERROR[4041] Type INTERVAL SECOND(2,6) cannot be compared
    #        with type CHAR(3).
    stmt = """alter table a12tab1 add c7 interval second check (c7 > '100');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    # a12.7: ERROR: Default value -100 is not valid for column C8.
    stmt = """alter table a12tab1 add c8 smallint unsigned default -100
check (c8 < -1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    # a12.8: ??
    stmt = """alter table a12tab1 add c9 char (4)
check (c9 < 'zzzzzz' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a12.9: ??
    stmt = """alter table a12tab1 add c10 varchar (2)
check (c10 > 'zzzzzz' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # a12.10: Default value _ISO88591'aaa' is not valid for column C11.
    stmt = """alter table a12tab1 add c11 varchar (2) default 'aaa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # a12.11: ERROR[1042] All PRIMARY KEY or UNIQUE constraint columns must
    #         be NOT NULL.
    stmt = """alter table a12tab1 add c12 varchar (2) unique;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    # a12.12: ERROR[1130] The column requires a default value.
    stmt = """alter table a12tab1 add c13 varchar (2) unique not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add column c14 numeric(9) unique int1, c5, c22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # a12.13: ERROR[1041] The primary key has already been defined.
    stmt = """alter table a12tab1 add c15 int primary key asc;"""
    _dci.expect_error_msg(output)

    stmt = """alter table a12tab1 add c16 char(4) primary key desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add c17 decimal(4,2) primary key ascending;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add column c18 pic x(9) primary key c23, int1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c19 int primary key int1 asc, c24 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[1136] For an added column, the PRIMARY KEY clause cannot
    #             specify NOT DROPPABLE.
    stmt = """alter table a12tab1 add column c20 int primary key not droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add column c21 smallint primary key droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add c22 pic x(3) reference a12tab2 (vch2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c23 char(30) default user NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add c24 char(30) default user "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c25 char(30) default NULL ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 drop column c26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add columns c27 pic s9(9)v9(2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[1130] The column requires a default value.
    stmt = """alter table a12tab1 add column c28 largeint not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add column c29 largeint not null not droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add column c30 int not null droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add column c31 dec(5,2) no default not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add column c32 float no default;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add c33 char(30) default current_date "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c34 char(30) default current_date '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c35 time default current_time '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c36 time default current_time '25:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[3046] The time '23:99:99' is not valid.
    stmt = """alter table a12tab1 add c37 time default time '23:99:99';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3046')
    
    # ERROR[3046] The time '25:00:00' is not valid.
    stmt = """alter table a12tab1 add c38 time default time '25:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3046')
    
    stmt = """alter table a12tab1 add c39 time default time heading "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # #expect any *15001*
    # alter table a12tab1 add c40 time default time heading '';
    
    stmt = """alter table a12tab1 add c41 time default time heading;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c42 time default time headings;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c95 date default current_date heading "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c96 int default 0 heading '';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c97 char(1) default 'a' heading;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c100 time heading 'time' no default ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c101 time no heading no default;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[1130] The column requires a default value.
    stmt = """alter table a12tab1 add c102 time no default heading 'time';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add c103 time default current_time no heading;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c43 time default time headings not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c44 time headings 'time' no default ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c45 time no headings 'time';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[3046] The time '24:00:00' is not valid.
    stmt = """alter table a12tab1 add c46 time check (c46 < time '24:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3046')
    
    # ERROR[1080] The create request has duplicate references to column C3.
    stmt = """alter table a12tab1 add column c3 double precision default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1080')
    
    # ERROR[1140] Row-length 4186 exceeds the maximum allowed row-length
    #             of 4036 for table CAT_ADD.SCH_ADD.N01TABLE.
    # doesn't work because of dblimits added to build 'alter table a12tab1 add c47 char(4096) default 'aaa';'
    # increase row length beyond maximum
    stmt = """alter table a12tab1 add c47 char(51000) default 'aaa';"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1140')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c48 varchar (2) unique not null default 'AB';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c49 largeint not null default 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c50 largeint not null not droppable
default 123456789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    stmt = """alter table a12tab1 add column c51 int not null droppable default -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c53 character varying(1)
character set ucs2 collate default upshift default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c54 nchar(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c55 nchar varying(1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c56 smallint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c57 integer default 12345;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c58 integer signed default -100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c59 integer unsigned default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c60 pic 9(9) default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c61 pic 9(9) comp default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c62 pic 9(9) display;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ERROR[3008] Precision of DECIMAL UNSIGNED data type, 11, cannot exceed 9.
    stmt = """alter table a12tab1 add c63 pic 9(9)v9(2)
display sign is leading;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3008')
    
    stmt = """alter table a12tab1 add c64 pic v9(2) display;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c65 float(22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c66 float(54);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c67 real(54) default 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c68 double precision(22);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c69 double precision;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ERROR[3135] The precision of float, 64, cannot exceed 54.
    stmt = """alter table a12tab1 add c66 float(64) default 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3135')
    
    stmt = """alter table a12tab1 add c67 interval year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c68 interval month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ERROR[1080] The create request has duplicate references to column C69.
    stmt = """alter table a12tab1 add c69 interval day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1080')
    
    stmt = """alter table a12tab1 add c70 interval minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c71 interval hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c72 interval second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add c73 interval year(18) default year '100';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[3044] The interval YEAR(19) is not valid.
    stmt = """alter table a12tab1 add c74 interval year(19);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3044')
    
    stmt = """alter table a12tab1 add c75 interval year(-1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[3044] The interval YEAR(2000) is not valid.
    stmt = """alter table a12tab1 add c75 interval year(2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3044')
    
    # ERROR[3044] The interval DAY(16) TO SECOND(5) is not valid.
    stmt = """alter table a12tab1 add c76 interval day(16) to second(5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3044')
    
    stmt = """alter table a12tab1 add c77 interval second(6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ERROR[3195] Table creation with data type INTERVAL with FRACTION field(s)
    #             is not supported.
    stmt = """alter table a12tab1 add c78 interval hour(6) to fraction (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3195')
    
    # ERROR[3044] The interval SECOND(2,10) is not valid.
    stmt = """alter table a12tab1 add c79 interval hour(2) to second(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3044')
    
    # ERROR[3134] The specified TIME or TIMESTAMP precision value, 12, cannot exceed 6.
    stmt = """alter table a12tab1 add c80 timestamp(12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3134')
    
    # ERROR[3134] The specified TIME or TIMESTAMP precision value, 10, cannot exceed 6.
    stmt = """alter table a12tab1 add c81 time(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3134')
    
    stmt = """alter table a12tab1 add c82 date(10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # ERROR[3045] The date ' ' is not valid.
    stmt = """alter table a12tab1 add c83 date default date ' ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3045')
    
    stmt = """alter table a12tab1 add c84 day default current_date;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c85 date default current_date ' ';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c86 long unsigned default 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c87 long signed default -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c88 long long default -100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c89 int (2) unique not null default 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add c90 pic x(3) references a12tab2 (vch2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab1 add c90 int references a12tab2(int1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # ERROR[1130] The column requires a default value.
    stmt = """alter table a12tab1 add c90 int not null references a12tab2 (int1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    # ERROR[1042] All PRIMARY KEY or UNIQUE constraint columns must be NOT NULL.
    stmt = """alter table a12tab1 add c90 int unique references a12tab2 (int1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    # ERROR[1130] The column requires a default value.
    stmt = """alter table a12tab1 add c90 int unique not null references a12tab2 (int1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1130')
    
    stmt = """alter table a12tab1 add c91 varchar(3) foreign key (vch2)
references a12tab2 (vch2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c92 float default -1 no default ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c93 int no default default -1 no default ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c94 int no default default -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """alter table a12tab1 add column c105 varchar(32);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add column c106 varchar(64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add column c107 varchar(128);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add column c108 varchar(256);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add column c109 varchar(512) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table a12tab1 add column c110 varchar(1024);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #alter table a12tab1 add column c111 varchar(2048);
    #changed due to dblimits have increased.
    stmt = """alter table a12tab1 add column c111 varchar(32709);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1140')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
   
    stmt = """alter table a12tab2 add c3 int primary key asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab2 add c4 char(4) primary key desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """alter table a12tab2 add c5 decimal(4,2) primary key ascending;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """alter table a12tab2 add column c6 smallint primary key droppable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """showddl a12tab1;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        added_cols_list = ['C3', 'C9', 'C10', 'C25', 'C96', 'C103', 'C53', 'C54', 'C55', 'C56', 'C57', 'C58', 'C59', 'C60', 'C61', 'C62', 'C64', 'C65', 'C66', 'C69', 'C67', 'C68', 'C70', 'C71', 'C72', 'C77', 'C105', 'C106', 'C107', 'C108', 'C109', 'C110']
    elif hpdci.tgtTR():
        added_cols_list = ['C3', 'C9', 'C10', 'C25', 'C96', 'C103', 
'C47', 'C53', 'C54', 'C55', 'C56', 'C57', 'C58', 'C59', 'C60', 'C61', 'C62', 'C64', 'C65', 'C66', 'C69', 'C67', 'C68', 'C70', 'C71', 'C72', 'C77', 'C105', 'C106', 'C107', 'C108', 'C109', 'C110', 'C111']
    for c in added_cols_list:
        _dci.expect_str_token(output, c)
 
    stmt = """showddl a12tab2;"""
    output = _dci.cmdexec(stmt)
    not_added_cols_list = ['C3', 'C4', 'C5', 'C6']
    for c in not_added_cols_list:
        _dci.unexpect_any_substr(output, c)

    stmt = """select count(*) from a12tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '3')
    
    stmt = """select count(*) from a12tab2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '2')
    
    _testmgr.testcase_end(desc)

