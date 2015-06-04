# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

import t003a_dat
import t001b_dat
import t003b_dat
import t001a_dat
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
    
def test001(desc="""t001"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in adjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t001setup
    # setup.01: varchar keys in adjacent columns
    #   store by primary
    stmt = """create table t001t1 (
i1 int not null,
i2 int,
v1 varchar(1) default 'a',
v2 varchar(2) not null,
v3 varchar(4) default 'NULL' not null,
v4 varchar(8) not null,
v5 varchar(16),
v6 varchar(32) default 'qadev.teg',
primary key (v2,v3) not droppable
)
attribute extent (1024, 1024), maxextents 15, blocksize 4096
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    
    # set constraints
    #expect purge
    stmt = """alter table t001t1 add constraint t001c1 check (i1 < 5000);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = """alter table t001t1 add constraint t001c2 check (v1 between 'A' and 'z');"""
    output = _dci.cmdexec(stmt)
    stmt = """alter table t001t1 add constraint t001c3 check (v2 between 'AA' and 'zz');"""
    output = _dci.cmdexec(stmt)
    stmt = """alter table t001t1 add constraint t001c4 check (v3 between '0000' and '9999');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index t001i11 on t001t1 (v1,v2);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index t001i12 on t001t1 (v2,v3);"""
    output = _dci.cmdexec(stmt)
    
    # setup.05:
    stmt = """create view t001v11 as select * from t001t1 where
insert(v5, 15, 2, 'ZZ') like '%ZZ';"""
    output = _dci.cmdexec(stmt)
    # setup.06:
    stmt = """create view t001v12 as select * from t001t1
where repeat(lower(v1),2) = v2 and v3 < '1000';"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t001sql
    # script: t001sql
    # create table ... like
    # t001.1:
    stmt = """create table t001t2 like t001t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t001.2:
    stmt = """create table t001t5 like t001t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t001t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl t001t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl t001t5;"""
    output = _dci.cmdexec(stmt)
    
    # load data on empty tables
    # query plan operator:
    #   sidetree insert     : create table as ...;
    #   insert_vsbb insert  : insert into <select ...);
    # t001.3: 20 rows
    
    t001a_dat._init(_testmgr)
    
    # t001.4:
    stmt = """select * from t001t1 order by i1,v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s4""")
    
    # t001.5: 250 rows
    t001b_dat._init(_testmgr)
    
    # t001.6:
    stmt = """select * from t001t2 order by i1,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s6""")
    
    # t001.7: create table as ...
    # 20 rows: varchar keys in adjacent order
    # $SQL_complete_msg
    stmt = """create table t001t3 (
int1 int,
vch1 varchar(1) ,
vch2 varchar(2) not null,
vch3 varchar(4) not null,
primary key (vch2,vch3) not droppable
) as select i1, v1, v2, v3 from t001t1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
    
    # t001.8:
    stmt = """select * from t001t3 order by int1, vch2, vch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s8""")
    
    # t001.10: 100 rows: store by
    # $SQL_complete_msg
    stmt = """create table t001t4 (
int1 int not null,
int2 int,
vchar1 varchar(1),
vchar2 varchar(2) not null,
vchar3 varchar(4) not null,
vchar4 varchar(8) not null,
vchar5 varchar(16),
vchar6 varchar(32))
store by (int1, vchar2, vchar3) as select * from t001t2
where v3 between '0100' and '0200';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 100)
    
    # t001.11:
    stmt = """select count(*) from t001t4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s11""")
    
    # t001.12:
    stmt = """select * from t001t4 order by 1,2,3,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s12""")
    
    # t001.13: insert into (select ...)
    stmt = """insert into t001t5 (select * from t001t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 250)
    
    # t001.14:
    stmt = """select * from t001t5 order by 1,4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s14""")
    
    # insert some: single insert - all columns
    # t001.15
    stmt = """insert into t001t1 values (
101, 101, 'a', 'AA', '0101', 'AAAAAAAA',
'1234567890123456',
'12345678902234567890333456789012');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # 102, ?, B, bb, 0102, BBBBBBBB, ?, ?
    stmt = """set param ?p1 B;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 bb;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 0102;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 BBBBBBBB;"""
    output = _dci.cmdexec(stmt)
    
    # t001.16
    stmt = """insert into t001t1 (i1, v1, v2, v3, v4, v6) values (
102, ?p1, ?p2, ?p3, ?p4, NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.17
    # 103, ?, c, CC, 0103, cccccccc, ?
    # not allow numbers
    # #expectfile $test_dir/t001exp t001s17
    stmt = """insert into t001t1 (i1, v1, v2, v3, v4, v5, v6) values (
103, '3', 'CC', '0103', concat('ccc','ccccc'), NULL, 'role.user');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # t001.18
    stmt = """insert into t001t1 (i1, i2, v1, v2, v3, v4, v6) values (
103, NULL, 'c', 'CC', '0103', concat('ccc','ccccc'),
'qadev' || '.' || 'user1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.19
    stmt = """select * from t001t1 where upper(v1) = 'C'
and lower(v2) = 'cc'
and v4 = repeat('c',8)
and right(upper(v6),5) = 'USER1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s19""")
    
    # 104, 104, d, dd, 0104, 5555567890123456, ?
    # t001.20
    stmt = """insert into t001t1 (i1, i2, v1, v2, v3, v4 ) values (
104, 104, 'd', 'dd', '0104', repeat('dD',2) || '0104');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t001.21
    stmt = """select * from t001t1 where v2 = repeat(v1,2)
and v3 = '0104'
and left(lower(v4),4) = 'dddd';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s21""")
    
    # t001.22
    stmt = """select * from t001t1 where (i2, v5, v6) is NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s22""")
    
    # insert into an non-empty table: 2 rows where v2 = gg
    # t001.23
    stmt = """insert into t001t1 (
select * from t001t2 where
v2 = substring(v5 from 13 for 2) and v3 between '0105' and '0130');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    # t001.24: 26 rows
    stmt = """select count(*) from t001t1 where v3 < '0135';"""
    output = _dci.cmdexec(stmt)
    
    # t001.25:
    stmt = """select * from t001t1 where
v2 = substring(v5 from 13 for 2) and v3 between '0105' and '0130'
order by v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s25""")
    
    # t001.26
    # insert 0151 to 0350
    stmt = """insert into t001t1 (
select * from t001t2 where v3 > '0150' and v6 like 'qadev%');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 200)
    
    # t001.27: 200 rows
    stmt = """select count(*) from t001t1 where v3 > '0135';"""
    output = _dci.cmdexec(stmt)
    # t001.28: 200 rows
    stmt = """select count(*) from t001t1 where i1 > 135;"""
    output = _dci.cmdexec(stmt)
    
    # t001.29: violate constraint
    ##expectfile $test_dir/t001exp t001s29
    stmt = """insert into t001t1 (i1, v1,v2,v3,v4) values (
2000, '0', '00', 'ZZZZ', '00000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # t001.30: string overflow
    # mode_0: #expect any *8402*
    # mode_1: 1 row(s) inserted
    stmt = """insert into t001t1 (i1, v1,v2,v3,v4) values (
2000, 'a', 'aaa', '0000000000', 'ABCDEFGHIJK');"""
    output = _dci.cmdexec(stmt)
    
    # t001.31: violate constraint
    ##expectfile $test_dir/t001exp t001s31
    stmt = """insert into t001t1 (i1, v1,v2,v3,v4) values (
7000, 'z', 'zz', 'ZZZZ', '00000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # t001.32: violate constraint - v1 and v2 not between A and z
    stmt = """insert into t001t2 (i1, v1,v2,v3,v4) values (
2000, '0', '00', '9999', '00000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s32""")
    
    # t001.33: string overflow - v3 > varchar(4)
    # mode_0: #expect any *8402*
    # mode_1: 1 row(s) inserted
    stmt = """insert into t001t5 (i1, v1,v2,v3,v4) values (
2000, '0', 'aaa', repeat('0', 12), 'ABCDEFG');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    # t001.34: violate constraint - i1 > 5000
    stmt = """insert into t001v11 (i1, v1,v2,v3,v4) values (
7000, 'z', 'zz', '9999', '00000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # t001.35: violate constraint - v3 not numbers
    stmt = """insert into t001v12 (i1, v1,v2,v3,v4) values (
4999, 'z', 'zz', 'zzzz', '00000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    # adjust the difference between mode_0 and mode_1
    stmt = """select * from t001t1 where i1 = 2000;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from t001t1 where i1 = 2000;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from t001t5 where i1 = 2000;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from t001t5 where i1 = 2000;"""
    output = _dci.cmdexec(stmt)
    
    # t001.40
    stmt = """set param ?p1 'this is a test for compressed varchar project in R2.3';"""
    output = _dci.cmdexec(stmt)
    
    # t001.41
    stmt = """insert into t001t1 (i1, v1, v2, v3, v4, v5, v6)
(select i1+2000,v1,v2,
cast(cast(v3 as decimal(4)) + 2000 as varchar(4)),
v1 || v2 || '00000',
substring(?p1,20,8) || substring(v5,9,1) || 'd    ',  -- compressed
left(v6,2) || current_user
from t001t5
where v3 <= '0120'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
    
    # t001.42: 246 rows
    stmt = """select * from t001t1 order by i1,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 246)
    
    # update some
    
    stmt = """set param ?p1 z;"""
    output = _dci.cmdexec(stmt)
    
    # update a single row: predicate on keys
    # t001.48
    # 350, ?, J, jj, 0350, JKLMNOPQ, ZZZZZZZZZZZZZZZZ, Z*32
    stmt = """update t001t1 set
i2 = NULL,
v1 = ?p1,
v5 = repeat('Z',16),
v6 = repeat(?p1,32)
where v2 = 'jj' and v3 = '0350';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # t001.49: update a single row
    # 105, 105, E, ee, 0105, EFGHIJKL, ABCDEFGHbcdefghi,
    #                                  AABBCCDDEEFFGGHHaabbccddeeffgghh
    stmt = """update t001t1 set
i2 = 105,
v5 = (select v4 from t001t5 where i1 = 101) ||
(select lcase(v4) from t001t5 where i1 = 102),
v6 = (select upper(v5) from t001t5 where i1 = 101) ||
(select v5 from t001t5 where i1 = 102)
where i1 = 20 and v1 = 'T' and v2 = 'tt' and v3 = '0020';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # update a subset of rows
    # t001.50
    stmt = """update t001t1 set
v5 = v4,
v6 = v1 || v2 || v3
where v3 >= '2000'
and substring(v4 from 4 for 5) = '00000'
and v2 = repeat(lower(v1),2)
and v1 = substring(ucase(v2) from 1 for 1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 20)
    
    # t001.51
    stmt = """update t001t2 set
v5 = 'aBcDeFgH',
v6 = 'aAbBcCdDeEfFgGhF'
where substring(v4 from 1 for 1) in ('A', 'B', 'C', 'D')
and substring(v5 from 3 for 2) = v2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 13)
    
    # t001.52
    stmt = """update t001t2 set
v5 = (select v4 from t001t1 where v2 = 'kk' and v5 = 'compressed' ),
v6 = (select v5 from t001t1 where v4 = 'Aaa00000')
where (v2 = 'tt' or v2 = 'jj')
and v3 between '0100' and '0450'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 25)
    
    # t001.53
    stmt = """update t001t5 set
v1 = 'x',
v5 = 'xxxxxxxx'
where v2 > 'ii' and v3 between '0000' and '0120';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    # t001.54
    stmt = """update t001t5 set
i2 = i1,
v5 = v3 || v3,
v6 = repeat(v3,8)
where v3 > '0250' and (v2 between 'aa' and 'jj')
and i1 < 300
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 20)
    
    # t001.55: 246 rows
    stmt = """select * from t001t1 order by v2,v3,i1,i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s55""")
    
    # t001.56: 251 rows
    stmt = """select * from t001t2 order by v2,v3,i1,i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s56""")
    
    # t001.57: 250 rows
    stmt = """select * from t001t5 order by v2,v3,i1,i2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s57""")
    
    # select some
    # t001.60:
    # #runscript $test_dir/t001select
    # script: t001select
    # t001prepare.01: hash_groupby
    
    stmt = """showshape
select v4, count(v4) from t001t1
group by v4 order by v4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s01 from
select v4, count(v4) from t001t1
group by v4 order by v4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.01: hash_groupby
    stmt = """explain options 'f' s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s01exe""")
    
    # t001prepare.02: ordered hash join
    
    stmt = """showshape
