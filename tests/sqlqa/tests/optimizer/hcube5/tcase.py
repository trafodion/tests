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

# Modified Roger's hcube tests to our test format.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='6 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s1 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T8, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T7 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a<77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A01exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A01exp P2
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A01exp""", 'P3')
    
    ##expectstat $test_dir/A01exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc='6 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s2 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T8, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T7 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.b<7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A02exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A02exp P2
    stmt = """explain options 'f' s2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A02exp""", 'P3')
    
    ##expectstat $test_dir/A02exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc='8 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s3 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T8, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T4.b and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A03exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A03exp P2
    stmt = """explain options 'f' s3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A03exp""", 'P3')
    
    ##expectstat $test_dir/A03exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc='9 way almost linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s4 from select [last 0] * from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8 ,""" + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T10.a and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T10.c and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A04exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A04exp P2
    stmt = """explain options 'f' s4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    ##expectstat $test_dir/A04exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc='10 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s5 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10 where
 """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b and
 """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A05exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A05exp P2
    stmt = """explain options 'f' s5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A05exp""", 'P3')
    
    ##expectstat $test_dir/A05exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc='10 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s6 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10 where
 """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T8.b and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T5.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T7.b and
 """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.b and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A06exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A06exp P2
    stmt = """explain options 'f' s6;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A06exp""", 'P3')
    
    ##expectstat $test_dir/A06exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc='12 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s7 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b and
 """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A07exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A07exp P2
    stmt = """explain options 'f' s7;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A07exp""", 'P3')
    
    ##expectstat $test_dir/A07exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test008(desc='14 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s8 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b and
 """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b and s1.a=s2.b and
s2.a=s3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A08exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A08exp P2
    stmt = """explain options 'f' s8;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A08exp""", 'P3')
    
    ##expectstat $test_dir/A08exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc='16 way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s9 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as
s3,""" + gvars.g_schema_hcubedb + """.T4 as s4, """ + gvars.g_schema_hcubedb + """.T5 as s5 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b and
 """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b and s1.a=s2.b and
