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

import t004a4_dat
import t001a_dat
import t003a_dat
import t001b_dat
import t002b_dat
import t002a_dat
import t004a3_dat
import t004a1_dat
import t003b_dat
import t004a2_dat
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
    
def test001(desc="""t001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in adjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t001sql
    # script: t001sql
    # varchar keys in adjacent columns
    
    stmt = """drop table t001t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t001t2;"""
    output = _dci.cmdexec(stmt)
    
    # t001.1: varchar keys in adjacent columns
    #   store by primary
    stmt = """create table t001t1 (
i1 int,
v1 varchar(1) default 'a',
v2 varchar(2) not null,
v3 varchar(8) default 'NULL' not null,
v4 varchar(16),
primary key (v2,v3) not droppable
)
attribute extent (1024, 1024), maxextents 15
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # load data on empty tables
    # t001.3: 20 rows
    
    # alter catalog ${test_catalog} disable schema sch;
    t001a_dat._init(_testmgr)
    # alter catalog ${test_catalog} enable schema sch;
    
    # t001.4:
    stmt = """select * from t001t1 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s4""")
    
    # insert some: single insert - all columns
    # t001.5:
    stmt = """insert into t001t1 values (101, 'a', 'AA', '0101', 'AAAAAAAA');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.6:
    stmt = """select * from t001t1 where i1 = 101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s6""")
    
    # 102, B, bb, 0102, BBBBBBBB
    # t001.7:
    stmt = """set param ?p1 B;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 bb;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 0102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 BBBBBBBB;"""
    output = _dci.cmdexec(stmt)
    
    # t001.8:
    stmt = """insert into t001t1 values (102, ?p1, ?p2, ?p3, ?p4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.9:
    stmt = """select * from t001t1 where
v1 = ?p1 and v2 = ?p2 and v3 = ?p3 and v4 = ?p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s9""")
    
    # 103, c, CC, 0103, ?
    # t001.10:
    stmt = """insert into t001t1 (i1, v1, v2, v3, v4) values (
103, '3', 'CC', '0103', NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s17""")
    
    stmt = """select * from t001t1 where v2 = 'CC' and v3 = '0103';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s10""")
    
    # 104, d, dd, 0104, zzzzABCD
    # t001.11:
    stmt = """insert into t001t1 (i1, v2, v3, v4 ) values (
104, 'dd', '0104', 'zzzzABCD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.12:
    stmt = """insert into t001t1 (v2, v3) values ('dd', '0105');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.13:
    stmt = """insert into t001t1 (i1, v1, v2, v3, v4 ) values (
106, 'z', 'zz', '0106', 'zzzzABCD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.14:
    stmt = """select * from t001t1 where char(ascii(v2)) = v1 and v3 > '0100';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s14""")
    
    # load data on non-empty tables
    # t001.15:
    stmt = """create table t001t2 like t001t1;"""
    output = _dci.cmdexec(stmt)
    # alter catalog ${test_catalog} disable schema sch;
    t001b_dat._init(_testmgr)
    # alter catalog ${test_catalog} enable schema sch;
    
    # t001.16:
    stmt = """insert into t001t1 (select * from t001t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
    
    # t001.17:
    stmt = """insert into t001t1 (v2, v3, v4)
values ('zz', '0107', 'zzzzABCD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.18:
    stmt = """insert into t001t1 (i1, v2, v3)
values (108, 'zz', '0108');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.19:
    stmt = """insert into t001t1 (v2, v3)
values ('dd', '0109');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.20:
    stmt = """insert into t001t1 (v1, v2, v3)
values ('z', 'zz', '0110');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.21:
    stmt = """select * from t001t1 where char(ascii(v2)) = v1 and v3 > '0100';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s21""")
    
    # t001.22: 50 rows
    stmt = """select * from t001t1 order by i1,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s22""")
    
    # update some
    # t001.25: 10 rows in consecutive order
    stmt = """update t001t1 set
i1 = i1+50,
v1 = 'M',
v4 = 'Mckinley'
where v2 between 'dd' and 'mm'
and v3 > '0021' and v3 < '0040';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    
    # debug
    # select v1,v4 from t001t1 order by 1,2;
    
    # t001.26:
    stmt = """select * from t001t1
where v1 = 'M' and v4 = 'McKinley';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t001.27: 1 row
    stmt = """update t001t1 set
i1 = 201,
v1 = 'Z',
v4 = 'Foraker'
where v2 = 'AA' and v3 = '0101';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # t001.28: 2 rows
    stmt = """update t001t1 set
v1 = 'x',
v4 = 'Denali'
where i1 is NULL and v2 = 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    # t001.29: 3 rows
    stmt = """update t001t1 set
i1 = i1+100,
v4 = 'Everest'
where i1 in (2,4,6,8,10,12,14,16,18,20)
and v1 in ('A','B','C','D','F')
and v2 between 'aa' and 'ss'
and v3 > '0000' and v3 < '0010'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    # t001.30:
    stmt = """select * from t001t1 order by v3,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s30""")
    
    # delete some
    # t001.31: 1 row
    stmt = """delete from t001t1