select i1, v1, v3, v3
from t001t1 t1, t001t3 t3
where t1.v3 = t3.vch3
order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s02 from
select i1, v1, v3, v3
from t001t1 t1, t001t3 t3
where t1.v3 = t3.vch3
order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.02: ordered hash join
    stmt = """explain options 'f' s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s02exe""")
    
    # t001prepare.03: left ordered hash join
    
    stmt = """showshape
select i1, vch1 || v1, vch2, vch3
from t001t3 left join t001t1
on vch3 = v3
where vch3 < '0100'
order by i1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s03 from
select i1, vch1 || v1, vch2, vch3
from t001t3 left join t001t1
on vch3 = v3
where vch3 < '0100'
order by i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.03: left ordered hash join
    stmt = """explain options 'f' s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s03exe""")
    
    # t001prepare.04: ordered_hash_semi_join
    
    stmt = """showshape
select vch1, vch2, vch3
from t001t3
where vch1 in
(select v1 from t001t1)
order by vch1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s04 from
select vch1, vch2, vch3
from t001t3
where vch1 in
(select v1 from t001t1)
order by vch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.04: ordered_hash_semi_join
    stmt = """explain options 'f' s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s04exe""")
    
    # t001prepare.05: sort_groupby
    
    stmt = """showshape
select vch3, max(vch2) from t001t3 group by vch3
order by vch3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s05 from
select vch3, max(vch2) from t001t3 group by vch3
order by vch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.05: sort_groupby
    stmt = """explain options 'f' s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s05exe""")
    
    # t001prepare.06: sort_partial_groupby
    
    stmt = """showshape
select vch1, vch2, count(vch2)
from t001t3 group by vch1, vch2 having vch1 = 'L';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s06 from
select vch1, vch2, count(vch2)
from t001t3 group by vch1, vch2 having vch1 = 'L';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.06: sort_partial_groupby
    stmt = """explain options 'f' s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s06exe""")
    
    # t001prepare.07: sort_scalar_aggr
    
    stmt = """showshape
select max(vchar3) from t001t4 where vchar2 = 'tt';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s07 from
select max(vchar3) from t001t4 where vchar2 = 'tt';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.07: sort_scalar_aggr
    stmt = """explain options 'f' s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s07exe""")
    
    # t001prepare.08: sort
    
    stmt = """showshape
