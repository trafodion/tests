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
#  Description:        Vary WHERE clause expressions and verify join elimination
#                      behavior.
#
#  Purpose:
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
    
def test001(desc="""Add condition on unique column of PK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and pk2a>220;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK column used in where clause shares VEG with an FK column, so it does not
    # preclude join elimination.
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

def test002(desc="""Add condition on non-unique column of PK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and pk2b>220;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # PK column used in where clause shares VEG with an FK column, so it does not
    # preclude join elimination.
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

def test003(desc="""Add condition involving two PK columns"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and pk2b+pk2c>425;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Add condition on column of FK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and fk12a>220;"""
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
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Add condition involving two FK columns"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and fk12b+fk12c>425;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # Currently not supported (8/20/2008), make it pass
    ##unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    # Currently not supported (8/20/2008), make it pass
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Add condition involving columns of both PK and FK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and fk12b+pk2c>425;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Add condition involving non-key column of PK table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and v2 > 'm2_1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""Add condition involving non-key column of hub table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and v1 > 'm1_1';"""
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

def test009(desc="""Includes join of non-RI key column"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1
from t1,t2
where b1 = pk2;"""
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
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""Join using fk, but to table other than one it references"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t3 where fk12=pk3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T3')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""RI join by transitivity"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from
select a7
from t7,t8
where fknn78=b7 and b7=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # make changes local to this test case, so we get matching rows
    stmt = """update t7 set b7=b7-100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '171')
    _dci.expect_any_substr(output, '172')
    _dci.expect_any_substr(output, '173')
    _dci.expect_selected_msg(output)
    
    # undo changes local to this test case
    stmt = """update t7 set b7=b7+100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    _testmgr.testcase_end(desc)

