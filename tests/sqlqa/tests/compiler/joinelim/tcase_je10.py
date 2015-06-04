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
#  Description:        RI models
#
#  Purpose:            Test the effects of join elimination and extra-hub
#                      marking on different patterns of referential integrity
#                      constraints, such as:
#                        -- Multiple tables referencing single table, e.g., A->C, B->C
#                        -- Single table referencing multiple tables, e.g., A->B, A->C
#                        -- RI chains, e.g., A->B->C.  These are used extensively in
#                           other tests, so only special cases are handled in this unit.
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
    
def test001(desc="""Multiple tables referencing single table with join elimination"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1y
from t1y, t1x, t1, t2
where fk1x2=pk2 and fk1y2=pk2 and fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *scan*.T2*
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Multiple tables referencing single table, join conditions ORed"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1y
from t1y, t1x, t1, t2
where fk1x2=pk2 or fk1y2=pk2 or fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # no join elimination
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Multiple tables referencing single table with partial key joins"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Note in the following query component columns of 2 different foreign keys are
    # compared to the referenced table's PK columns.
    stmt = """prepare s from
select v1
from m1, m1x, m2
where fk12a=pk2a and fk12b=pk2b and fk1x2c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # no join elimination
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Multiple tables referencing single table with composite foreign keys with join elimination"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select m1.v1
from m1, m1x, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and fk1x2a=pk2a and fk1x2b=pk2b and fk1x2c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Multiple tables referencing single extra-hub table with composite foreign keys"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select m1.v1, m2.v2
from m1, m1x, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c
and fk1x2a=pk2a and fk1x2b=pk2b and fk1x2c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M2')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Multiple tables referencing single table in 3-way join, only 1 join condition"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1x
from t1x, t1y, t2
where fk1x2=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *scan*.T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Vary MULTI_PASS_JOIN_ELIM_LIMIT with long chains of unnecssary RI joins"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Enter SQO only once, only one join will be eliminated.
    stmt = """control query default MULTI_PASS_JOIN_ELIM_LIMIT '1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s from
select a1
from t1,t2,t3,t4,t5,t6,t7,t8
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T3')
    _dci.expect_any_substr(output, '_scan*T4')
    _dci.expect_any_substr(output, '_scan*T5')
    _dci.expect_any_substr(output, '_scan*T6')
    _dci.expect_any_substr(output, '_scan*T7')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #===
    
    # Specifying 0 should be same as 1; SQO must be entered at least once.
    stmt = """control query default MULTI_PASS_JOIN_ELIM_LIMIT '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s from
select a1
from t1,t2,t3,t4,t5,t6,t7,t8
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T3')
    _dci.expect_any_substr(output, '_scan*T4')
    _dci.expect_any_substr(output, '_scan*T5')
    _dci.expect_any_substr(output, '_scan*T6')
    _dci.expect_any_substr(output, '_scan*T7')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #===
    
    stmt = """control query default MULTI_PASS_JOIN_ELIM_LIMIT '7';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s from
select a1
from t1,t2,t3,t4,t5,t6,t7,t8
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    #unexpect any *_scan*T3*
    #unexpect any *_scan*T4*
    #unexpect any *_scan*T5*
    #unexpect any *_scan*T6*
    #unexpect any *_scan*T7*
    #unexpect any *_scan*T8*
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
    _dci.expect_selected_msg(output)
    
    #===
    
    stmt = """control query default MULTI_PASS_JOIN_ELIM_LIMIT '2';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s from
select a1
from t1,t2,t3,t4,t5,t6,t7,t8
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T7*
    #unexpect any *_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T3')
    _dci.expect_any_substr(output, '_scan*T4')
    _dci.expect_any_substr(output, '_scan*T5')
    _dci.expect_any_substr(output, '_scan*T6')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_any_substr(output, 'scan*.T3')
    _dci.expect_any_substr(output, 'scan*.T4')
    _dci.expect_any_substr(output, 'scan*.T5')
    _dci.expect_any_substr(output, 'scan*.T6')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    #===
    
    # Negative value means no limit on number of joins eliminated.
    stmt = """control query default MULTI_PASS_JOIN_ELIM_LIMIT '-1';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """prepare s from
select a1
from t1,t2,t3,t4,t5,t6,t7,t8
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    #unexpect any *_scan*T3*
    #unexpect any *_scan*T4*
    #unexpect any *_scan*T5*
    #unexpect any *_scan*T6*
    #unexpect any *_scan*T7*
    #unexpect any *_scan*T8*
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
    _dci.expect_selected_msg(output)
    
    #===
    
    # Put the CQD back to its default setting.
    stmt = """control query default MULTI_PASS_JOIN_ELIM_LIMIT reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""Single table referencing multiple tables through unnecessary joins"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1x
from t1x, t2, t1y
where fk1x1y=pk1y and fk1x2=pk2;"""
    output = _dci.cmdexec(stmt)
    
    #unexpect any *_scan*T2*
    #unexpect any *_scan*T1Y*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1X')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""Single table referencing multiple extra-hub tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1x, a2, a1y
from t1x, t2, t1y
where fk1x1y=pk1y and fk1x2=pk2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T1X')
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T1Y')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1X')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_any_substr(output, 'scan*.T1Y')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