select v2, v3, v4, v5 from t001t1
where v3 between '0200' and '0300'
order by v2, v3, v4, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s08 from
select v2, v3, v4, v5 from t001t1
where v3 between '0200' and '0300'
order by v2, v3, v4, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.08: sort
    stmt = """explain options 'f' s08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s08exe""")
    
    # t001prepare.09: OR optimization
    
    stmt = """showshape
select i1, v3, vch3, v4, v5 from t001t1 t1, t001t3 t3, t001t4 t4
where t1.v4 = 'ABCDEFGH' and t1.i1 > t3.int1
and (t1.v2 = vchar2 OR t3.vch2 = vchar2)
and v1 = vch1 and vch1 = vchar1
and v6 like 'qadev%' order by i1, v3, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s09 from
select i1, v3, vch3, v4, v5 from t001t1 t1, t001t3 t3, t001t4 t4
where t1.v4 = 'ABCDEFGH' and t1.i1 > t3.int1
and (t1.v2 = vchar2 OR t3.vch2 = vchar2)
and v1 = vch1 and vch1 = vchar1
and v6 like 'qadev%' order by i1, v3, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.09: OR optimization
    stmt = """explain options 'f' s09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute s09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s09exe""")
    
    # delete some
    # t001.61: delete and rollback
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # #runscript $test_dir/t001delete
    # script: t001delete
    
    stmt = """set param ?p1 z;"""
    output = _dci.cmdexec(stmt)
    
    # delete a single row: predicate on keys
    # t001delete.01
    # 18,18,r,rr,0018,RSTUWVXY,aabbccddeeffgghh,qadev.teg
    
    stmt = """delete from t001t1 where v2 = 'rr' and v3 = '0018';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t001delete.02: delete a single row
    # 105, 105, E, ee, 0105, EFGHIJKL, ABCDEFGHbcdefghi,
    #                                  AABBCCDDEEFFGGHHaabbccddeeffgghh
    stmt = """delete from t001t1
where i2 = 105
and v5 = (select v4 from t001t5 where i1 = 101) ||
(select lcase(v4) from t001t5 where i1 = 102)
and v6 = (select upper(v5) from t001t5 where i1 = 101) ||
(select v5 from t001t5 where i1 = 102);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # delete a subset of rows
    # t001delete.04
    stmt = """delete from t001t1
where i2 is NULL
and v1 in ('A','C','E','G','I','K','M','O','Q')
and substring(v4 from 4 for 5) = '00000'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 9)
    
    # t001delete.05
    stmt = """select * from t001t1 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """delt1""")
    
    # t001delete.10
    
    stmt = """set param ?p1 'eEfFgGhF';"""
    output = _dci.cmdexec(stmt)
    
    # t001delete.11
    stmt = """delete from t001t2
where v5 = 'aBcD' || 'eFgH'
and v6 = concat('aAbBcCdD',?p1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 13)
    
    # t001delete.12
    stmt = """delete from t001t2
where (v2 = (select v2 from t001t1 where v3 = '0010')
or  v2 in (select v2 from t001t1 where v4 like 'T%'))
and v3 between '0100' and '0450'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 25)
    
    # t001delete.13
    stmt = """select * from t001t2 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """delt2""")
    
    # t001delete.16
    stmt = """delete from t001t5
where v1 = 'x' and v5 = repeat(v1,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    
    # t001delete.17
    stmt = """delete from t001t5
where i2 = i1
and v5 = v3 || v3
and v3 > '0250' and (v2 between 'aa' and 'jj')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 20)
    
    # t001delete.18
    stmt = """select * from t001t5 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """delt5""")
    
    # t001.62
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # statements should be recompiled
    # t001.63: output should be the same as t001.60
    
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t001.64
    # #runscript $test_dir/t001select
    # script: t001select
    # t001prepare.01: hash_groupby
    
    stmt = """showshape
select v4, count(v4) from t001t1
group by v4 order by v4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s01 from
select v4, count(v4) from t001t1
group by v4 order by v4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.01: hash_groupby
    stmt = """explain options 'f' s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s01exe""")
    
    # t001prepare.02: ordered hash join
    
    stmt = """showshape
select i1, v1, v3, v3
from t001t1 t1, t001t3 t3
where t1.v3 = t3.vch3
order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s02 from
select i1, v1, v3, v3
from t001t1 t1, t001t3 t3
where t1.v3 = t3.vch3
order by t1.v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.02: ordered hash join
    stmt = """explain options 'f' s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s02exe""")
    
    # t001prepare.03: left ordered hash join
    
    stmt = """showshape
select i1, vch1 || v1, vch2, vch3
from t001t3 left join t001t1
on vch3 = v3
where vch3 < '0100'
order by i1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s03 from
select i1, vch1 || v1, vch2, vch3
from t001t3 left join t001t1
on vch3 = v3
where vch3 < '0100'
order by i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.03: left ordered hash join
    stmt = """explain options 'f' s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s03exe""")
    
    # t001prepare.04: ordered_hash_semi_join
    
    stmt = """showshape
select vch1, vch2, vch3
from t001t3
where vch1 in
(select v1 from t001t1)
order by vch1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s04 from
select vch1, vch2, vch3
from t001t3
where vch1 in
(select v1 from t001t1)
order by vch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.04: ordered_hash_semi_join
    stmt = """explain options 'f' s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s04exe""")
    
    # t001prepare.05: sort_groupby
    
    stmt = """showshape
select vch3, max(vch2) from t001t3 group by vch3
order by vch3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s05 from
select vch3, max(vch2) from t001t3 group by vch3
order by vch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.05: sort_groupby
    stmt = """explain options 'f' s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s05exe""")
    
    # t001prepare.06: sort_partial_groupby
    
    stmt = """showshape
select vch1, vch2, count(vch2)
from t001t3 group by vch1, vch2 having vch1 = 'L';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s06 from
select vch1, vch2, count(vch2)
from t001t3 group by vch1, vch2 having vch1 = 'L';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.06: sort_partial_groupby
    stmt = """explain options 'f' s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s06exe""")
    
    # t001prepare.07: sort_scalar_aggr
    
    stmt = """showshape
select max(vchar3) from t001t4 where vchar2 = 'tt';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s07 from
select max(vchar3) from t001t4 where vchar2 = 'tt';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.07: sort_scalar_aggr
    stmt = """explain options 'f' s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s07exe""")
    
    # t001prepare.08: sort
    
    stmt = """showshape
select v2, v3, v4, v5 from t001t1
where v3 between '0200' and '0300'
order by v2, v3, v4, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s08 from
select v2, v3, v4, v5 from t001t1
where v3 between '0200' and '0300'
order by v2, v3, v4, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.08: sort
    stmt = """explain options 'f' s08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s08exe""")
    
    # t001prepare.09: OR optimization
    
    stmt = """showshape
