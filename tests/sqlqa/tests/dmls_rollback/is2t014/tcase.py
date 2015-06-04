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
    
def test001(desc="""t01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Illegal syntax for INSERT statement
    
    stmt = """create table t14tabA ( a1 int not null, a2 int) store by (a1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table t14tabB ( a1 int not null, a2 int) store by (a1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t14tabA values (1,2),(3,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into t14tabB values (4,3),(2,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """drop table t14tab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t14tab ( a1 int not null, a2 int) store by (a1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.1
    stmt = """insert with rollback
into t14tab (select * from t14tabA);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.2
    stmt = """insert no rollback into t14tab values (5,50);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.3
    stmt = """insert no rollback on into t14tab (a1,a2) values (6,60);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.4
    stmt = """insert with rollback into t14tab values (5,55);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.5
    stmt = """insert rollback into t14tab (a1) values (7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.6
    stmt = """insert rollback -1
into t14tab values (5,6),(7,8),(9,10),(11,12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.7
    stmt = """insert with no rollback off
into t14tab (select t14tabA.a1, t14tabB.a2 from t14tabA, t14tabB);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.8
    stmt = """insert with no backout into t14tab (a1) values (7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.9
    stmt = """insert with no into t14tab (a1) values (8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.10
    stmt = """insert without rollback
into t14tab (select a.a1, b.a1 from t14tabA a, t14tabB b
where a.a1 = b.a1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.11
    stmt = """insert with no rollbacks
into t14tab (select * from t14tabB sample random 80 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.12
    stmt = """insert with no rollbacks
into t14tab (a1,a2) values (10,10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.13
    stmt = """insert with no rollback on
into t14tab (select * from t14tabA);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.14
    stmt = """insert into t14tab (select * with no rollback from t14tabA);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.15
    stmt = """insert into t14tab with no rollback (
select * from t14tabA sample first 10 rows sort by a2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.16
    stmt = """insert with no rollback into t14tab (
select with no rollback * from t14tabB);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.17
    stmt = """alter table with no rollback t14tab add column a1 int default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t01.18
    stmt = """prepare x from
insert into t14tab (select * from t14tabB);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute with no rollback x;"""
    output = _dci.cmdexec(stmt)
    # This error message does not have ERROR[15001] header.
    _dci.expect_any_substr(output, 'A syntax error occurred at or before')
    
    stmt = """execute x with no rollback;"""
    output = _dci.cmdexec(stmt)
    # This error message does not have ERROR[15001] header.
    _dci.expect_any_substr(output, 'A syntax error occurred at or before')
    
    # t01.19
    stmt = """prepare x from
insert with no rollbacks
into t14tab (select * from t14tabB sample random 80 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select count(*) from t14tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t14exp""", 't14s1')
    
    stmt = """select count(*) from t14tabA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t14exp""", 't14s2')
    
    stmt = """select count(*) from t14tabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t14exp""", 't14s3')
    
    _testmgr.testcase_end(desc)

def test002(desc="""t02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Illegal syntax for UPDATE statement
    
    stmt = """create table t02tabA (a1 int not null, a2 int) store by (a1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t02tabA values (1,2),(3,4),(5,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    
    stmt = """create table t02tab (
a1 int not null,
a2 int,
v1 int,
v2 int) store by (a1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into t02tab (
select * from t02tabA
transpose 0,1,2,3,4,5,6,7,8,9 as v1
transpose 0,1,2,3,4,5,6,7,8,9 as v2
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 300)
    
    stmt = """select count(*) from t02tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """300""")
    
    # t02.1
    stmt = """update with rollback
t02tab set a2 = a1 where a2 < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.2
    stmt = """update no rollback
t02tab set v1 = a1 + a2 where v1 <> v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.3
    stmt = """update no rollback on
t02tab set a2 = a1,
v1 =  a1 + a2
where v2 > 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.4
    stmt = """update with no roll back
t02tab set a2 = v2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.5
    stmt = """update rollback
t02tab set a2 = v1 * v2 where a1 = 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.6
    stmt = """update rollback -1
t02tab set a2 = -1, v1 = v2 where a1 = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.7
    stmt = """update with no backout
t02tab set v1 = (a1 + a2) * 10 where a1 = 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.8
    stmt = """update with no
t02tab set v2 = 120 / v1 where v1 > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.9
    stmt = """update without rollback
t02tab set a2 = v2 * v1 where v2 between 1 and 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.10
    stmt = """update with no rollback on
t02tab set a2 = a1 * v1 * v2 where v1 > 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.11
    stmt = """update with rollback off
t02tab set v1 = a1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.12
    stmt = """update t02tab with no rollback
set v1 = a1 * a2 where v2 = 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.13
    stmt = """update rollback on t02tab set v2 = a1 + a2 + v1 where v2 = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.14
    stmt = """update with -1 t02tab set
a2 = -1,
v1 = -1,
v2 = -1 where (a1 + a2) > 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.15
    stmt = """update witho no rollback t02tab set v1 = v2 where a2 > 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.16
    stmt = """update t02tab set v1 = 100 with no rollback where v2 < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t02.17
    stmt = """prepare x from
update no rollback t02tab set v1 = 100 where v2 < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # mxci:$err_msg 15017 X
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    
    # t02.l8
    stmt = """prepare x from
update with no rollback t02tab set v1 = a1 + a2 where v2 < 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3233')
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    
    stmt = """select count(*) from t02tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """300""")
    
    _testmgr.testcase_end(desc)

def test003(desc="""t03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Illegal syntax for DELETE statement
    
    # t03.1
    stmt = """delete with rollback 0
from t03tab where unique1 = unique2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.2
    stmt = """delete no rollback
from t03tab where (two, four, ten, twenty) = (0,0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.3
    stmt = """delete no rollback on
from t03tab where onepercent < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.4
    stmt = """delete rollback
from t03tab where unique3 = unique1 and unique2 < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.5
    stmt = """delete rollback -1
from t03tab where stringu2 like 'AAAABZ%' or stringu2 like 'AAAAAZ%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.6
    stmt = """delete with no delete
from t03tab where unique2 between 1999 and 2001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.7
    stmt = """delete with
from t03tab where (two, four, ten, twenty) = (1,1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.8
    stmt = """delete with no rollbacks
from t03tab where evenonepercent + 1 = oddonepercnt and
unique2 between 1001 and 1100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.9
    stmt = """delete -1 from t03tab where twenty > 12 and ten < 5 and unique2 < 1000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.10
    stmt = """delete with rollback on
from t03tab where onepercent between 77 and 87 and
unique2 between 700 and 1200;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.11
    stmt = """delete from t03tab with no rollback where unique1 < 10000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.12
    stmt = """delete rollback ON from t03tab where unique2 in (1,100,200,300,400,500);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.13
    stmt = """delete with rollback off from t03tab where (unique1 / 10000) < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # t03.14
    stmt = """prepare x from
delete from t03tab with no rollback where unique1 < 10000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

