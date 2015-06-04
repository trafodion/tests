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
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: READ UNCOMMITTED.
    # READ ONLY transaction: n/a
    # Autoabort interval   : n/a
    # No_Abort_On_Capacity : n/a
    
    stmt = """prepare s01 from
select avg(tA.a+tB.v1) as t_avg
from t01tabA tA, t01tabB tB where tA.a = tB.v1
for read uncommitted access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't01exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""t02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: browse access.
    # READ ONLY transaction: n/a
    # Autoabort interval   : n/a
    # No_Abort_On_Capacity : n/a
    
    stmt = """prepare s02 from
select * from vw_avg for browse access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't02exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""t03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: READ COMMITTED.
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """prepare s03 from
select avg(tA.a+tB.v1) as t_avg, sum(tA.a+tB.v1) as t_sum
from t01tabA tA, t01tabB tB where tA.a = tB.v1
for read committed access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't03exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""t04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: SERIALIZABLE
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """prepare s04 from
select * from vw_avg for serializable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't04exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""t05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: REPEATABLE READ
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """prepare s05 from
select avg(tA.a+tB.v1) as t_avg
from t01tabA tA, t01tabB tB where tA.a = tB.v1
for repeatable read access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't05exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc="""t06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: STABLE
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """prepare s06 from
select * from vw_avg  for stable access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't06exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc="""t07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # isolation level: SKIP CONFLICT.
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """prepare s07 from
select * from vw_avg for skip conflict access;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s07;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't07exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""t11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # SET TRANSACTION      : READ UNCOMMITTED
    # READ ONLY transaction: n/a
    # Autoabort interval   : n/a
    # No_Abort_On_Capacity : n/a
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s11 from
select * from vw_avg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt = """execute s11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't11exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""t12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # SET TRANSACTION      : READ COMMITTED, READ ONLY
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED, READ ONLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """showcontrol query default ISOLATION_LEVEL, match partial;"""
    output = _dci.cmdexec(stmt)
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s12 from
select avg(tA.a+tB.v1) as t_avg
from t01tabA tA, t01tabB tB where tA.a = tB.v1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't12exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""t13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # SET TRANSACTION      : SERIALIZABLE, READ ONLY
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """SET TRANSACTION ISOLATION LEVEL SERIALIZABLE, READ ONLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """showcontrol query default ISOLATION_LEVEL, match partial;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s13 from select * from vw_sum ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't13exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""t14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # SET TRANSACTION      : REPEATABLE READ, READ ONLY
    # READ ONLY transaction: Yes
    # Autoabort interval   : 0
    # No_Abort_On_Capacity : Yes
    
    stmt = """SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s14 from
select avg(tA.a+tB.v1) as t_avg
from t01tabA tA, t01tabB tB where tA.a = tB.v1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't14exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""t15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Pure SELECT. AUTOCOMMIT OFF.
    # SET TRANSACTION      : AUTOCOMMIT OFF
    # isolation level      : READ COMMITTED.
    # READ ONLY transaction: no
    # Autoabort interval   : system default
    # No_Abort_On_Capacity : no
    # Expecting transaction complete successfully.
    
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s15 from select * from vw_avg;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't15exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""t16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Non-pure SELECT. AUTOCOMMIT ON
    # READ ONLY transaction: no
    # Autoabort interval   : system default
    # No_Abort_On_Capacity : no
    # Expecting transaction complete successfully.
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    
    # Can't use [last 0] with in an embedded update/delete statement
    stmt = """prepare s16 from
select a, b, c
from (update t01tabA set b = a+v1+v2+v3+v4+v5 where a > 1) as temp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc="""t17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Non-pure SELECT. AUTOCOMMIT ON
    # SET TRANSACTION      : default
    # READ ONLY transaction: no
    # Autoabort interval   : system default
    # Expecting transaction complete successfully.
    
    stmt = """create table t01tabC like t01tabA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s17 from
select * from
(insert into t01tabC (select * from t01tabA where a < 10)) as temp
order by 1,2,3,4,5,6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s17;"""
    output = _dci.cmdexec(stmt)

    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """show reccount;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't17exe')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""t18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # pure SELECT. AUTOCOMMIT ON.
    # SET TRANSACTION      : READ WRITE
    # READ ONLY transaction: Yes
    # Autoabort interval   : system default
    # Expecting transaction complete successfully.
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION READ WRITE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s18 from
select sum(a) as tempSUM
from (select tA.a from t01tabA tA, t01tabB tB
where tA.a = tB.v1) as temp
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't18exe')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""t19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Non-pure SELECT. AUTOCOMMIT ON.
    # SET TRANSACTION      : READ WRITE
    # READ ONLY transaction: No
    # Autoabort interval   : system default
    # No_Abort_On_Capacity : No
    # Expecting transaction complete successfully.
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION READ WRITE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s19 from
select a,b,c
from (delete from t01tabA where a < 10) as temp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain s19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """execute s19;"""
    output = _dci.cmdexec(stmt)

    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """show reccount;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/t01exp""", 't19exe')
    
    stmt = """showtransaction;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