select i1, v3, vch3, v4, v5 from t001t1 t1, t001t3 t3, t001t4 t4
where t1.v4 = 'ABCDEFGH' and t1.i1 > t3.int1
and (t1.v2 = vchar2 OR t3.vch2 = vchar2)
and v1 = vch1 and vch1 = vchar1
and v6 like 'qadev%' order by i1, v3, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s09 from
select i1, v3, vch3, v4, v5 from t001t1 t1, t001t3 t3, t001t4 t4
where t1.v4 = 'ABCDEFGH' and t1.i1 > t3.int1
and (t1.v2 = vchar2 OR t3.vch2 = vchar2)
and v1 = vch1 and vch1 = vchar1
and v6 like 'qadev%' order by i1, v3, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t001select.09: OR optimization
    stmt = """explain options 'f' s09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """execute s09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001pexp""", """s09exe""")
    
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t001.65:
    # #runscript $test_dir/t001delete
    # script: t001delete
    
    stmt = """set param ?p1 z;"""
    output = _dci.cmdexec(stmt)
    
    # delete a single row: predicate on keys
    # t001delete.01
    # 18,18,r,rr,0018,RSTUWVXY,aabbccddeeffgghh,qadev.teg
    
    stmt = """delete from t001t1 where v2 = 'rr' and v3 = '0018';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # t001delete.02: delete a single row
    # 105, 105, E, ee, 0105, EFGHIJKL, ABCDEFGHbcdefghi,
    #                                  AABBCCDDEEFFGGHHaabbccddeeffgghh
    stmt = """delete from t001t1
where i2 = 105
and v5 = (select v4 from t001t5 where i1 = 101) ||
(select lcase(v4) from t001t5 where i1 = 102)
and v6 = (select upper(v5) from t001t5 where i1 = 101) ||
(select v5 from t001t5 where i1 = 102);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # delete a subset of rows
    # t001delete.04
    stmt = """delete from t001t1
where i2 is NULL
and v1 in ('A','C','E','G','I','K','M','O','Q')
and substring(v4 from 4 for 5) = '00000'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 9)
    
    # t001delete.05
    stmt = """select * from t001t1 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """delt1""")
    
    # t001delete.10
    
    stmt = """set param ?p1 'eEfFgGhF';"""
    output = _dci.cmdexec(stmt)
    
    # t001delete.11
    stmt = """delete from t001t2
where v5 = 'aBcD' || 'eFgH'
and v6 = concat('aAbBcCdD',?p1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 13)
    
    # t001delete.12
    stmt = """delete from t001t2
where (v2 = (select v2 from t001t1 where v3 = '0010')
or  v2 in (select v2 from t001t1 where v4 like 'T%'))
and v3 between '0100' and '0450'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 25)
    
    # t001delete.13
    stmt = """select * from t001t2 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """delt2""")
    
    # t001delete.16
    stmt = """delete from t001t5
where v1 = 'x' and v5 = repeat(v1,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 11)
    
    # t001delete.17
    stmt = """delete from t001t5
where i2 = i1
and v5 = v3 || v3
and v3 > '0250' and (v2 between 'aa' and 'jj')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 20)
    
    # t001delete.18
    stmt = """select * from t001t5 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """delt5""")
    
    # t001.65: 235 rows
    stmt = """select * from t001t1 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s65""")
    
    # t001.66: 213 rows
    stmt = """select * from t001t2 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s66""")
    
    # t001.67: 219 rows
    stmt = """select * from t001t5 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s67""")
    
    # t001.70: create volatile table
    stmt = """create volatile table voltt1 (
i1 int not null,
i2 int,
v1 varchar(1) default 'a',
v2 varchar(2) not null,
v3 varchar(4) default 'NULL' not null,
v4 varchar(8) not null,
v5 varchar(16),
v6 varchar(32) default 'qadev.teg' not null,
primary key (v2,v3) not droppable
)
attribute extent (1024, 1024), maxextents 15
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t001.71: 100 rows
    stmt = """insert into voltt1 (select * from t001t4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 100)
    
    # t001.72:
    # $SQL_complete_msg
    stmt = """create volatile table voltt2 as select * from voltt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 100)
    # t001.73:
    # $SQL_complete_msg
    stmt = """create volatile table voltt3 as select * from t001t3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
    
    # t001.74: 100 rows
    stmt = """select * from voltt1 order by v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s74""")
    
    # t001.75: 100 rows
    stmt = """select * from voltt2 order by i1,v2,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s75""")
    
    # t001.76: 20 rows
    stmt = """select * from voltt3 order by int1, vch3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s76""")
    
    # t001.77: 100 rows
    stmt = """select count(*) from voltt1
where ascii(v1) = ascii(ucase(v2))
and v2 = repeat(lower(v1),2)
and v3 < '1000'
and cast(v3 as integer) = i1
and insert(v5,5,8,v4) = 'aabb' || v4 || 'gghh';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t001exp""", """t001s77""")
    
    _testmgr.testcase_end(desc)

def test002(desc="""t002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in adjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # #runscript $test_dir/t002sql
    # script: t002sql
    # t002.1: insert (tuplelist)  : insert into (),(),..;
    stmt = """create table t002t1 (
i1 int,
v1 varchar(10),
v2 varchar(27) not null,
v3 varchar(2) not null,
primary key (v2, v3) not droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t002.2:
    stmt = """insert into t002t1 values
(1,  '1', '   01', '11'), (2, '2', '   02', '22'), (3, '3', '   03', '33'),
(4,  '4', '04   ', '44'), (5, '5', '   05', '55'), (6, '6', '06   ', '66'),
(7,  '7', ' 07 ' , '77'), (8, '8', ' 08 ',  '88'), (9, '9', ' 09 ',  '99'),
(10, '0', '10'   , '00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    # t002.3: 10 rows
    stmt = """select * from t002t1 order by v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s3""")
    
    # t002.4: sidetree insert when more than 110 records
    # insert (tuplelist)  : insert into (),(),..;
    stmt = """create table t002t2 (
v1 varchar(1) not null not droppable,
v2 varchar(8) not null not droppable,
v3 varchar(16),
primary key (v1,v2)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t002.5:
    stmt = """insert into t002t2 values