where v2 = 'nn' and v3 between '0010' and '0020';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t001.32: 1 row
    stmt = """delete from t001t1
where v2 = 'zz' and v3 = '0106';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t001.33: 11 rows
    stmt = """delete from t001t1
where ascii(v1) = ascii(v4)
and v3 between '0030' and '0050';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    
    # t001.34: 4 rows
    stmt = """delete from t001t1
where i1 in (1,3,5,7,9,11,13,15)
and v1 between 'A' and 'Z'
and v4 like '%IJ%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    # t001.35: 1 row
    stmt = """delete from t001t1
where i1 = 103 and v1 = '3' and v4 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t001.36: 1 row
    stmt = """delete from t001t1
where i1 = 201 and v1 = 'Z' and v2 = 'AA'
and v3 = '0101' and v4 = 'Foraker';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t001.37:
    stmt = """select * from t001t1 order by v3,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s37""")
    
    # t001.39:
    stmt = """select * from t001t1
where (v3 > '0000' and v3 < '0015')
or (v3 > '0105' and v3 < '0250')
and (v2 between 'aa' and 'ee')
or v2 in ('ll','oo','qq','tt','zz')
order by i1, v3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s39""")
    
    _testmgr.testcase_end(desc)

def test002(desc="""t002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in nonadjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # #runscript $test_dir/t002sql
    # script: t002sql
    # varchar keys in nonadjacent columns
    
    stmt = """drop table t002t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t002t2;"""
    output = _dci.cmdexec(stmt)
    
    # t002.1: varchar keys in nonadjacent columns
    stmt = """create table t002t1 (
i1 int,
v1 varchar(1) default 'a',
v2 varchar(2) not null,
v3 varchar(8),
v4 varchar(16) not null,
primary key (v2,v4) not droppable
)
attribute extent (1024, 1024), maxextents 15
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # load data on empty tables
    # t002.3: 20 rows
    
    # alter catalog cat_vchr001 disable schema sch;
    t002a_dat._init(_testmgr)
    # alter catalog cat_vchr001 enable schema sch;
    
    # t002.4:
    stmt = """select * from t002t1 order by v2,v4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s4""")
    
    # insert some: single insert - all columns
    # t002.5:
    stmt = """insert into t002t1 values (101, 'a', 'AA', 'AAAAAAAA','0101');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.6:
    stmt = """select * from t002t1 where i1 = 101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s6""")
    
    # 102, B, bb, 0102, BBBBBBBB
    # t002.7:
    stmt = """set param ?p1 B;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 bb;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 BBBBBBBB;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 0102;"""
    output = _dci.cmdexec(stmt)
    
    # t002.8:
    stmt = """insert into t002t1 values (102, ?p1, ?p2, ?p3, ?p4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.9:
    stmt = """select * from t002t1 where
v1 = ?p1 and v2 = ?p2 and v3 = ?p3 and v4 = ?p4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s9""")
    
    # 103, c, CC, ?, 0103
    # t002.10:
    stmt = """insert into t002t1 (i1, v1, v2, v3, v4) values (
103, '3', 'CC', NULL, '0103' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s17""")
    
    stmt = """select * from t002t1 where v2 = 'CC' and v3 = '0103';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # 104, d, dd, 0104, 'zzzzABCD'
    # t002.11:
    stmt = """insert into t002t1 (i1, v2, v3, v4 ) values (
104, 'dd', 'zzzzABCD','0104');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.12:
    stmt = """insert into t002t1 (v2, v4) values ('dd', '0105');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.13:
    stmt = """insert into t002t1 (i1, v1, v2, v3, v4 ) values (
106, 'z', 'zz', 'zzzzABCD','0106');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.14:
    stmt = """select * from t002t1 where char(ascii(v2)) = v1 and v4 > '0100';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s14""")
    
    # load data on non-empty tables
    # t002.15:
    stmt = """create table t002t2 like t002t1;"""
    output = _dci.cmdexec(stmt)
    
    t002b_dat._init(_testmgr)
    
    # t002.16:
    stmt = """insert into t002t1 (select * from t002t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
    
    # t002.17:
    stmt = """insert into t002t1 (v2, v3, v4)
values ('zz', 'zzzzABCD','0107');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.18:
    stmt = """insert into t002t1 (i1, v2, v4)
values (108, 'zz', '0108');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.19:
    stmt = """insert into t002t1 (v2, v4)
values ('dd', '0109');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.20:
    stmt = """insert into t002t1 (v1, v2, v4)
values ('z', 'zz', '0110');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002.21:
    stmt = """select * from t002t1 where char(ascii(v2)) = v1 and v4 > '0100';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s21""")
    
    # t002.22: 50 rows
    stmt = """select * from t002t1 order by i1,v4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s22""")
    
    # update some
    # t002.25: 10 rows in consecutive order
    stmt = """update t002t1 set
i1 = i1+50,
v1 = 'M',
v3 = 'Mckinley'
where v2 between 'dd' and 'mm'
and v4 > '0021' and v4 < '0040';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 10)
    
    # debug:
    # select v1,v3 from t002t1 order by 1,2;
    
    # t002.26:
    stmt = """select * from t002t1
