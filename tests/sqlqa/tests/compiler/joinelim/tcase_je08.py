# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# =================  Begin Test Case Header  ==================
#
#  Description:        Join elimination queries using subqueries.
#
#  Purpose:
#
#
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Use subqueries instead of tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1
from (select * from t1) x1,
(select * from t2) x2,
(select * from t3) x3,
(select * from t4) x4
where fk12=pk2 and fk23=pk3 and fk34 = pk4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    #unexpect any *_scan*T3*
    #unexpect any *_scan*T4*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/expectFile""", 'a1')
    
    _testmgr.testcase_end(desc)

def test002(desc="""Use subquery with eliminated table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1
from (select * from t1) x1,
(select * from t2) x2,
(select * from t3,t4 where fk34=pk4) x3,
(select * from t4) x4
where fk12=pk2 and fk23=pk3 and fk34 = x4.pk4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    #unexpect any *_scan*T3*
    #unexpect any *_scan*T4*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/expectFile""", 'a1')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Use nested query that is equivalent to redundant join"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1
where fk12 in (select pk2 from t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/expectFile""", 'a1')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Use nested query that would be equivalent to redundant join, except for added condition"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1
where fk12 in (select pk2 from t2 where fk23=31);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Results don't come out in same order as a1 section in expectFile.
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Series of nested queries/redundant joins"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1
where fk12 in (select pk2 from t2
where fk23 in (select pk3 from t3
where fk34 in (select pk4 from t4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    #unexpect any *_scan*T3*
    #unexpect any *_scan*T4*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/expectFile""", 'a1')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Series of nested queries/redundant joins with composite keys"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select v1 from m1
where (fk12a, fk12b,fk12c) in (select pk2a,pk2b,pk2c from m2
where (fk23a, fk23b,fk23c) in (select pk3a,pk3b,pk3c from m3
where (fk34a, fk34b,fk34c) in (select pk4a,pk4b,pk4c from m4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    #unexpect any *_scan*M3*
    #unexpect any *_scan*M4*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'm1_1')
    _dci.expect_any_substr(output, 'm1_2')
    _dci.expect_any_substr(output, 'm1_3')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Foreign key renamed in subquery"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from (select a1,fk12 as z from t1) x, t2 where z=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/expectFile""", 'a1')
    
    _testmgr.testcase_end(desc)

def test008(desc="""Foreign key used in expr in subquery, expr given FK name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from (select a1,fk12+1 as fk12 from t1) x, t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    # Results don't come out in same order as a1 section in expectFile.
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