('1','001','11'), ('2','002','22'), ('3','003','33'), ('4','004','44'), ('5','005','55'),
('6','006','66'), ('7','007','77'), ('8','008','88'), ('9','009','99'), ('0','010','00'),
('1','011','11'), ('2','012','22'), ('3','013','33'), ('4','014','44'), ('5','015','55'),
('6','016','66'), ('7','017','77'), ('8','018','88'), ('9','019','99'), ('0','020','00'),
('1','021','11'), ('2','022','22'), ('3','023','33'), ('4','024','44'), ('5','025','55'),
('6','026','66'), ('7','027','77'), ('8','028','88'), ('9','029','99'), ('0','030','00'),
('1','031','11'), ('2','032','22'), ('3','033','33'), ('4','034','44'), ('5','035','55'),
('6','036','66'), ('7','037','77'), ('8','038','88'), ('9','039','99'), ('0','040','00'),
('1','041','11'), ('2','042','22'), ('3','043','33'), ('4','044','44'), ('5','045','55'),
('6','046','66'), ('7','047','77'), ('8','048','88'), ('9','049','99'), ('0','050','00'),
('1','051','11'), ('2','052','22'), ('3','053','33'), ('4','054','44'), ('5','055','55'),
('6','056','66'), ('7','057','77'), ('8','058','88'), ('9','059','99'), ('0','060','00'),
('1','061','11'), ('2','062','22'), ('3','063','33'), ('4','064','44'), ('5','065','55'),
('6','066','66'), ('7','067','77'), ('8','068','88'), ('9','069','99'), ('0','070','00'),
('1','071','11'), ('2','072','22'), ('3','073','33'), ('4','074','44'), ('5','075','55'),
('6','076','66'), ('7','077','77'), ('8','078','88'), ('9','079','99'), ('0','080','00'),
('1','081','11'), ('2','082','22'), ('3','083','33'), ('4','084','44'), ('5','085','55'),
('6','086','66'), ('7','087','77'), ('8','088','88'), ('9','089','99'), ('0','090','00'),
('1','091','11'), ('2','092','22'), ('3','093','33'), ('4','094','44'), ('5','095','55'),
('6','096','66'), ('7','097','77'), ('8','098','88'), ('9','099','99'), ('0','100','00'),
('1','101','11'), ('2','102','22'), ('3','103','33'), ('4','104','44'), ('5','105','55'),
('6','106','66'), ('7','107','77'), ('8','108','88'), ('9','109','99'), ('0','110','00'),
('1','111','11'), ('2','112','22'), ('3','113','33'), ('4','114','44'), ('5','115','55'),
('6','116','66'), ('7','117','77'), ('8','118','88'), ('9','119','99'), ('0','120','00'),
('1','121','11'), ('2','122','22'), ('3','123','33'), ('4','124','44'), ('5','125','55'),
('6','126','66'), ('7','127','77'), ('8','128','88'), ('9','129','99'), ('0','130','00'),
('1','131','11'), ('2','132','22'), ('3','133','33'), ('4','134','44'), ('5','135','55'),
('6','136','66'), ('7','137','77'), ('8','138','88'), ('9','139','99'), ('0','140','00'),
('1','141','11'), ('2','142','22'), ('3','143','33'), ('4','144','44'), ('5','145','55'),
('6','146','66'), ('7','147','77'), ('8','148','88'), ('9','149','99'), ('0','150','00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 150)
    
    # t002.6: 150 rows
    stmt = """select * from t002t2 order by v2,v1,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s6""")
    
    # t002.7
    
    stmt = """set param ?p1 -9;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p2 05.234567;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p3 '01/01/1980';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 06.234567e1;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p5 'z';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p6 ' z';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p7 ' Yosemite National Park';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p8 'ZZ';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """show param;"""
    output = _dci.cmdexec(stmt)
    # t002.8
    #expect purge
    
    # t002ins.1:
    stmt = """insert into t002t1 (v1, v2, v3) values (
'z', cast (cast (01.0 as smallint unsigned) as varchar(27)),
upper('zz'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t002ins.2:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (-0123456789.1 as int) as varchar(27)), ?p1);"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.3:
    stmt = """insert into t002t1 (i1, v1, v2, v3) values (
13, 'z',
cast (cast (01.234567890e7 as integer unsigned) as varchar(27)),
'z' || 'Z');"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.4:
    stmt = """insert into t002t1 (v1, v2, v3) values (
?p1, cast (cast (-01.234567891e5 as largeint signed) as varchar(27)),
?p6);"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.5:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (' - 01.1 ' as numeric) as varchar(27)), substring(?p7,2,2));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.6:
    stmt = """insert into t002t1 (i1, v2, v3) values (
16, cast (cast (-012.30 as numeric(3,1) signed) as varchar(27)),
cast(16 as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.7:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (01.23456e1 as numeric(5,3) unsigned) as varchar(27)),
(select v3 from t002t2 where v2 = '017'));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.8:
    stmt = """insert into t002t1 (v1, v2, v3) values (
cast(18 as char(10)),
cast(01.234567 as varchar(9)) || '-e001', repeat(?p5,2));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.9:
    stmt = """insert into t002t1 (v2, v3) values (
cast(-01.234567 as varchar(10)), concat(?p5,?p5));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.10:
    stmt = """insert into t002t1 (i1, v2, v3) values ( 10,
cast(date '09/21/2007' as char(10)), cast(hour(current_time) as char(2)));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.11:
    stmt = """insert into t002t1 (v2, v3) values (
concat(cast('Hello' as char(5)), ' World!'),
cast(month(current_date) as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.12:
    stmt = """insert into t002t1 (v1, v2, v3) values (
cast(current_date as char(10)),
cast (cast (011.3579 as decimal(5,3) unsigned) as varchar(27)),
(select trim(v2) from t002t1 where trim(v2) = '07'));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.13:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (-029e-1 as pic s9 display sign is leading) as varchar(27)),'$ ');"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.14:
    stmt = """insert into t002t1 (v1, v2, v3) values ( '   AAAA   ',
cast (cast (' 01234.50 ' as picture 999(2)v9 display) as varchar(27)),
char(ascii('?')) || '!' );"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.15:
    stmt = """insert into t002t1 (v1, v2, v3) values ( '     BBBBB',
cast (cast (-0.123456789012 as picture sv999(9) comp) as varchar(27)),
cast (ascii('0') as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.16:
    stmt = """insert into t002t1 (v1, v2, v3) values ('ccccc     ',
cast (cast (2.1234567 as float) as varchar(27)), 'v3');"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.17:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (2.2345678e0 as float(15)) as varchar(27)), upshift(?p5));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.18:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (' -3.3345678e0 ' as real) as varchar(27)),
cast (locate('N', cast(?p7 as varchar(30))) as varchar(2)));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.19:
    stmt = """insert into t002t1 (v2, v3) values (
cast (cast (' -4.3345678e0 ' as double precision) as varchar(27)), '19');"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.20:
    stmt = """insert into t002t1 (v2, v3) values (
cast(cast(?p1 as integer) as varchar(10)), concat('Z',?p5));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.21:
    stmt = """insert into t002t1 (v2, v3) values (
cast(cast(?p2 as decimal(10,8)) as varchar(27)),lpad('22',2,?p8));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.22:
    stmt = """insert into t002t1 (i1, v2, v3) values ( 22,
cast(cast('1980-01-01' as date) as varchar(10)), '22');"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.23:
    stmt = """insert into t002t1 (v2, v3) values (
cast(cast(?p4 as numeric(11,9)) as varchar(27)), rpad('YY',1));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.24:
    stmt = """insert into t002t1 (v1, v2, v3) values (
?p5, concat('today is ', cast (current_date as varchar(10))), '99');"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.25:
    stmt = """insert into t002t1 (v2, v3) values (
concat('the time is ', (cast (current_time as varchar(10)))),
substring(?p3,9,2));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.26:
    stmt = """insert into t002t1 (v1, v2, v3) values (
?p5, cast(current_timestamp as varchar(27)), concat(?p5, '9'));"""
    output = _dci.cmdexec(stmt)
    
    # t002ins.27:
    stmt = """insert into t002t1 (v1, v2, v3) values (
'Z', cast(current_user as varchar(27)), lpad('ZZ',1));"""
    output = _dci.cmdexec(stmt)
    
    # t002.10:
    stmt = """select * from t002t1 order by 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 37)
    
    # t002.11:
    stmt = """select * from t002t1 where (i1, v1) is NULL order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 13)
    
    # t002.12:
    stmt = """select * from t002t1 where trim(v2) NOT between '01' and '20'
order by v2, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 18)
    
    # t002.13:
    stmt = """select * from t002t1 where v3 = ?p8 order by v2, v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s13""")
    
    # t002.15: rollback work
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t002.16:
    # #runscript $test_dir/t002update
    # script: t002update
    stmt = """prepare upd1 from
update t002t2 set
v3 = 'ZZ' where v1 = '9' and v2 = '099';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from t002t2 where v3 = 'ZZ' order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds01""")
    
    stmt = """prepare upd2 from
update t002t2 set
v3 = 'ZZ' where v1 = '9' and v2 like '%9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 15)
    
    stmt = """select * from t002t2 where v3 = 'ZZ' order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds02""")
    
    stmt = """prepare upd3 from
update t002t2 set
v3 = (select v2 from t002t1 where v3 = 'Y ')
where v1 = '2' and v2 = '052';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from t002t2 where v1 = '2' and v2 = '052';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds03""")
    
    stmt = """select v2, cast(v2 as decimal(4)) / 119 from t002t2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare upd4 from
update t002t2 set
v3 = v2 || '.' || insert(v3,3,10,'-123456789')
where v1 between '5' and '9'
and cast(v2 as decimal(4)) / 119 = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # mode_0: $SQL_updated_msg 1
    # mode_1: $SQL_updated_msg 45
    stmt = """execute upd4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """exes04""")
    
    stmt = """select * from t002t2 where v2 = '119';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds04""")
    
    stmt = """prepare upd5 from
update t002t2 set
v3 = '0001-01-01'
where v2 = (select '0' || v3 from t002t1
where v2 = concat('today is ', cast(current_date as varchar(10))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p1 'Mount Mckinley National Park';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare upd6 from
update t002t2 set
v3 = substring(?p1,7,8)
where v1 in (select v1 from t002t1
where v1 is not null and v1 < '5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 75)
    
    stmt = """select count(*) from t002t2 where v3 = 'Mckinley';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '75')
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    time.sleep(15)
    
    # t002.20:
    stmt = """select * from t002t2 order by v2,v1,v3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s6""")
    
    # t002.21: commit work
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    # t002.22
    # #runscript $test_dir/t002update
    # script: t002update
    stmt = """prepare upd1 from
update t002t2 set
v3 = 'ZZ' where v1 = '9' and v2 = '099';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from t002t2 where v3 = 'ZZ' order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds01""")
    
    stmt = """prepare upd2 from
update t002t2 set
v3 = 'ZZ' where v1 = '9' and v2 like '%9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 15)
    
    stmt = """select * from t002t2 where v3 = 'ZZ' order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds02""")
    
    stmt = """prepare upd3 from