where v1 = 'M' and v3 = 'McKinley';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t002.27: 1 row
    stmt = """update t002t1 set
i1 = 201,
v1 = 'Z',
v3 = 'Foraker'
where v2 = 'AA' and v4 = '0101';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # t002.28: 2 rows
    stmt = """update t002t1 set
v1 = 'x',
v3 = 'Denali'
where i1 is NULL and v2 = 'zz';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    # t002.29: 3 rows
    stmt = """update t002t1 set
i1 = i1+100,
v3 = 'Everest'
where i1 in (2,4,6,8,10,12,14,16,18,20)
and v1 in ('A','B','C','D','F')
and v2 between 'aa' and 'ss'
and v4 > '0000' and v4 < '0010'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    
    # t002.30:
    stmt = """select * from t002t1 order by v4,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s30""")
    
    # delete some
    # t002.31: 1 row
    stmt = """delete from t002t1
where v2 = 'nn' and v4 between '0010' and '0020';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t002.32: 1 row
    stmt = """delete from t002t1
where v2 = 'zz' and v4 = '0106';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t002.33: 11 rows
    stmt = """delete from t002t1
where ascii(v1) = ascii(v3)
and v4 between '0030' and '0050';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    
    # t002.34: 4 rows
    stmt = """delete from t002t1
where i1 in (1,3,5,7,9,11,13,15)
and v1 between 'A' and 'Z'
and v3 like '%IJ%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    # t002.35: 1 row
    stmt = """delete from t002t1
where i1 = 103 and v1 = '3' and v3 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t002.36: 1 row
    stmt = """delete from t002t1
where i1 = 201 and v1 = 'Z' and v2 = 'AA'
and v4 = '0101' and v3 = 'Foraker';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t002.37:
    stmt = """select * from t002t1 order by v4,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s37""")
    
    # t002.39:
    stmt = """select * from t002t1
where (v4 > '0000' and v4 < '0015')
or (v4 > '0105' and v4 < '0250')
and (v2 between 'aa' and 'ee')
or (v2 in ('ll','oo','qq','tt','zz'))
order by i1, v4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s39""")
    
    _testmgr.testcase_end(desc)

def test003(desc="""t003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in nonadjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t003sql
    # script: t003sql
    # multiple varchar columns with multiple varchar columns in
    #   clustering key
    
    stmt = """drop table t003t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t003t2;"""
    output = _dci.cmdexec(stmt)
    
    # t003.1:
    stmt = """create table t003t1 (
i1 int,
v1 varchar(1),
v2 varchar(4) not null,
v3 varchar(8) not null,
v4 varchar(16),
v5 varchar(32) not null,
v6 varchar(1),
primary key (v2, v3, v5) not droppable
)
attribute extent (1024, 1024)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t003.2:
    stmt = """create table t003t2 like t003t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t003.5: 20 rows
    
    t003a_dat._init(_testmgr)
    
    # t003.6: 20 rows
    t003b_dat._init(_testmgr)
    
    # t003t1: insert rows - v3
    #    0001 - 0020
    #    0101 - 0200, 0301-0400
    #    0041 - 0045
    #    0501 & 0505
    # t003.7:
    stmt = """insert into t003t1 (v2,v3,v5) values ('ww', '0041', 'wwww0041');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.8:
    stmt = """insert into t003t1 values (
42, '5', 'ww', '0042', 'BBCDEFGH', 'wwww0042', 'U');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.9:
    stmt = """insert into t003t1 (v1, v2, v3, v5) values (
'5', 'ww', '0043', 'wwww0043');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.10:
    stmt = """insert into t003t1 ( v2, v3, v4, v5) values (
'ww', '0044', 'BBCDEFGH', 'wwww0044');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.11:
    stmt = """insert into t003t1 ( v1, v2, v3, v5) values (
'5', 'ww', '0045', 'wwww0045');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.12:
    stmt = """insert into t003t1 (select * from t003t2 where v3 = '0505');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.13:
    stmt = """insert into t003t1 (v2, v3, v5) values (
(select v2 from t003t2 where v3 = '0501'),
(select v3 from t003t2 where v3 = '0501'),
(select v5 from t003t2 where v3 = '0501'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003.15:
    stmt = """select i1, v1, v2, v3,
