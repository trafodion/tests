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

#opt/hcube2/testcase
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='Linear query for Hcube 6-way'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.CUBE2 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE2.b
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a<77;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.CUBE2 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE2.b
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a<77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A01exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A01exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A01exp P3
    #execute xx;
    
    # #expectstat $test_dir/A01exp P4
    # display statistics;
    
    _testmgr.testcase_end(desc)

def test002(desc='Linear query for Hcube 8-way'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.d=""" + gvars.g_schema_hcubedb + """.CUBE2.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.e=""" + gvars.g_schema_hcubedb + """.CUBE2.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.f=""" + gvars.g_schema_hcubedb + """.CUBE2.c
and """ + gvars.g_schema_hcubedb + """.CUBE2.e=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.d=""" + gvars.g_schema_hcubedb + """.CUBE2.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.e=""" + gvars.g_schema_hcubedb + """.CUBE2.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.f=""" + gvars.g_schema_hcubedb + """.CUBE2.c
and """ + gvars.g_schema_hcubedb + """.CUBE2.e=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A02exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A02exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A02exp""", 'P3')
    
    ##expectstat $test_dir/A02exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc='HCUBE 9-way almost linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T10.a
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T10.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T10.a
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T10.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A03exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A03exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A03exp""", 'P3')
    
    ##expectstat $test_dir/A03exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc='HCUBE 10-way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 
where  """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 
where  """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A04exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A04exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A04exp""", 'P3')
    
    ##expectstat $test_dir/A04exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc='HCUBE 10-way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 
where  """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.T3.c=""" + gvars.g_schema_hcubedb + """.CUBE3.c
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T5.c=""" + gvars.g_schema_hcubedb + """.T2.c
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE2.b
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.T4.c
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T4.a < 2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10 
where  """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.T3.c=""" + gvars.g_schema_hcubedb + """.CUBE3.c
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T5.c=""" + gvars.g_schema_hcubedb + """.T2.c
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE2.b
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.T4.c
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T4.a < 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A05exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A05exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A05exp P3
    #execute xx;
    
    # NCI #expectstat $test_dir/A05exp P4
    # NCI display statistics;
    
    _testmgr.testcase_end(desc)

def test006(desc='HCUBE 12-way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.CUBE2,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.CUBE2,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A06exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A06exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A06exp""", 'P3')
    
    ##expectstat $test_dir/A06exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc='HCUBE 14-way linear(CO)'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.CUBE2,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3
where """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b
and s1.a=s2.b
and s2.a=s3.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.CUBE2,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3
where """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b
and s1.a=s2.b
and s2.a=s3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A07exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A07exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A07exp""", 'P3')
    
    ##expectstat $test_dir/A07exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test008(desc='HCUBE 16-way linear'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10,
 """ + gvars.g_schema_hcubedb + """.T1 as s1, """ + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3, """ + gvars.g_schema_hcubedb + """.T4 as s4, """ + gvars.g_schema_hcubedb + """.T5 as s5
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b
and s1.a=s2.b
and s2.a=s3.b
and s3.a=s4.b
and s4.a=s5.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T3, """ + gvars.g_schema_hcubedb + """.T4, """ + gvars.g_schema_hcubedb + """.T5, """ + gvars.g_schema_hcubedb + """.T6, """ + gvars.g_schema_hcubedb + """.CUBE2, """ + gvars.g_schema_hcubedb + """.CUBE3, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T10,
 """ + gvars.g_schema_hcubedb + """.T1 as s1, """ + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3, """ + gvars.g_schema_hcubedb + """.T4 as s4, """ + gvars.g_schema_hcubedb + """.T5 as s5
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE2.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.CUBE2.b=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.CUBE2.c=""" + gvars.g_schema_hcubedb + """.CUBE3.f
and """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b
and s1.a=s2.b
and s2.a=s3.b
and s3.a=s4.b
and s4.a=s5.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A08exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A08exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A08exp""", 'P3')
    
    ##expectstat $test_dir/A08exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test009(desc='HCUBE star 7-way'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #(1 prime, 6 dimensions, 1 linear extension of a dimension) 7-way
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.CUBE3 
where  """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE3.a
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE3.c
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE3.f;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.CUBE3 
where  """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE3.a
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE3.c
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE3.d
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.CUBE3.e
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE3.f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A09exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A09exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A09exp""", 'P3')
    
    ##expectstat $test_dir/A09exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test010(desc='HCUBE 8-way snowflake with fringes'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.CUBE1 