update t002t2 set
v3 = (select v2 from t002t1 where v3 = 'Y ')
where v1 = '2' and v2 = '052';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from t002t2 where v1 = '2' and v2 = '052';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds03""")
    
    stmt = """prepare upd4 from
update t002t2 set
v3 = v2 || '.' || insert(v3,3,10,'-123456789')
where v1 between '5' and '9'
and cast(v2 as decimal(4)) / 119 = 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # mode_0: $SQL_updated_msg 1
    # mode_1: $SQL_updated_msg 45
    stmt = """execute upd4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """exes04""")
    
    stmt = """select * from t002t2 where v2 = '119';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """upds04""")
    
    stmt = """prepare upd5 from
update t002t2 set
v3 = '0001-01-01'
where v2 = (select '0' || v3 from t002t1
where v2 = concat('today is ', cast(current_date as varchar(10))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """set param ?p1 'Mount Mckinley National Park';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare upd6 from
update t002t2 set
v3 = substring(?p1,7,8)
where v1 in (select v1 from t002t1
where v1 is not null and v1 < '5');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' upd6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute upd6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 75)
    
    stmt = """select count(*) from t002t2 where v3 = 'Mckinley';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '75')
    
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    
    # t002.23:
    stmt = """select * from t002t2 order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s23""")
    
    # t002.25:
    # 0,00,00,000-123456789
    # mode_0: $SQL_deleted_msg 1
    # mode_1: $SQL_deleted_msg 44
    stmt = """delete from t002t2
where substring(v3,8,9) = '123456789';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002d25""")
    stmt = """;"""
    output = _dci.cmdexec(stmt)
    
    # t002.26:
    # 9, 099, 0001-01-01
    stmt = """delete from t002t2
where v2 = (select '0' || v3 from t002t1
where v2 = concat('today is ', cast(current_date as varchar(10))));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """set param ?p1 'Mount Mckinley National Park';"""
    output = _dci.cmdexec(stmt)
    
    # t002.27:
    # mode_0: $SQL_deleted_msg 54
    # mode_1: $SQL_deleted_msg 40
    stmt = """delete from t002t2
where v3 = substring(?p1,7,8)
and v1 in ('2','4','6','8','0')
and (v2 > '000' and v2 < '100')
or (v2 > '125' and v2 < '175')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002d27""")
    
    # t002.28:
    stmt = """select * from t002t2 order by 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t002exp""", """t002s28""")
    
    _testmgr.testcase_end(desc)

def test003(desc="""t003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # varchar keys in nonadjacent columns
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop index t003i11;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view  t003v11;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view  t003v12;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t003t1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table t003t2;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default hist_missing_stats_warning_level '0';"""
    output = _dci.cmdexec(stmt)
    
    # #runscript $test_dir/t003sql
    # script: t003sql
    # multiple varchar columns with two varchar columns in
    #   clustering key in nonadjacent order
    
    #expect purge
    
    # t003.1: varchar keys in adjacent columns
    #   store by primar;y
    stmt = """create table t003t1 (
i1 int not null,
v1 varchar(1),
v2 varchar(4) not null,
v3 varchar(32) default 'NULL' not null,
i2 int,
v4 varchar(8),
v5 varchar(16) not null,
v6 varchar(1),
primary key (v2, v5) not droppable
)
attribute extent (1024, 1024), maxextents 15
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t003.3:
    stmt = """create index t003i11 on t003t1 (v2, v3, v5);"""
    output = _dci.cmdexec(stmt)
    
    # t003.5:
    stmt = """create view t003v11 as
select * from t003t1 where substring(v5,5,4) = v2;"""
    output = _dci.cmdexec(stmt)
    
    # t003.6:
    stmt = """create view t003v12 as select * from t003t1
where v4 = concat(v2, 'ABCD');"""
    output = _dci.cmdexec(stmt)
    
    # t003.7: 20 rows
    
    t003a_dat._init(_testmgr)
    
    # t003.8: 20 rows
    t003b_dat._init(_testmgr)
    
    # t003.9: 40 rows
    stmt = """select i1, v1, v2, cast(v3 as char(8)), i2, v4, v5, v6
from t003t1 order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s9""")
    
    # t003.10: 9 rows
    stmt = """select i1, v1, v2, cast(v3 as varchar(8)), i2, v4, v5, v6
from t003v11 order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s10""")
    
    # t003.11: 20 rows
    stmt = """select i1, v1, v2, cast(v3 as pic x(8)), i2, v4, v5, v6
from t003v12 order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s11""")
    
    # t003.15:
    stmt = """create table t003t2 (
chr1 char(1),              -- v1
vch1 varchar(8) not null,  -- v2 (key)
vch2 varchar(8),           -- v6 || v2
vch3 varchar(16) not null, -- v5 (key)
primary key (vch1,vch3) not droppable
)
attribute extent (1024, 1024), maxextents 15
store by primary key
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t003.16:
    stmt = """insert into t003t2 (
select v1, v2,
v6 || v2 || v1,
insert(v5,5,4,'0000')
from t003t1
where (v2 > '0000' and v2 < '0006')   -- 5 rows
or (substring(v5,5,4) > '0110' and -- 10 rows
substring(v5,1,4) < '0021')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 15)
    
    # t003.17:
    stmt = """select * from t003t2 order by vch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """t003s17""")
    
    # t003.20:
    # #runscript $test_dir/t003select
    # script: t003select
    # t003prepare.s01: 9 rows
    
    stmt = """showshape
select * from t003t1
where v2 = lpad(cast(i1 as varchar(4)),4,'0')
and substring(v5,1,4) < '0010' order by i1, v2, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s01 from
select * from t003t1
where v2 = lpad(cast(i1 as varchar(4)),4,'0')
and substring(v5,1,4) < '0010' order by i1, v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s01;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s01: 9 rows
    stmt = """execute s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s01""")
    
    # t003prepare.s02: 2 rows
    
    stmt = """showshape