cast (v4 as char(8)),
cast (v5 as varchar(8)), v6 from t003t1
order by i1, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s15""")
    
    # t003.16:
    stmt = """insert into t003t1 (select * from t003t2 where v3 < '0450');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 200)
    
    # t003.17:
    stmt = """select count(*) from t003t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s17""")
    
    # t003.18:
    stmt = """select i1, v1, v2, v3,
cast (v4 as char(8)),
cast (v5 as varchar(8)), v6 from t003t1
where v3 between '0030' and '0050'
or v3 in ('0101','0201','0301','0400', '0401')
or v3 > '0500'
order by i1, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s18""")
    
    # t003t1: insert rows - v3
    #    0001 - 0020
    #    0101 - 0200, 0301-0400
    #    0041 - 0045
    #    0501 & 0505
    # t003t1: update rows - v3
    #    0150, 0151, 0504,
    #    0311-0330
    #    0111-0150, 0171-0190
    #    interleave ...
    # t003.20: update with keys
    # 50, 5, jj, 0150, BBCDEFGH, iiii0150, U
    stmt = """update t003t1 set
i1 = 50,
v1 = '7',
v4 = 'BBCDEFGH',
v6 = 'U'
where v2 = 'jj' and v3 = '0150' and v5 = 'iiii0150';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t003.22:
    # 51, 5, kk, 0151, KLMNOPQR, kkkk0151, K
    stmt = """update t003t1 set
i1 = 51,
v1 = '7'
where v2 = (select v2 from t003t1 where v3 = '0151')
and v3 = '0151'
and v4 = (select v4 from t003t1 where v3 = '0151')
and v5 = (select v5 from t003t1 where v3 = '0151')
and v6 = 'K';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t003.24:
    # 501, 1, cc, 0152, EFGHIJKL, eeee0506, G
    stmt = """update t003t1 set
i1 = (select i1 from t003t2 where v3 = '0501'),
v1 = '7',
v4 = (select v4 from t003t2 where v3 = '0505'),
v6 = (select v6 from t003t2 where v3 = '0507')
where v3 = '0152';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t003.25:
    stmt = """select i1, v1, v2, v3,
cast (v4 as varchar(8)),
cast (v5 as varchar(8)), v6 from t003t1
where v3 between '0150' and '0153'
or v3 between '0500' and '0510'
order by i1, v3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s25""")
    
    # t003.27: 11 rows
    stmt = """update t003t1 set
i1 = i1 + 100,
v1 = '6'
where i1 < 400
and v4 like 'IJ%'
and v6 between 'A' and 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    # t003.28:
    stmt = """select i1, v1, v2, v3,
cast (v4 as varchar(8)),
cast (v5 as varchar(8)), v6 from t003t1
where v1 = '6' and v4 like 'IJ%'
order by i1, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s28""")
    
    # subset of consecutive rows
    # t003.29: 60 rows
    stmt = """update t003t1 set
i1 = i1 + 300,
v1 = '7',
v4 = concat('ZZZZ', v3)
where v3 < '0151' and v3 > '0110'
or v3 < '0191' and v3 > '0170';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 60)
    
    # t003.30:
    stmt = """select i1, v1, v2, v3,
cast (v4 as varchar(8)),
cast (v5 as varchar(8)), v6 from t003t1
where v3 < '0152' and v3 > '0109'
or v3 < '0192' and v3 > '0169'
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s30""")
    
    # t003.31:
    stmt = """update t003t1 set
i1 = i1 - 100,
v1 = '7',
v4 = v5,
v6 = 'U'
where v2 in ('aa','dd','gg','jj','mm','pp')
and v3 between '0370' and '0399'
and substring(v5,5,4) between '0370' and '0399'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 9)
    
    # t003.32:
    stmt = """select count(*) from t003t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s32""")
    
    # t003.35:
    stmt = """select i1, v1, v2, v3,
cast (v4 as varchar(8)),
cast (v5 as varchar(8)), v6 from t003t1
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s35""")
    
    # t003t1: update rows - v3
    #    0150, 0151, 0504,
    #    0311-0330
    #    0111-0150, 0171-0190
    #    interleave ...
    # t003t1: delete rows - v3
    # t003.41:
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    # t003.43: single delete on keys
    stmt = """delete from t003t1
where v2 = 'tt' and v3 = '0120' and v5 = 'ssss0120';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t003.45: subset_delete
    stmt = """delete from t003t1
where v3 > '0145' and v3 < '0166';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 20)
    
    # t003.47:
    stmt = """delete from t003t1 where i1 > 520;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    # t003.49:
    stmt = """delete from t003t1
where (i1,v1,v4,v6) is NULL
and v2 = 'aa'
and v3 = substring(v5,5,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t003.51:
    stmt = """delete from t003t1
where v1 in ('5','6','7')
and v2 in ('aa','cc','ii','mm','oo','qq')
and substring(v5,1,4) = substring(v4,1,4)
and v3 between '0350' and '0450'
or v4 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    # t003.53:
    stmt = """delete from t003t1
where v2 = (select v2 from t003t2 where v3 = '0391')
and v3 = '0391'
and v5 = (select v5 from t003t2 where v3 = '0391')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t003.55: missing key
    stmt = """delete from t003t1
where v1 = (select v1 from t003t2 where v3 = '0595');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # t003.57: missing key
    # v1 is '4'
    stmt = """delete from t003t1
where v1 = (select v1 from t003t2 where v3 = '0320');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 33)
    
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    
    # t003.59:
    stmt = """select count(*) from t003t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s59""")
    
    # t003.60:
    stmt = """select i1, v1, v2, v3,
cast (v4 as varchar(8)),
cast (v5 as varchar(8)), v6 from t003t1
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s60""")
    
    _testmgr.testcase_end(desc)

