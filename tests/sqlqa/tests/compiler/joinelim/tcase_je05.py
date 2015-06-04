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
#  Description:        Reordering of left linear join tree
#
#  Purpose:            Test join elimination with reordering of left linear
#                      join trees. Use permutations of 3-way join with 1 RI
#                      constraint, permutations of 4-way join with 3 RI
#                      constraints.
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
    
def test001(desc="""((A Join1 B) Join2 C) with A(FK)->B(PK)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1 join t2 on fk12=pk2 join t3 on b1=b3;"""
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
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""((A Join1 C) Join2 B) with A(FK)->B(PK)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1 join t3 on b1=b3 join t2 on fk12=pk2;"""
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
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""((B Join1 A) Join2 C) with A(FK)->B(PK)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2 join t1 on fk12=pk2 join t3 on b1=b3;"""
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
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""((B Join1 C) Join2 A) with A(FK)->B(PK)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2 join t3 on b2=b3 join t1 on fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T3')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""((C Join1 B) Join2 A) with A(FK)->B(PK)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3 join t2 on b2=b3 join t1 on fk12=pk2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    _dci.expect_any_substr(output, '_scan*T3')
    
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '111')
    _dci.expect_any_substr(output, '112')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""((C Join1 A) Join2 B) with A(FK)->B(PK)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3 join t1 on b1=b3 join t2 on fk12=pk2;"""
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
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Join A,B,C,D with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t2,t3,t4 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test008(desc="""Join A,B,D,C with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t2,t4,t3 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test009(desc="""Join A,C,B,D with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t3,t2,t4 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test010(desc="""Join A,C,D,B with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t3,t4,t2 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test011(desc="""Join A,D,C,B with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t4,t3,t2 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test012(desc="""Join A,D,B,C with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t1,t4,t2,t3 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test013(desc="""Join B,A,C,D with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2,t1,t3,t4 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test014(desc="""Join B,A,D,C with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2,t1,t4,t3 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test015(desc="""Join B,C,A,D with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2,t3,t1,t4 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test016(desc="""Join B,C,D,A with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2,t3,t4,t1 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test017(desc="""Join B,D,A,C with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2,t4,t1,t3 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test018(desc="""Join B,D,C,A with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t2,t4,t3,t1 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test019(desc="""Join C,A,B,D with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3,t1,t2,t4 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test020(desc="""Join C,A,D,B with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3,t1,t4,t2 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test021(desc="""Join C,B,A,D with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3,t2,t1,t4 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test022(desc="""Join C,B,D,A with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3,t2,t4,t1 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test023(desc="""Join C,D,A,B with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3,t4,t1,t2 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test024(desc="""Join C,D,B,A with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t3,t4,t2,t1 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test025(desc="""Join D,A,B,C with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t4,t1,t2,t3 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test026(desc="""Join D,A,C,B with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t4,t1,t3,t2 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test027(desc="""Join D,B,A,C with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t4,t2,t1,t3 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test028(desc="""Join D,B,C,A with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t4,t2,t3,t1 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test029(desc="""Join D,C,A,B with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from
select a1 from t4,t3,t1,t2 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

def test030(desc="""Join D,C,B,A with A->B->C->D referential constraints"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s from
select a1 from t4,t3,t2,t1 where fk12=pk2 and fk23=pk3 and fk34=pk4;"""
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

