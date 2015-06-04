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

import t02sql
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
    # INSERT/UPDATE/DELETE with NO ROLLBACK
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.1:
    stmt = """create table t12tabA (
a int not null, b int, c int,
d char(8), e varchar(8), f char(8),
v1 int not null,
v2 int not null,
v3 int not null,
v4 int not null,
v5 int not null
)
attribute extent (10240, 10240), maxextents 512
store by (a, v1, v2, v3, v4, v5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t12tabA;"""
    output = _dci.cmdexec(stmt)
    
    # t01.2:
    stmt = """prepare i1 from
insert with no rollback
into t12tabA (
select * from t12tab
transpose 0,1 as v1
transpose 1,2 as v2
transpose 2,3 as v3
transpose 3,4 as v4
transpose 11,12,13,14,15 as v5)
-- transpose 0,1,2,3,4,5,6,7,8,9,10,11 as v1
-- transpose 1,2,3,4,5,6,7,8,9,10,11,12 as v2
-- transpose 2,3,4,5,6,7,8,9,10,11,12,13 as v3
-- transpose 3,4,5,6,7,8,9,10,11,12,13,14 as v4
-- transpose 4,5,6,7,8,9,10,11,12,13,14,15 as v5)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t01.3:
    stmt = """explain i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    # t01.4:
    stmt = """execute i1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1200)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.5:
    stmt = """prepare u1 from
update with no rollback
t12tabA
set b = (select a from t12tab where c / a = b),
c = 12 ** 2,
f = (select e || f from t12tab where a = 15)
where v1 < 11 and v2 < 11 and v3 < 12 and v4 < 13 and v5 < 13
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t01.7:
    stmt = """explain u1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.8:
    stmt = """execute u1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 480)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.10:
    stmt = """prepare d1 from
delete with no rollback
from t12tabA where
v1 < 11 and v2 < 11 and v3 < 12 and v4 < 13 and v5 < 13
and a < 15
and c = (select a ** 2 from t12tab where b = 120)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t01.11:
    stmt = """explain d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t01.12:
    stmt = """execute d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 448)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t01.13:
    stmt = """select count(*) from t12tabA;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""t02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # CREATE TABLE AS
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    t02sql._init(_testmgr)
    
    # t02.1:
    ##expect any *${numRows}*
    stmt = """select count(*) from t02tabB;"""
    output = _dci.cmdexec(stmt)
    
    # t02.5:
    stmt = """prepare x from
insert with no rollback into t02tabB (
select * from t12tab
transpose 0 as v1
transpose 1,3,5,7 as v2
transpose 2,4,6,8 as v3
transpose 3,5,7,9 as v4
transpose 4,6,8,10 as v5
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t02.6:
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t02.7:
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3840)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t02.8:
    stmt = """showddl t02tabB;"""
    output = _dci.cmdexec(stmt)
    
    # t02.9:
    stmt = """select count(*) from t02tabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """5055""")
    
    # t02.11:
    stmt = """update with no rollback t02tabB
set b = (select a from t12tab where a = 1),
c = (select a from t12tab where a = 11),
d = (select d from t12tab where a = 15),
e = (select e from t12tab where c = 1000),
f = (select f from t12tab where b = 100)
where v1 < 100000 and v2 < 99 and v3 < 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4110)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # t02.14:
    stmt = """delete with no rollback from t02tabB
where d = (select d from t12tab where a = 15)
and e = (select e from t12tab where c = 1000)
and f = (select f from t12tab where b = 100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4110)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""t03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # CREATE TABLE AS
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table t031tab like """ + gvars.g_schema_wisc32 + """.ABASE;"""
    output = _dci.cmdexec(stmt)
    
    # t03.1:
    stmt = """prepare x1 from
insert with no rollback
into t031tab (select * from """ + gvars.g_schema_wisc32 + """.ABASE
where unique2 < 2000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    # where unique2 < 2000000);
    
    # t03.2:
    stmt = """explain x1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t03.3:
    stmt = """execute x1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2000)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t03.5:
    stmt = """select count(*) from t031tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """2000""")
    
    stmt = """drop table t032tab;"""
    output = _dci.cmdexec(stmt)
    
    # t03.6: expected savepoint on
    stmt = """prepare x2 from