def test004(desc="""t004"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in nonadjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t004sql
    # script: t004sql
    # multiple varchar columns with multiple varchar columns in
    #   clustering key
    
    stmt = """drop table t004s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t004t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t004t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t004t3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t004t4;"""
    output = _dci.cmdexec(stmt)
    
    # t004.1: big rows and big keys
    stmt = """create table t004t1 (
i1 int,
v1 varchar(1),
v2 varchar(4) not null,
v3 varchar(128) not null,
v4 varchar(256),
v5 varchar(1024) not null,
v6 varchar(4028),
primary key (v2, v3, v5) not droppable
)
store by (v2, v3, v5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t004.2:
    stmt = """create table t004t2 like t004t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t004.3: 20 rows
    
    defs.tbname = """t004t1"""
    t004a1_dat._init(_testmgr)
    
    # t004.4: 20 rows
    t004a2_dat._init(_testmgr)
    
    # t004t1: insert rows - v3
    #    0001 - 0020
    #    0101 - 0200, 0301-0400
    #    0041 - 0045
    #    0501 & 0505
    # t004.5:
    
    stmt = """set param ?p1 ww;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 wwww;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 0041;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'Mount Fairweather has generally harsh weather conditions';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 'Fairweather';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t004t1 (v2,v3,v5) values (?p1, ?p2, ?p2 || ?p3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t004.6:
    stmt = """select i1,v1,v2,
substring(v3,1,8), substring(v4,1,8),
substring(v5,1,8), substring(v6,1,20)
from t004t1
where v2 = ?p1 and v3 = ?p2 and v5 = concat(?p2, ?p3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s6""")
    
    # t004.7:
    stmt = """insert into t004t1 values (
42, '5', 'ww', '0042', 'BBCDEFGH',
substring(?p4,7,11), ?p4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t004.8:
    stmt = """select i1,v1,v2,
substring(v3,1,8), substring(v4,1,8),
substring(v5,1,11), substring(v6,1,17)
from t004t1
where v5 = 'Fairweather';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s8""")
    
    # t004.9:
    stmt = """insert into t004t1 (v1, v2, v3, v5) values (
'5', 'ww', '0043', 'wwww0043');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t004.10:
    stmt = """insert into t004t1 ( v2, v3, v4, v5) values (
'ww', '0044', 'BBCDEFGH', 'wwww0044');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t004.11:
    stmt = """insert into t004t1 ( v1, v2, v3, v5, v6) values (
'5', 'ww', '0045', 'wwww0045', replace(?p4, ?p5, 'Cook'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t004.12:
    stmt = """insert into t004t1 (select * from t004t2 where v3 = '0505');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t004.13:
    stmt = """insert into t004t1 (v2, v3, v5) values (
(select v2 from t004t2 where v3 = '0501'),
(select v3 from t004t2 where v3 = '0501'),
(select v5 from t004t2 where v3 = '0501'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # Ignore warning 8402
    # t004.15:
    stmt = """select i1, v1, v2, cast(v3 as varchar(4)),
cast (v4 as char(8)),
cast (v5 as varchar(8)),
substring(v6,1,40)
from t004t1 order by i1, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s15""")
    
    # t004.17:
    stmt = """insert into t004t1 (select i1, v1, v2, v3, v4, v5, v6
from t004t2 where v3 < '0450');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 200)
    
    # t004.19:
    stmt = """select count(*) from t004t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s17""")
    
    # t004.20:
    stmt = """select i1, v1 || v2, cast(concat(v3,v4) as varchar(20)),
cast (v5 as varchar(8)), cast(v6 as char(30)) from t004t1
where v3 between '0030' and '0050'
or v3 in ('0101','0201','0301','0400', '0401')
or v3 > '0500'
order by i1, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s20""")
    
    # t004execute:
    stmt = """create table t004s1 like t004t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    defs.tbname = """t004s1"""
    t004a1_dat._init(_testmgr)
    
    # #runscript $test_dir/t004exec1
    # script: t004exec1
    # cross join: cartesian product of two tables 20*227= 4540 rows
    stmt = """showshape
select substring(t1.v3,1,8), substring(t1.v6,1,12),
substring(s1.v3,1,8), substring(s1.v6,1,12)
from t004t1 t1, t004s1 s1 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # debug:
    # select v3 from t004t1 order by 1;
    
    stmt = """prepare s01 from
select substring(t1.v3,1,8), substring(t1.v6,1,12),
substring(s1.v3,1,8), substring(s1.v6,1,12)
from t004t1 t1, t004s1 s1 order by t1.v3,s1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set envvar NO_SCREEN_OUTPUT 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s01""")
    stmt = """reset envvar NO_SCREEN_OUTPUT;"""
    output = _dci.cmdexec(stmt)
    
    # natural join: 20 rows
    stmt = """showshape
select v1,v2, substring(v3,1,8), substring(v5,1,8)
from t004t1 natural join t004s1
order by v3,v2,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s02 from
select v1,v2, substring(v3,1,8), substring(v5,1,8)
from t004t1 natural join t004s1
order by v3,v2,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s02;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s02""")
    
    # inner join: 2o rows
    stmt = """showshape
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t1 t1 inner join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s03 from
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t1 t1 inner join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s03;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s03""")
    
    # left join: 227 rows
    stmt = """showshape
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t1 t1 left join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s04 from
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t1 t1 left join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s04;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s04""")
    
    # right join: 20 rows
    stmt = """showshape
select substring(t1.v5,1,8), substring(s1.v5,1,8)
from t004t1 t1 right join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s05 from
select substring(t1.v5,1,8), substring(s1.v5,1,8)
from t004t1 t1 right join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s05;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s05""")
    
    # self join:
    stmt = """showshape
select t1.v1, t2.v2,
substring(t2.v5,1,8), substring(t1.v6,1,32)
from t004t1 t1, t004t1 t2
where t1.v2 = substring(t2.v5,1,2)
order by t1.v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s06 from
select t1.v1, t2.v2,
substring(t2.v5,1,8), substring(t1.v6,1,32)
from t004t1 t1, t004t1 t2
where t1.v2 = substring(t2.v5,1,2)
order by t1.v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s06;"""
    output = _dci.cmdexec(stmt)
    
    # debug:
    # select v5 from t004t1 order by 1;
    
    stmt = """set envvar NO_SCREEN_OUTPUT 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s06""")
    stmt = """reset envvar NO_SCREEN_OUTPUT;"""
    output = _dci.cmdexec(stmt)
    
    # union
    stmt = """showshape
select substring(v5,1,2), substring(v3,1,8), substring(v4,1,8)
from t004s1
union
select v2, substring(v3,1,8), substring(v4,1,8)
from t004t1
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s07 from
select substring(v5,1,2), substring(v3,1,8), substring(v4,1,8)
from t004s1
union
select v2, substring(v3,1,8), substring(v4,1,8)
from t004t1
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s07;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s1exp""", """s07""")
    
    # t004.21a:
    stmt = """create table t004t3 like t004t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # log $test_dir/t004t1log clear;
    # select * from t004t1 order by i1,v2,v3;
    # log off;
    
    # t004.21b: 227 rows
    
    t004a3_dat._init(_testmgr)
    
    # t004t1: update rows - v3
    #    0150, 0151, 0504,
    #    0311-0330
    #    0111-0150, 0171-0190
    #    interleave ...
    # 50, 5, jj, 0150, BBCDEFGH, iiii0150, ...
    
    stmt = """set param ?p6 'Mount McKinley or Denali in Alaska is the highest mountain peak in North America, at a height of approximately 20,320 feet (6,194 m). It is the centerpiece of Denali National Park. The mountain is also known as Bolshaya Gora, meaning Big Mountain, in Russian.';"""
    output = _dci.cmdexec(stmt)
    
    # t004.22: update with keys
    stmt = """update t004t3 set
i1 = 50,
v1 = '7',
v4 = v3 || v3,
v6 = ?p6
where v2 = 'jj' and v3 = '0150' and v5 = 'iiii0150';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t004.25:
    # 51, 5, kk, 0151, KLMNOPQR, kkkk0151, ...
    stmt = """update t004t3 set
i1 = 51,
v1 = '7',
v6 = ?p6
where v2 = (select v2 from t004t3 where v3 = '0151')
and v3 = '0151'
and v4 = (select v4 from t004t3 where v3 = '0151')
and v5 = (select v5 from t004t3 where v3 = '0151')
and v6 like '%America';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t004.27:
    # 501, 1, cc, 0152, EFGHIJKL, eeee0506, G
    stmt = """update t004t3 set
i1 = (select i1 from t004t2 where v3 = '0501'),
v1 = '7',
v4 = (select v4 from t004t2 where v3 = '0505'),
v6 = (select insert(v6,9,7,'McKinley') from t004t2 where v3 = '0507')
where v3 = '0152';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t004.29:
    stmt = """select i1, concat(v1, v2) as v1v2,
cast(trim(v3) as varchar(4)) as vv3,
cast(replace(v4,'CDEF',trim(v3)) as varchar(8)) as vv4,
cast(repeat(substring(v5,5,4),2) as varchar(8)) as vv5,
cast(substring(v6,19,40) as varchar(40)) as vv6
from t004t3
where v3 between '0150' and '0153'
or v3 between '0500' and '0510'
order by i1, v3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s29""")
    
    # t004.31: 11 rows
    stmt = """update t004t3 set
i1 = i1 + 100,
v1 = '6',
v6 = replace(cast(?p6 as varchar(259)), ' or Denali ',' ')
where i1 < 400
and v4 like 'IJ%'
and char(ascii(v6)) between 'A' and 'Z';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    # t004.33:
    stmt = """select i1, v1, v2, cast(v3 as varchar(4)),
cast (v4 as varchar(8)), cast (v5 as varchar(8)),
cast (v6 as varchar(40)) from t004t3
where v1 = '6' and v4 like 'IJ%'
order by i1, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s33""")
    
    stmt = """set param ?p7 'Bolshaya Gora, meaning Big Mountain,';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p8 'Big Mountain';"""
    output = _dci.cmdexec(stmt)
    
    # subset of consecutive rows
    # t004.35: 39 rows
    stmt = """update t004t3 set
i1 = i1 + 300,
v1 = '7',
v4 = concat('zzzz', v3),
v6 = substring(replace(cast(?p6 as varchar(259)),
cast(?p7 as varchar(36)),cast(?p8 as varchar(12))) from 135)
where v3 < '0121' and v3 > '0110'
or v3 < '0191' and v3 > '0181'
or v3 between '0331' and '0345'
or v3 in ('0351','0361','0375','0395','0399');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 39)
    
    # t004.37:
    stmt = """select i1, v1, v2, substring(v3,1,4), substring(v4,1,8),
substring(v5,1,8) from t004t3
where v3 < '0121' and v3 > '0110'
or v3 < '0191' and v3 > '0181'
or v3 between '0331' and '0345'
or v3 in ('0351','0361','0375','0395','0399')
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s37""")
    
    # t004.39:
    stmt = """select cast(v3 as varchar(4)),
substring(v6,48,42) from t004t3
where v3 < '0121' and v3 > '0110'
or v3 < '0191' and v3 > '0181'
or v3 between '0331' and '0345'
or v3 in ('0351','0361','0375','0395','0399')
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s39""")
    
    # t004.41:
    stmt = """update t004t3 set
i1 = i1 - 100,
v1 = '7',
v4 = v5,
v6 = left(cast(?p6 as varchar(259)),34) || '.tbc.'
where v2 in ('aa','dd','gg','jj','mm','pp')
and v3 between '0370' and '0399'
and substring(v5,5,4) between '0370' and '0399'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 9)
    
    stmt = """select i1,v1,substring(v4,1,8),substring(v6,1,35) from t004t3
where v6 like '%.tbc.%';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from t004t3 where left(v6,3) = 'A M';"""
    output = _dci.cmdexec(stmt)
    
    # t004.43:
    stmt = """select cast(v3 as varchar(4)),
cast(insert(v6, 1, 15, 'Mount McKinley') as varchar(72))
from t004t3 where left(v6,3) = 'A M' order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s43""")
    
    stmt = """select count(*) from t004t3 where v6 like 'Mount McKinley%';"""
    output = _dci.cmdexec(stmt)
    
    # t004.45:
    stmt = """update t004t3 set
v4 = v1 || v2 || v3,
v6 = replace(v6,'compressed','internal')
where v2 in ('aa','bb','ee','jj','qq','ss','tt')
and v3 < '0050';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 7)
    
    stmt = """select cast(v4 as varchar(12)), cast(v6 as varchar(54))
from t004t3 where v6 like '%internal%'
order by v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s45""")
    
    # t004.46: yku
    # mode_0: $SQL_updated_msg 31
    # mode_1: $SQL_updated_msg 42
    stmt = """update t004t3 set
v4 = 'Whitney',
v6 = replace(v6,'Whitney','McKinley')
where v1 = '4'
and right(trim(v4),1) > 'L'
and left(v4,1) <> '4'
and octet_length(v6) < 42;"""
    output = _dci.cmdexec(stmt)
    
    # log $test_dir/t004t3log clear;
    # select * from t004t3 order by i1,v2,v3;
    # log off;
    
    # t004.45a:
    stmt = """create table t004t4 like t004t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t004.45b: 227 rows
    
    t004a4_dat._init(_testmgr)
    
    # t004.49:
    stmt = """select count(*) from t004t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s49""")
    
    # t004.51:
    stmt = """select i1, v1, v2, substring(v3,1,4),
substring(v4,1,8), substring(v5,1,8) from t004t4
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s51""")
    
    # t004.53:
    stmt = """select cast(v3 as varchar(4)) as vch3, substring(v6,1,64)
from t004t4 order by v3, i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s53""")
    
    # t004.54:
    stmt = """select i1, cast(v3 as varchar(4)),
char_length(v3) as L3, octet_length(v4) as L4,
char_length(v5) as L5, octet_length(v6) as L6
from t004t4
where i1 in (1, 20, 101, 411, 269, 490)
or i1 between 41 and 50
order by i1,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s54""")
    
    # t004.55: 7
    stmt = """select count(*) from t004t4 where char_length(v4) = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s55""")
    
    # t004.56: 62 rows
    stmt = """select count(*) from t004t4 where char_length(v6) > 42;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s56""")
    
    # t004.57: 17 rows
    stmt = """select count(*) from t004t4 where v4 like '_CDEFGH_'
or v4 like 'GHIJKLM_';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s57""")
    
    # t004t4: update rows - v3
    #    0150, 0151, 0504,
    #    0311-0330
    #    0111-0150, 0171-0190
    #    interleave ...
    # t004t4: delete rows - v3
    # t004.41:
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    # t004.43: single delete on keys
    stmt = """delete from t004t4
where v2 = 'tt' and v3 = '0120' and v5 = 'ssss0120';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t004.45: subset_delete
    stmt = """delete from t004t4
