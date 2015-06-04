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
#  Description:        GROUP BY clause with join elimination.
#
#  Purpose:            Add GROUP BY to the test scenarios and verify join
#                      elimination behavior.
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
    
def test001(desc="""Group by unique column of PK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select max(fk12a)
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by pk2a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK grouping column shares VEG with an FK column, so it does not preclude
    # join elimination.
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Group by non-unique column of PK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select max(fk12a)
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by pk2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK grouping column shares VEG with an FK column, so it does not preclude
    # join elimination.
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Group by both unique and non-unique columns of PK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select max(fk12a)
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by pk2a, pk2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK grouping columns share VEGs with an FK columns, so they do not preclude
    # join elimination.
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Group by single column from FK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by fk12a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Group by multiple columns from FK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by fk12a, fk12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Group by unique column from PK and column from FK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12b
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by pk2a, fk12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK grouping column shares VEG with an FK column, so it does not preclude
    # join elimination.
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '212')
    _dci.expect_any_substr(output, '222')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Group by non-unique column from PK and column from FK."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12b
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by pk2b, fk12b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK grouping column shares VEG with an FK column, so it does not preclude
    # join elimination.
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '212')
    _dci.expect_any_substr(output, '222')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""GROUP BY with HAVING."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select max(fk12a)
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
group by pk2a
having pk2a>220;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK grouping column shares VEG with an FK column, so it does not preclude
    # join elimination.
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""GROUP BY on PK table alone in nested query (redundant join)."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1
from t1, (select pk2 from t2 group by pk2) as tbl2
where fk12 = tbl2.pk2;"""
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
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""GROUP BY on PK table alone in nested query (extra-hub)."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1, pk2
from t1, (select pk2 from t2 group by pk2) as tbl2
where fk12 = tbl2.pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '111 * 21')
    _dci.expect_any_substr(output, '112 * 21')
    _dci.expect_any_substr(output, '113 * 22')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""GROUP BY on non-PK column of PK table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select max(a1)
from t1, t2
where fk12 = pk2
group by b2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""GROUP BY with HAVING on non-PK column of PK table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select max(a1)
from t1, t2
where fk12 = pk2
group by b2
having b2 < 132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