s2.a=s3.b and s3.a=s4.b and s4.a=s5.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A09exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A09exp P2
    stmt = """explain options 'f' s9;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A09exp""", 'P3')
    
    ##expectstat $test_dir/A09exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc='14 way circular'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s10 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b and
 """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b and s1.a=s2.b and
s2.a=s3.b and s3.a=""" + gvars.g_schema_hcubedb + """.T0.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A10exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A10exp P2
    stmt = """explain options 'f' s10;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A10exp""", 'P3')
    
    ##expectstat $test_dir/A10exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test011(desc='8 star (1 prime, 6 dimensions, 1 linear extension of a dimension)'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s11 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.CUBE1 where
 """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE1.a and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE1.b and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE1.c and
 """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE1.d and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.CUBE1.e and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE1.f and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T6.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A11exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A11exp P2
    stmt = """explain options 'f' s11;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A11exp""", 'P3')
    
    ##expectstat $test_dir/A11exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #prepare s from select  count(*) from t1,t2,t3,t4,t5,t6,t7,cube1 where
    #t1.a=cube1.a and t2.a=cube1.b and t3.a=cube1.c and
    #t4.a=cube1.d and t5.a=cube1.e and t6.a=cube1.f and t7.a=t6.b and
    #t1.c=1 and t2.c=1 and t3.c=1;
    
    _testmgr.testcase_end(desc)

def test012(desc='8 star 10 way snowflake of fully connected frindges'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s12 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T8, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5 where
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T9.c and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T9.c and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T9.c and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T9.b and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A12exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A12exp P2
    stmt = """explain options 'f' s12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A12exp""", 'P3')
    
    ##expectstat $test_dir/A12exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test013(desc='10 snowflake'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s13 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE1 where
 """ + gvars.g_schema_hcubedb + """.CUBE1.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.CUBE1.b=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.CUBE1.c=""" + gvars.g_schema_hcubedb + """.T7.c and
 """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T1.b and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T2.c and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T3.a and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T4.c and
 """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T5.a and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T6.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A13exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A13exp P2
    stmt = """explain options 'f' s13;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A13exp""", 'P3')
    
    ##expectstat $test_dir/A13exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test014(desc='11 snowflake'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s14 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE1 where
 """ + gvars.g_schema_hcubedb + """.CUBE1.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.CUBE1.b=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.CUBE1.c=""" + gvars.g_schema_hcubedb + """.T7.c and
 """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c and
 """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a and
 """ + gvars.g_schema_hcubedb + """.T0.a = """ + gvars.g_schema_hcubedb + """.T6.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A14exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A14exp P2
    stmt = """explain options 'f' s14;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A14exp""", 'P3')
    
    ##expectstat $test_dir/A14exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test015(desc='12 snowflake'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s15 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE1,""" + gvars.g_schema_hcubedb + """.T1 as s1 where
 """ + gvars.g_schema_hcubedb + """.CUBE1.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.CUBE1.b=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.CUBE1.c=""" + gvars.g_schema_hcubedb + """.T7.c and
 """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c and
 """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a and
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A15exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A15exp P2
    stmt = """explain options 'f' s15;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A15exp""", 'P3')
    
    ##expectstat $test_dir/A15exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test016(desc='14 way snow flake (with linear frindges)'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s16 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE1,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3 where
 """ + gvars.g_schema_hcubedb + """.CUBE1.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.CUBE1.b=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.CUBE1.c=""" + gvars.g_schema_hcubedb + """.T7.c and
 """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c and
 """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a and
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a and """ + gvars.g_schema_hcubedb + """.T2.b=s2.b and """ + gvars.g_schema_hcubedb + """.T3.b=s3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A16exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A16exp P2
    stmt = """explain options 'f' s16;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A16exp""", 'P3')
    
    ##expectstat $test_dir/A16exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test017(desc='16 way snow flake (with linear frindges)'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s17 from select  count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE1,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as
s3,""" + gvars.g_schema_hcubedb + """.T4 as s4, """ + gvars.g_schema_hcubedb + """.T5 as s5 where
 """ + gvars.g_schema_hcubedb + """.CUBE1.a=""" + gvars.g_schema_hcubedb + """.T9.a and """ + gvars.g_schema_hcubedb + """.CUBE1.b=""" + gvars.g_schema_hcubedb + """.T8.b and """ + gvars.g_schema_hcubedb + """.CUBE1.c=""" + gvars.g_schema_hcubedb + """.T7.c and
 """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c and
 """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c and
 """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a and
 """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a and """ + gvars.g_schema_hcubedb + """.T2.b=s2.b and """ + gvars.g_schema_hcubedb + """.T3.b=s3.b and """ + gvars.g_schema_hcubedb + """.T4.b=s4.b and """ + gvars.g_schema_hcubedb + """.T5.b=s5.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A17exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A17exp P2
    stmt = """explain options 'f' s17;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A17exp""", 'P3')
    
    ##expectstat $test_dir/A17exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test018(desc='12 flat fully connected'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
  
    stmt = """set schema """ +  gvars.g_schema_hcubedb + """;"""
    output = _dci.cmdexec(stmt);

    stmt = """prepare s18 from select  count(*) from t1,t2,t3,t4,t0 as t5,t1 as t6, t2 as t7,t3 as t8, t4 as t9,
t0 as t10, t1 as t11, t0 where
t0.a=t1.a and t1.a=t2.a and t2.a=t3.a and t3.a=t4.a and t4.a=t5.a and t5.a=t6.a
and t6.a=t7.a and t7.a=t8.a and t8.a=t9.a and t9.a=t10.a and t10.a=t11.a;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A18exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A18exp P2
    stmt = """explain options 'f' s18;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A18exp""", 'P3')
    
    ##expectstat $test_dir/A18exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test019(desc='16 flat fully connected'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set schema """ +  gvars.g_schema_hcubedb + """;"""
    output = _dci.cmdexec(stmt);
   
    stmt = """prepare s19 from select  count(*) from t1,t2,t3,t4,t0 as t5,t1 as t6, t2 as t7,t3 as t8, t4 as t9,
t0 as t10, t1 as t11, t2 as t12, t3 as t13, t4 as t14, t5 as t15, t0 where
t0.a=t1.a and t1.a=t2.a and t2.a=t3.a and t3.a=t4.a and t4.a=t5.a and t5.a=t6.a
and t6.a=t7.a and t7.a=t8.a and t8.a=t9.a and t9.a=t10.a and t10.a=t11.a
and t11.a=t12.a and t12.a=t13.a and t13.a=t14.a and t14.a=t15.a;""" 
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A19exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A19exp P2
    stmt = """explain options 'f' s19;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A19exp""", 'P3')
    
    ##expectstat $test_dir/A19exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

