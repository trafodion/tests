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
    
    # TRAF stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, READ WRITE;"""
    # TRAF output = _dci.cmdexec(stmt)
    
    stmt = """create table t01tab (
a int not null, b int, c int,
d char(10), e char(10), f char(10)
)
attribute extent (1024, 1024), maxextents 12
store by (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """delete from t01tab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t01tab values (1,10,100,'d1','e1','f1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """create table t01tabA (
a int not null, b int, c int,
d char(10), e char(10), f char(10),
v1 int not null,
v2 int not null,
v3 int not null,
v4 int not null,
v5 int not null
)
attribute extent (2048, 10240), maxextents 512
store by (a, v1, v2, v3, v4, v5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """showddl t01tabA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table t01tabB;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table t01tabB (
a int not null, b int, c int,
d char(2), e char(2), f char(2),
v1 int not null,
v2 int not null,
v3 int not null,
v5 int not null
)
attribute extent (1024, 1024), maxextents 512
store by (a,v1,v2,v3,v5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """showddl t01tabB;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from t01tabA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert with no rollback
into t01tabA (
select * from t01tab
transpose 0,1,2,3,4,5,6,7,8,9 as v1
transpose 10,11,12,13,14,15,16,17,18,19 as v2
transpose 0,100,200,300,400,500,600,700,800,900 as v3
transpose 30,31,32,33,34,35,36,37,38,39 as v4
transpose 10 as v5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10000)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into t01tab values (2,20,200,'d2','e2','f2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """delete from t01tabB;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert with no rollback
into t01tabB (
select * from t01tab
transpose 0,1,2,3,4,5,6,7,8,9 as v1
transpose 10,11,12,13,14,15,16,17,18,19 as v2
transpose 10,11,12,13,14,15,16,17,18,19 as v3
transpose 10 as v5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2000)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table t01tabA on every column;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table t01tabB on every column;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idxt01A on t01tabA (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idxt01A2 on t01tabA (v1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idxt01B on t01tabB (a);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index idxt01B2 on t01tabB (v1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vw_avg as
select avg(tA.a+tB.v1) as t_avg
from t01tabA tA, t01tabB tB where tA.a = tB.v1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vw_sum as
select sum(a) as tempSUM
from (select tA.a from t01tabA tA, t01tabB tB
where tA.a = tB.v1) as temp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