create table t032tab store by (unique2) AS (
select * from """ + gvars.g_schema_wisc32 + """.ABASE
where unique2 = unique1
and stringu1 = stringu2
and unique3 < 3200)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' x2;"""
    output = _dci.cmdexec(stmt)
    
    # t03.7:
    stmt = """explain x2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute x2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t03.10:
    stmt = """select count(*) from t032tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """0""")
    
    _testmgr.testcase_end(desc)

def test004(desc="""t04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # CREATE TABLE AS
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t04.1: 5 million rows from wisconsin table
    stmt = """prepare x from
create table t04tab store by (unique2) AS (
select * from """ + gvars.g_schema_wisc32 + """.ABASE
where unique2 < 5000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' x;"""
    output = _dci.cmdexec(stmt)
    
    # t04.2:
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from t04tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """5000""")
    
    # t04.4:
    stmt = """showddl t04tab;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """alter table t04tab add column a1 int default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table t04tab add column a2 varchar(3) default 'abc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """alter table t04tab add column a3 char(2) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t04.6:
    stmt = """prepare u1 from
update with no rollback
t04tab set
ten = 10,
onepercent    = 10 * 10,
twentypercent = 10 ** 2,
stringu1 = substring('stringu1',1,8),
stringu2 = substring('stringu1stringu2',9,8),
a3 = 'A3'
where unique2 < 2500
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*) from t04tab where a1 = 100 and a2 = 'abc' and a3 is NULL;"""
    output = _dci.cmdexec(stmt)
    
    # t04.7:
    stmt = """explain u1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t04.8:
    stmt = """execute u1;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t04.10:
    stmt = """prepare u2 from
update
t04tab set
ten = two + four,
onepercent    = tenpercent,
twentypercent = tenpercent,
stringu1 = 'stringu1',
stringu2 = substring('stringu1',1,7) || '2',
a3 = 'a3'
where unique2 < 2500
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t04.11:
    stmt = """explain u2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t04.12:
    stmt = """execute u2;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # t04.15: result depends on autoabort in TMF
    # it could be "Never" if TMF autoabort is 0 (never abort) or
    # given time as in tmfs4 if TMF autoabort is not 0.
    stmt = """prepare d1 from
delete with no rollback
from t04tab
where a1 = (select c from t12tab where c / a = 100 and d = 'd1')
and a2 = 'abc'
and a3 is NULL
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t04.16:
    stmt = """explain d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t04.17:
    stmt = """execute d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2500)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""t05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # INSERT ... SELECT
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t05.1:
    stmt = """create table t05tab like """ + gvars.g_schema_wisc32 + """.ABASE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t05.2:
    stmt = """prepare x from
insert with no rollback
into t05tab (
select * from """ + gvars.g_schema_wisc32 + """.ABASE
where unique2 < 3750);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t05.3:
    stmt = """explain x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t05.4:
    stmt = """execute x;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3750)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl t05tab;"""
    output = _dci.cmdexec(stmt)
    
    # t05.7:
    stmt = """alter table t05tab add column a1 int default 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t05.8:
    stmt = """alter table t05tab add a2 varchar(3) default 'abc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t05.9:
    stmt = """alter table t05tab add column a3 char(2) default null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t05.10:
    stmt = """prepare u1 from
update with no rollback
t05tab set
ten = 1 * 10,
onepercent   =  10,
twentypercent = 10 ** 2,
stringu1 = substring('stringu30000',1,8),
stringu2 = substring('0000stringu3',5,8),
a3 = 'A3'
where unique2 < 2500 and unique1 = unique3
for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t05.11:
    stmt = """explain u1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # t05.12:
    stmt = """execute u1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2500)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t05.13:
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select [last 1] * from """ + gvars.g_schema_wisc32 + """.ABASE
where unique2 < 12500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # t05.14:
    stmt = """prepare s1 from
select [last 1] * from """ + gvars.g_schema_wisc32 + """.ABASE
where unique2 < 12500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t05.15:
    stmt = """explain s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t05.16: read only transaction
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    # t05.18:
    stmt = """prepare d1 from
delete with no rollback
from t05tab
where a1 = 100
and a2 = 'abc'
and a3 is NULL
and stringu1 <> 'stringu3'
and stringu2 <> 'stringu3'
and twentypercent < 2000
and oddonepercent = evenonepercent + 1
and unique2 < 4750
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # t05.19:
    stmt = """explain d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # t05.20:
    stmt = """execute d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1250)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # t05.22:
    stmt = """select count(*) from t05tab;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """2500""")
    
    _testmgr.testcase_end(desc)