where  """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE1.a
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE1.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE1.c
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE1.d
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.CUBE1.e
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE1.f
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T1.c=1
and """ + gvars.g_schema_hcubedb + """.T2.c=1
and """ + gvars.g_schema_hcubedb + """.T3.c=1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.CUBE1 
where  """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.CUBE1.a
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.CUBE1.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.CUBE1.c
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.CUBE1.d
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.CUBE1.e
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.CUBE1.f
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T1.c=1
and """ + gvars.g_schema_hcubedb + """.T2.c=1
and """ + gvars.g_schema_hcubedb + """.T3.c=1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A10exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A10exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A10exp""", 'P3')
    
    ##expectstat $test_dir/A10exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test011(desc='HCUBE 10-way snowflake with connected fringes'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T8, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T9.c
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T9.c
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T9.c
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.a;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0, """ + gvars.g_schema_hcubedb + """.T9, """ + gvars.g_schema_hcubedb + """.T1, """ + gvars.g_schema_hcubedb + """.T8, """ + gvars.g_schema_hcubedb + """.T2, """ + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5 
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T9.c
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T9.c
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T9.c
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A11exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A11exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A11exp""", 'P3')
    
    ##expectstat $test_dir/A11exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test012(desc='HCUBE 12-way snowflake'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T1 as s1
where  """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.b=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T7.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b
and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a
and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a
and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a
and """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a
and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T1 as s1
where  """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.b=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T7.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b
and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a
and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a
and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a
and """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a
and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A12exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A12exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A12exp""", 'P3')
    
    ##expectstat $test_dir/A12exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test013(desc='HCUBE 14-way snow flake (with linear fringes)'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3