select * from t003t1
where char(ascii(v2) + 20) = right(v4,1)
and i2 in (101, 111, 120, 130, 140) order by i1, v2, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s02 from
select * from t003t1
where char(ascii(v2) + 20) = right(v4,1)
and i2 in (101, 111, 120, 130, 140) order by i1, v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s02;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s02: 2 rows
    
    stmt = """execute s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t003prepare.s03: 5 rows
    
    stmt = """showshape
select v1 || v6 as v1n6, cast(v2 as decimal(7,2)) as v2dec,
substring(v5,5,4) as v5sub, ascii(v6) as v6asc
from t003t1
where left(v2,1) = right(trim(v3),1)
and v2 between '0015' and '0025' order by v2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s03 from
select v1 || v6 as v1n6, cast(v2 as decimal(7,2)) as v2dec,
substring(v5,5,4) as v5sub, ascii(v6) as v6asc
from t003t1
where left(v2,1) = right(trim(v3),1)
and v2 between '0015' and '0025' order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s03;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s03: 5 rows
    
    stmt = """execute s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t003prepare.s04: 3 rows: 0001, 0002, and 0040
    
    stmt = """showshape
select v1 || space(2) || v6 as v1spv6,
insert(v5,5,2,?p1) as v5i, v5
from t003t1
where locate(cast(i2 as varchar(3)),v5) = 6
and cast(v2 as int) > 39 or v2 < '0003' order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s04 from
select v1 || space(2) || v6 as v1spv6,
insert(v5,5,2,?p1) as v5i, v5
from t003t1
where locate(cast(i2 as varchar(3)),v5) = 6
and cast(v2 as int) > 39 or v2 < '0003' order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s04;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s04: 3 rows: 0001, 0002, and 0040
    
    stmt = """set param ?p1 'ZZ';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s04""")
    
    # t003prepare.s05: 1 rows: 0040
    
    stmt = """showshape
select * from t003t1
where position(cast(i1 as varchar(2)) in v4) = 3
and cast(v2 as int) > 39 or v2 < '0003' order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s05 from
select * from t003t1
where position(cast(i1 as varchar(2)) in v4) = 3
and cast(v2 as int) > 39 or v2 < '0003' order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s05;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s05: 1 rows: 0040
    
    stmt = """execute s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s05""")
    
    # t003prepare.s06:
    
    stmt = """showshape
select * from t003t1
where v2 = (select substring(vch3,1,4) from t003t2
where left(vch2,1) = 'a') order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s06 from
select * from t003t1
where v2 = (select substring(vch3,1,4) from t003t2
where left(vch2,1) = 'a') order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s06;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s06:
    
    stmt = """execute s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s06""")
    
    # t003prepare.s07:
    
    stmt = """showshape
select v2, vch1, v5, vch3
from t003t1 inner join t003t2
on v2 = substring(vch2,2,4) order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s07 from
select v2, vch1, v5, vch3
from t003t1 inner join t003t2
on v2 = substring(vch2,2,4) order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s07;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s07:
    
    stmt = """execute s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s07""")
    
    # t003prepare.s08:
    
    stmt = """showshape
select v1, v2, cast(v3 as char(8)), v4, v5, v6
from t003t1
where exists (
select * from t003t2
where v5 = repeat(substring(vch3,1,4),2)
)
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s08 from
select v1, v2, cast(v3 as char(8)), v4, v5, v6
from t003t1
where exists (
select * from t003t2
where v5 = repeat(substring(vch3,1,4),2)
)
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s08;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s08:
    
    stmt = """execute s08;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s08""")
    
    # t003prepare.s09:
    
    stmt = """showshape
select v1, vch1, v2, vch2, v5, vch3
from t003t2 left join t003t1
on chr1 = v1
where vch1 is NOT NULL
and v6   = 'a'
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s09 from
select v1, vch1, v2, vch2, v5, vch3
from t003t2 left join t003t1
on chr1 = v1
where vch1 is NOT NULL
and v6   = 'a'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s09;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s09:
    
    stmt = """execute s09;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s09""")
    
    # t003prepare.s10:
    
    stmt = """showshape
select v1,v2,v5,v6 from t003t1
where upper(v6) not in (select max(chr1) from t003t2)
order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s10 from
select v1,v2,v5,v6 from t003t1
where upper(v6) not in (select max(chr1) from t003t2)
order by v2, v5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s10;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s10:
    
    stmt = """execute s10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s10""")
    
    # t003prepare.s11: MDAM range predicate
    
    stmt = """set param ?p3 'NULL';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'ABCDEFGH';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showshape
select v1, v2, max(v5) from t003t1
where v1 = 'A' and v6 between 'a' and 'z' and
v3 = ?p3 and v4 = ?p4
group by v1, v2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s11 from
select v1, v2, max(v5) from t003t1
where v1 = 'A' and v6 between 'a' and 'z' and
v3 = ?p3 and v4 = ?p4
group by v1, v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s11;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s11: MDAM range predicate
    
    stmt = """set param ?p3 'NULL';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p4 'ABCDEFGH';"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/t003pexp s11
    stmt = """execute s11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # t003prepare.s12: MDAM IN list predicate
    
    stmt = """showshape
select i1, v1, v2, v6, sum(cast(v2 as int)) from t003t1
where v1 between 'a' and 'z'
and v2 in ('0025','0030','0035','0040')
and i2 in (125,135)
group by i1, v1, v2, v6
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s12 from
select i1, v1, v2, v6, sum(cast(v2 as int)) from t003t1
where v1 between 'a' and 'z'
and v2 in ('0025','0030','0035','0040')
and i2 in (125,135)
group by i1, v1, v2, v6
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s12;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s12: MDAM IN list predicate
    
    stmt = """execute s12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t003prepare.s13: MDAM - missing key column
    
    stmt = """showshape
select * from t003t1 where v2 = '0121';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s13 from
select * from t003t1 where v2 = '0121';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s13;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s13: MDAM - missing key column
    
    stmt = """execute s13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # t003prepare.s15: MDAM - DSS query
    
    stmt = """showshape
