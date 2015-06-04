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
#  Test case name:       JoinElim01
#
#  Description:          Variation in Select list with join elimination.
#
#  Purpose:              Vary the SELECT clause of queries with redundant joins
#                        or extra-hub tables, and verify elimination of the
#                        redundant joins and marking of the extra-hub tables.
#
#  Special Instructions: If the default value for MULTI_PASS_JOIN_ELIM_LIMIT
#                        changes (current default is 5), some of the expected
#                        results in test cases A01, A02, and A03 will have to
#                        be changed, or the setup file could be amended to set
#                        the value of the CQD to the old default value.
#
#                        The algorithm used currently finds at most 1 extra-hub
#                        table, so some extra-hub tables are left as part of
#                        the hub. If this is fixed, some expected results from
#                        tests A01-A03 will need to be changed.
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
    
def test001(desc="""Successively add columns from join tables to the select list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
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
    
    # t2 and t3 preserved because of limit on number of times SQL entered
    # (determined by value of MULTI_PASS_JOIN_ELIM_LIMIT).
    #unexpect any *_scan*T4*
    #unexpect any *_scan*T5*
    #unexpect any *_scan*T6*
    #unexpect any *_scan*T7*
    #unexpect any *_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T3')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_any_substr(output, 'scan*.T3')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2
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
    
    #unexpect any *file_scan*T4*
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a3
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
    
    #unexpect any *file_scan*T4*
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    # The algorithm used currently only finds 1 extra-hub table, so t2 is listed as
    # a hub even though it really isn't.
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a3, a4
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
    
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a3, a4, a5
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
    
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a3, a4, a5, a6
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
    
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a3, a4, a5, a6, a7
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
    
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a3, a4, a5, a6, a7, a8
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
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_any_substr(output, '.T8')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Combinations of join tables represented in select list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1, a4
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
    
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T3')
    _dci.expect_any_substr(output, 'scan*.T4')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a4
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
    
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T3')
    _dci.expect_any_substr(output, 'scan*.T4')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a8
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
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_any_substr(output, '.T8')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a8
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
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_any_substr(output, '.T8')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a2, a5, a7
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
    
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Use series of joins with Not Null foreign keys.
    stmt = """prepare s from
select a5,a6
from t5,t6,t7,t8
where fknn56=pk6
and fknn67=pk7
and fknn78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '151 * 161')
    _dci.expect_any_substr(output, '152 * 161')
    _dci.expect_any_substr(output, '153 * 162')
    _dci.expect_any_substr(output, '154 * 162')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Try several Select list combinations with From clause reversed."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *file_scan*T4*
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1,a2
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *file_scan*T4*
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1,a2,a3,a4,a5
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a1, a4
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *file_scan*T5*
    #unexpect any *file_scan*T6*
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a6
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *file_scan*T7*
    #unexpect any *file_scan*T8*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a8
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T8')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select a4, a8
from t8,t7,t6,t5,t4,t3,t2,t1
where fk12=pk2
and fk23=pk3
and fk34=pk4
and fk45=pk5
and fk56=pk6
and fk67=pk7
and fk78=pk8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T1')
    _dci.expect_any_substr(output, '.T2')
    _dci.expect_any_substr(output, '.T3')
    _dci.expect_any_substr(output, '.T4')
    _dci.expect_any_substr(output, '.T5')
    _dci.expect_any_substr(output, '.T6')
    _dci.expect_any_substr(output, '.T7')
    _dci.expect_selected_msg(output)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '.T8')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Foreign key column only"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12
from t1,t2
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '21')
    _dci.expect_any_substr(output, '21')
    _dci.expect_any_substr(output, '22')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Unique key column only; allows join elim because of sharing VEG with FK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select pk2
from t1,t2
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '21')
    _dci.expect_any_substr(output, '21')
    _dci.expect_any_substr(output, '22')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Unique key only from composite PK; allows join elim, same as above"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select pk2a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Non-unique key columns only from composite PK; allows join elim as above"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select pk2b, pk2c
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '212 * 213')
    _dci.expect_any_substr(output, '212 * 213')
    _dci.expect_any_substr(output, '222 * 223')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""Both unique and non-unique key columns from composite PK; allows join elim as above"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select pk2a, pk2b, pk2c
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211 * 212 * 213')
    _dci.expect_any_substr(output, '211 * 212 * 213')
    _dci.expect_any_substr(output, '221 * 222 * 223')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""Select foreign key columns only"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a, fk12b, fk12c
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M1')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211 * 212 * 213')
    _dci.expect_any_substr(output, '211 * 212 * 213')
    _dci.expect_any_substr(output, '221 * 222 * 223')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""Only unique key column from PK and any column from FK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Once again, the pk is in a VEG with the FK, so t2 is not needed to compute
    # the output list.
    stmt = """prepare s from
select pk2a, v1
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211*m1_1')
    _dci.expect_any_substr(output, '211*m1_2')
    _dci.expect_any_substr(output, '221*m1_3')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""Combination of columns from both PK and FK"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Once again, the pk is in a VEG with the FK, so t2 is not needed to compute
    # the output list.
    stmt = """prepare s from
