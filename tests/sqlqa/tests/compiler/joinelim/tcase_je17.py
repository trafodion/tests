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
#  Description:        Constant folding no-ops combined with join elimination.
#
#  Purpose:            Use various combinations of constant boolean
#                      expressions that can be evaluated at compile time
#                      ANDed or ORed with foreign key equijoins leading to
#                      join elimination or marking of extra-hub tables.
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
    
def test001(desc="""Constant folding removes 2nd AND operand and enables join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 and 2>1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *file_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Constant folding removes 1st AND operand and enables join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where 2>1 and fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *file_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Constant folding removes 2nd OR operand and enables join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 or 2>3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Constant folding removes 1st OR operand and enables join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where 2>3 or fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Constant folding renders WHERE clause false."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # No join elimination occurs, but file scans have false local predicate.
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 and 2>3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T1')
    _dci.expect_any_substr(output, '_scan*T2')
    stmt = """explain s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'executor_predicates .... 0.')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Constant folding renders WHERE clause true."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # No join elimination occurs
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 or 2>1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T1')
    _dci.expect_any_substr(output, '_scan*T2')
    
    _testmgr.testcase_end(desc)

def test007(desc="""Constant folding removes reducing predicate, allowing join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 and (b2>10 or 'abc' = 'abc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test008(desc="""Where clause evalustes to false, no join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where 2>3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    _testmgr.testcase_end(desc)

def test009(desc="""Equijoin ANDed with comparison of constant and dynamic parameter."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # 2nd AND operand can't be evaluated at compile-time, so there is no constant
    # folding and no join elimination.
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 and 2>?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    _testmgr.testcase_end(desc)

def test010(desc="""Constant folding removes obstacle to join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2 where fk12=pk2 and (b2=7 or 2>1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test011(desc="""Folded constant used in boolean expr with AND, OR, and NOT results in removing reducing predicate and allows join elimination"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2
where fk12=pk2 or (a2>10 and not(2>1 or b2=8));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test012(desc="""Folded constants cause all parts of predicates to be eliminated except join condition, allowing join elimination"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from select a1 from t1,t2
where (a2>5 and 3+4=12 and a2<99) or fk12=pk2 and (b2>10 or b2<0 or 6=6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