select avg(cast(substring(v5,1,4) as numeric(9))) as v5_avg
from t003t1
where v5 >= '00100100'
and v2 < substring(v5,1,4)
and v1 between 'A' and 'z'
and v6 between 'A' and 'Z'
and i1 < 100
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s15 from
select avg(cast(substring(v5,1,4) as numeric(9))) as v5_avg
from t003t1
where v5 >= '00100100'
and v2 < substring(v5,1,4)
and v1 between 'A' and 'z'
and v6 between 'A' and 'Z'
and i1 < 100
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s15;"""
    output = _dci.cmdexec(stmt)
    
    # t003select.s15: MDAM - DSS query
    
    stmt = """execute s15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003pexp""", """s15""")
    
    # t003.21:
    stmt = """control query default MDAM_SCAN_METHOD 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    # t003.22:
    # #runscript $test_dir/t003insert
    # script: t003insert
    # multiple varchar columns with two varchar columns in
    #   clustering key in nonadjacent order
    # t003insert.1: varchar keys in adjacent columns
    #   store by primary
    #expect purge
    
    # t003insert.1:
    stmt = """insert into t003t1 (i1, v2, v3, v5) values ( 99,
'0099', 'Denali National Park','aaaa0099bbbb0099');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # t003insert.2:
    stmt = """insert into t003t1 (i1, v1, v2, v3, v5) values (
50, '5', '0050', 'Mount McKinley', '00500050bbbb');"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.3:
    stmt = """insert into t003t1 (i1, v2, v3, i2, v5) values ( 98,
'0098','Denali Wilderness', 98, '0098bbbbBBBB0098');"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.4:
    stmt = """insert into t003t1 (i1, v1, v2, v3, v5) values ( 51,
'1', '0051', 'Denali State Park', '00510051bbbbBBBB');"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.5:
    stmt = """insert into t003t1 (i1, v2, v3, i2, v4, v5) values ( 97,
'0097','Wonder Lake', 97, 'McKinley', '0097');"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.6:
    stmt = """insert into t003t1 (i1, v2, v3, v4, v5, v6) values ( 52,
'0052', '0052', '0052', '0052', '5');"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.7:
    stmt = """insert into t003t1 (i1, v2, v3, v5, v6) values (
96, '0096', 'William McKinley', 'bbbb00960096', '5');"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.8:
    stmt = """insert into t003t1 (i1, v1, v2, v3, v5) values ( 53,
(select chr1 from t003t2 where vch1 = '0001'),              -- A
(select upper(vch1) from t003t2 where vch2 = 'a0001A'),     -- AA01
'A' || (select ucase(vch1) from t003t2 where chr1 = 'A') || 'A', -- AAA01A
'AA01AAAA');                                                -- AA01AAAA"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.9:
    stmt = """insert into t003t1 (i1, v1, v2, v3, v5) values ( 95,
(select chr1 from t003t2 where vch1 = '0002'),
(select vch1 from t003t2 where vch2 = 'b0002B'),
(select vch2 from t003t2 where vch3 like '0002%'),
(select vch3 from t003t2 where chr1 = 'B'));"""
    output = _dci.cmdexec(stmt)
    
    # t003insert.10:
    stmt = """insert into t003t1 (i1, v1, v2, v3, v5) values ( 55, 'k',
(select substring(vch2,3,4) from t003t2
where vch1 = '0011'), 'aa11',
(select concat(vch1,chr1) from t003t2
where vch2 = 'k0011K'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from t003t1
where v2 not between '0000' and '0040'
order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """ins01""")
    
    # t003insert.11:
    stmt = """insert into t003t1 (i1, v2, v3, v5, v6) values (
96, '0096', 'Edmund Hillary', 'bbbb00960096', '6');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8102')
    
    # t003.23:
    # #runscript $test_dir/t003update
    # script: t003update
    # multiple varchar columns with two varchar columns in
    #   clustering key in nonadjacent order
    # t003update.1: varchar keys in nonadjacent columns
    #   store by primary
    # t003update.1: update a single row with keys
    stmt = """update t003t1 set
i1 = 107,
v1 = 'A',
v3 = 'Alaska Range',
i2 = 107,
v4 = 'Mountain',
v6 = 'M'
where v2 = '0097' and v5 = '0097';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # t003update.2: update a single row
    stmt = """update t003t1 set
i1 = 105,
v1 = 'A',
v3 = 'Alaska Range',
i2 = 105,
v4 = 'Foraker',
v6 = 'F'
where i1 = 52
and v1 is NULL
and i2 is NULL
and v3 = v4
and v6 = '5';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from t003t1 where i1 = 105 or i1 = 107
order by i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """upds02""")
    
    # t003update.3: v2 in 0021 to 0040
    stmt = """update t003t1 set
v3 = v1 || v2 || v6
where v2 = substring(v4,1,4)
and v4 = concat(v2,'ABCD');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 9)
    
    stmt = """select v1,v2,v3,v6 from t003t1
where v2 = substring(v4,1,4)
and v4 = concat(v2,'ABCD') order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """upds03""")
    
    # t003update.5:
    stmt = """update t003t1 set
v1 = 'H',
v3 = 'Mount Everest',
v4 = 'Himalaya',
v6 = 'h'
where i2 in (101, 103, 105, 107, 109, 110)
and v2 < '0025' and substring(v5,5,4) < '0110';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 6)
    
    stmt = """select v1,v2,v3,v4,v5 from t003t1
where v1 = upper(v6)
and v3 = 'Mount Everest'
and v4 = 'Himalaya'
order by v1,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """upds05""")
    
    # t003update.7:
    stmt = """update t003t1 set
v1 = 'y',
v6 = 'Y'
where v3 = 'NULL' and v4 like '%ABCD%'
and v2 between '0019' and '0029'
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """select v1,v2,v3,v4,v6 from t003t1
where v1 = lower(v6) order by v1,v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """upds07""")
    
    # t003update.8:
    stmt = """update t003t1 set
i1 = 101,
v1 = 'r',
v3 = 'Mount Rainier',
i2 = 201,
v4 = 'WA',
v6 = 'R'
where v2 = '011K' and v5 = '0' || v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from t003t1 where i1 > 101 order by i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """upds08""")
    
    # t003update.9:
    # before R2.3 sut25 -> #expect any *4033*
    # mode_0: #expect any *ERROR[8402]*
    # mode_1: $SQL_updated_msg
    stmt = """update t003t1 set
v2 = 'Mt. Shasta' where v5 = '00400140';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8402')
    
    # t003update.10:
    stmt = """update t003t1 set
v4 = NULL where v3 = 'NULL' and v2 between '0010' and '0017';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 7)
    
    # t003update.11:
    stmt = """select * from t003t1 order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """upds11""")
    
    # t003.24:
    # #runscript $test_dir/t003delete
    # script: t003delete
    # multiple varchar columns with two varchar columns in
    #   clustering key in nonadjacent order
    # t003delete.1: varchar keys in nonadjacent columns
    #   store by primary
    # t003delete.1:  delete a single row on keys
    stmt = """delete from t003t1
where v2 = '0001' and v5 = v2 || v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # t003delete.2: delete a single row not on keys
    stmt = """delete from t003t1
where v3 = v1 || v2 || v6
and i2 = 21
and upper(v1) = v6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    # t003delete.3:
    stmt = """delete from t003t1
where v4 = concat('ABCD',v2)
and substring(v5,1,4) = v2
and v2 in ('0031','0035','0039','0042');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    # t003delete.4: delete not on keys
    stmt = """delete from t003t1
where v4 is NULL and v3 = 'NULL';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 7)
    
    # t003delete.5:
    stmt = """delete from t003t1
where v2 = substring(v4,1,4)
and v3 = v1 || v2 || v6
and v5 = concat(v2,v2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 8)
    
    # 30 rows
    # t003delete.6:
    stmt = """select * from t003t1 order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """dels01""")
    
    # 5 rows
    # t003delete.7:
    stmt = """insert into t003t1 (i1,v2,v3,v5)
(select ascii(chr1),vch1,vch2,vch3 from t003t2
where vch1 > '0015');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    # 35 rows
    # t003delete.8:
    stmt = """select * from t003t1 order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """dels02""")
    
    # t003delete.9:
    stmt = """delete from t003t1
where v5 = (select trim(vch3) from t003t2 where ascii(chr1) = 80)
or v5 = (select trim(vch3) from t003t2 where chr1 = 'T');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    # t003delete.10:
    stmt = """delete from t003t1
where v2 in (select vch1 from t003t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 12)
    
    # t003delete.11:
    stmt = """delete from t003t1
where v3 like 'Denali%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    # t003delete.12: 18 rows
    stmt = """select * from t003t1 order by v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t003exp""", """dels03""")
    
    # t003.25:
    stmt = """control query default MDAM_SCAN_METHOD reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control table * MDAM reset;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