select pk2a, pk2b, pk2c, fk12a, fk12b, fk12c
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211 * 212 * 213 * 211 * 212 * 213')
    _dci.expect_any_substr(output, '211 * 212 * 213 * 211 * 212 * 213')
    _dci.expect_any_substr(output, '221 * 222 * 223 * 221 * 222 * 223')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""Aggregate function in Select list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from select count(*) from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3')
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from select count(a1) from t1,t2 where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3')
    _dci.expect_selected_msg(output)
    
    # t2 not currently marked as extra-hub in this example, but Suresh may change
    # the way it works.
    stmt = """prepare s from select count(a2) from t1,t2 where fk12=pk2;"""
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
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3')
    _dci.expect_selected_msg(output)
    
    # t2 not currently marked as extra-hub in this example, but Suresh may change
    # the way it works.
    stmt = """prepare s from select count(a1), count(a2) from t1,t2 where fk12=pk2;"""
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
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '3 * 3')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""Select no columns from either table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select ' '
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M1')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc="""Partial key join"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M1')
    _dci.expect_any_substr(output, 'scan*.M2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_any_substr(output, '251')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""Non-equijoin to redundant table"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c>=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M1')
    _dci.expect_any_substr(output, 'scan*.M2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '211')
    _dci.expect_any_substr(output, '221')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""Non-equijoin to table represented in Select list"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12a, v2
from m1, m2
where fk12a=pk2a and fk12b=pk2b and fk12c>=pk2c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*M2')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M1')
    _dci.expect_any_substr(output, 'scan*.M2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '211*m2_1')
    _dci.expect_any_substr(output, '211*m2_1')
    _dci.expect_any_substr(output, '221*m2_2')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test017(desc="""Add DISTINCT to Select list (introduces a groupby node)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # Although DISTINCT is used in the subquery, a groupby node will not be
    # generated (because pk2 is unique), so join elimination will occur.
    stmt = """prepare s from
select a1
from t1, (select distinct pk2 from t2) x
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    # Adding a2 to the Select list of the subquery makes it a grouping column for
    # DISTINCT, so there will be a groupby node even though the presence of pk2 in
    # the Select list ensures distinctness of the subquery result. This makes a2 an
    # essential output, so the join to t2 will not be eliminated.
    stmt = """prepare s from
select a1
from t1, (select distinct pk2, a2 from t2) x
where fk12=pk2;"""
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
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_any_substr(output, '113')
    _dci.expect_selected_msg(output)
    
    # This uses the same subquery Select list as the previous query, but DISTINCT
    # has been removed. Thus, there is no groupby node, and there are no essential
    # outputs from t2, so that table and the join to it are eliminated.
    stmt = """prepare s from
select a1
from t1, (select pk2, a2 from t2) x
where fk12=pk2;"""
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
    
    # The DISTINCT is used in the Select list of the main query, so the groupby
    # node will be above the join. a2 is used as a grouping column, and so is an
    # essential output, preventing the join from being eliminated and t2 from being
    # an extra-hub table.
    stmt = """prepare s from
select distinct a2
from t1,t2
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '121')
    _dci.expect_any_substr(output, '122')
    _dci.expect_selected_msg(output)
    
    # Same as above, but a1 is used in the Select list instead of a2, so a2 is no
    # longer an essential output needed in the groupby node, and join elimination
    # will occur.
    stmt = """prepare s from
select distinct a1
from t1,t2
where fk12=pk2;"""
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

def test018(desc="""Select list column that makes table non-redundant used in an expression"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12, sqrt(a2)
from t1,t2
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '21 * 11.')
    _dci.expect_any_substr(output, '21 * 11.')
    _dci.expect_any_substr(output, '22 * 11.')
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
select fk12, case fk12 when 1 then 2 when 2 then 3 when a2 then 10 else 100 end
from t1,t2
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '21 * 100')
    _dci.expect_any_substr(output, '21 * 100')
    _dci.expect_any_substr(output, '22 * 100')
    _dci.expect_selected_msg(output)
    
    stmt = """prepare s from
-- Note: a1 - a2 behaves differently (no extra-hub); waiting for info from Suresh
select fk12 - a2
from t1,t2
where fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2')
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '-100')
    _dci.expect_any_substr(output, '-100')
    _dci.expect_any_substr(output, '-100')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test019(desc="""PK in Select list, same VEG as FK (does not prevent join elimination)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select fk12, pk2
from t1,t2
where fk12=pk2;"""
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
    _dci.expect_any_substr(output, '21 * 21')
    _dci.expect_any_substr(output, '21 * 21')
    _dci.expect_any_substr(output, '22 * 22')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