where  """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.b=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T7.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b
and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a
and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a
and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a
and """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a
and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a
and """ + gvars.g_schema_hcubedb + """.T2.b=s2.b
and """ + gvars.g_schema_hcubedb + """.T3.b=s3.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3
where  """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.b=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T7.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b
and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a
and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a
and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a
and """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a
and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a
and """ + gvars.g_schema_hcubedb + """.T2.b=s2.b
and """ + gvars.g_schema_hcubedb + """.T3.b=s3.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A13exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A13exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A13exp""", 'P3')
    
    ##expectstat $test_dir/A13exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test014(desc='HCUBE 14-way circular'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b
and s1.a=s2.b
and s2.a=s3.b
and s3.a=""" + gvars.g_schema_hcubedb + """.T0.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*) from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.T10,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3
where  """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T1.b
and """ + gvars.g_schema_hcubedb + """.T1.a=""" + gvars.g_schema_hcubedb + """.T2.b
and """ + gvars.g_schema_hcubedb + """.T2.a=""" + gvars.g_schema_hcubedb + """.T3.b
and """ + gvars.g_schema_hcubedb + """.T3.a=""" + gvars.g_schema_hcubedb + """.T4.b
and """ + gvars.g_schema_hcubedb + """.T4.a=""" + gvars.g_schema_hcubedb + """.T5.b
and """ + gvars.g_schema_hcubedb + """.T5.a=""" + gvars.g_schema_hcubedb + """.T6.b
and """ + gvars.g_schema_hcubedb + """.T6.a=""" + gvars.g_schema_hcubedb + """.T7.b
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T9.b
and """ + gvars.g_schema_hcubedb + """.T9.a=""" + gvars.g_schema_hcubedb + """.T10.b
and """ + gvars.g_schema_hcubedb + """.T10.a=s1.b
and s1.a=s2.b
and s2.a=s3.b
and s3.a=""" + gvars.g_schema_hcubedb + """.T0.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A14exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A14exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A14exp""", 'P3')
    
    ##expectstat $test_dir/A14exp P4
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test015(desc='HCUBE 16-way snow flake (with linear fringes)'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showshape
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3,""" + gvars.g_schema_hcubedb + """.T4 as s4, """ + gvars.g_schema_hcubedb + """.T5 as s5
where  """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.b=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T7.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b
and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a
and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a
and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a
and """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a
and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a
and """ + gvars.g_schema_hcubedb + """.T2.b=s2.b
and """ + gvars.g_schema_hcubedb + """.T3.b=s3.b
and """ + gvars.g_schema_hcubedb + """.T4.b=s4.b
and """ + gvars.g_schema_hcubedb + """.T5.b=s5.b;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare xx from
select count(*)
from """ + gvars.g_schema_hcubedb + """.T0,""" + gvars.g_schema_hcubedb + """.T1,""" + gvars.g_schema_hcubedb + """.T2,""" + gvars.g_schema_hcubedb + """.T3,""" + gvars.g_schema_hcubedb + """.T4,""" + gvars.g_schema_hcubedb + """.T5,""" + gvars.g_schema_hcubedb + """.T6,""" + gvars.g_schema_hcubedb + """.T7,""" + gvars.g_schema_hcubedb + """.T8,""" + gvars.g_schema_hcubedb + """.T9,""" + gvars.g_schema_hcubedb + """.CUBE3,""" + gvars.g_schema_hcubedb + """.T1 as s1,""" + gvars.g_schema_hcubedb + """.T2 as s2, """ + gvars.g_schema_hcubedb + """.T3 as s3,""" + gvars.g_schema_hcubedb + """.T4 as s4, """ + gvars.g_schema_hcubedb + """.T5 as s5
where  """ + gvars.g_schema_hcubedb + """.CUBE3.a=""" + gvars.g_schema_hcubedb + """.T9.a
and """ + gvars.g_schema_hcubedb + """.CUBE3.b=""" + gvars.g_schema_hcubedb + """.T8.b
and """ + gvars.g_schema_hcubedb + """.CUBE3.c=""" + gvars.g_schema_hcubedb + """.T7.c
and """ + gvars.g_schema_hcubedb + """.T9.b=""" + gvars.g_schema_hcubedb + """.T0.b
and """ + gvars.g_schema_hcubedb + """.T9.c=""" + gvars.g_schema_hcubedb + """.T1.c
and """ + gvars.g_schema_hcubedb + """.T8.a=""" + gvars.g_schema_hcubedb + """.T2.a
and """ + gvars.g_schema_hcubedb + """.T8.c=""" + gvars.g_schema_hcubedb + """.T3.c
and """ + gvars.g_schema_hcubedb + """.T7.a=""" + gvars.g_schema_hcubedb + """.T4.a
and """ + gvars.g_schema_hcubedb + """.T7.b=""" + gvars.g_schema_hcubedb + """.T5.a
and """ + gvars.g_schema_hcubedb + """.T0.a=""" + gvars.g_schema_hcubedb + """.T6.a
and """ + gvars.g_schema_hcubedb + """.T1.a=s1.a
and """ + gvars.g_schema_hcubedb + """.T2.b=s2.b
and """ + gvars.g_schema_hcubedb + """.T3.b=s3.b
and """ + gvars.g_schema_hcubedb + """.T4.b=s4.b
and """ + gvars.g_schema_hcubedb + """.T5.b=s5.b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectstat $test_dir/A15exp P1
    # NCI display statistics;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan $test_dir/A15exp P2
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A15exp P3
    #execute xx;
    
    # #expectstat $test_dir/A15exp P4
    # display statistics;
    
    _testmgr.testcase_end(desc)