where v3 > '0145' and v3 < '0166'
or v3 > '0190' and v3 < '0196';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 25)
    
    # t004.47: i1 = 589
    stmt = """delete from t004t4 where i1 > 520;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 21)
    
    # t004.49: v3 = 0043
    stmt = """delete from t004t4
where (i1,v1,v4,v6) is NULL
and v2 = 'aa'
and v3 = substring(v5,5,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t004.51:
    stmt = """delete from t004t4
where v1 in ('5','6','7')
and v2 in ('aa','cc','ii','mm','oo','qq')
and substring(v5,1,4) = substring(v4,1,4)
and v3 between '0350' and '0450'
or v4 is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 6)
    
    # t004.53:
    stmt = """delete from t004t4
where v2 = (select v2 from t004t2 where v3 = '0391')
and v3 = '0391'
and v5 = (select v5 from t004t2 where v3 = '0391')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t004.55: missing key
    stmt = """delete from t004t4
where v1 = (select v1 from t004t2 where v3 = '0595');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # t004.57:
    stmt = """delete from t004t4 where v3 = '0120';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    # t004.58: v1 is '4'
    stmt = """delete from t004t4
where v1 = (select v1 from t004t2 where v3 = '0320');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 37)
    
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    
    # t004.59:
    stmt = """select count(*) from t004t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s59""")
    
    # t004.60:
    stmt = """select i1, v1, v2, cast(v3 as varchar(8)),
cast (v4 as varchar(8)),
cast (v5 as varchar(8)), cast(v6 as varchar(32)) from t004t4
order by v3,i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004exp""", """t004s60""")
    
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t004exec2
    # script: t004exec2
    # cross join: cartesian product of two tables 20*227= 4540 rows
    stmt = """showshape
select substring(t1.v3,1,8), substring(t1.v6,1,12),
substring(s1.v3,1,8), substring(s1.v6,1,12)
from t004t4 t1, t004s1 s1 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s01 from
select substring(t1.v3,1,8), substring(t1.v6,1,12),
substring(s1.v3,1,8), substring(s1.v6,1,12)
from t004t4 t1, t004s1 s1 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s01;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set envvar NO_SCREEN_OUTPUT 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s01""")
    stmt = """reset envvar NO_SCREEN_OUTPUT;"""
    output = _dci.cmdexec(stmt)
    
    # natural join: 20 rows
    stmt = """showshape
select v1,v2, substring(v3,1,8), substring(v5,1,8)
from t004t4 natural join t004s1
order by v3,v2,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s02 from
select v1,v2, substring(v3,1,8), substring(v5,1,8)
from t004t4 natural join t004s1
order by v3,v2,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s02;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s02""")
    
    # inner join: 2o rows
    stmt = """showshape
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t4 t1 inner join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s03 from
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t4 t1 inner join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s03;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s03""")
    
    # left join: 227 rows
    stmt = """showshape
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t4 t1 left join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s04 from
select substring(t1.v3,1,8), substring(s1.v3,1,8)
from t004t4 t1 left join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s04;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s04""")
    
    # right join: 20 rows
    stmt = """showshape
select substring(t1.v5,1,8), substring(s1.v5,1,8)
from t004t4 t1 right join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s05 from
select substring(t1.v5,1,8), substring(s1.v5,1,8)
from t004t4 t1 right join t004s1 s1
on t1.v3 = s1.v3 order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s05;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s05""")
    
    # self join:
    stmt = """showshape
select t1.v1, t2.v2,
substring(t2.v5,1,8), substring(t1.v6,1,32)
from t004t4 t1, t004t4 t2
where t1.v2 = substring(t2.v5,1,2)
order by t1.v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s06 from
select t1.v1, t2.v2,
substring(t2.v5,1,8), substring(t1.v6,1,32)
from t004t4 t1, t004t4 t2
where t1.v2 = substring(t2.v5,1,2)
order by t1.v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s06;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """set envvar NO_SCREEN_OUTPUT 1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s06""")
    stmt = """reset envvar NO_SCREEN_OUTPUT;"""
    output = _dci.cmdexec(stmt)
    
    # union
    stmt = """showshape
select substring(v5,1,2), substring(v3,1,8), substring(v4,1,8)
from t004s1
union
select v2, substring(v3,1,8), substring(v4,1,8)
from t004t4
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s07 from
select substring(v5,1,2), substring(v3,1,8), substring(v4,1,8)
from t004s1
union
select v2, substring(v3,1,8), substring(v4,1,8)
from t004t4
order by 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s07;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t004s2exp""", """s07""")
    
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """set warnings on;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

