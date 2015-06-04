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
    
def test001(desc="""test010"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test010
    # distall.sql
    # jclear
    # 22 Apr 1997
    # Test for DISTINCT & ALL in the new aggreate functions.
    # Tests Variance &  StDev with DISTINCT, ALL, and default (= ALL)
    # on a smallint column with 500 values, 10 of which are duplicates.
    #
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    # Prep: create 5 duplicate rows
    # 1. copy row 30's values to row 50
    stmt = """update ints500 
set small500 = 454, int500 = 421757431
where counter = 50;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # 2. copy row 130's values to row 150
    stmt = """update ints500 
set small500 = 4490, int500 = 473915955
where counter = 150;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # 3. copy row 230's values to row 250
    stmt = """update ints500 
set small500 = 3859, int500 = 1765741615
where counter = 250;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # 4. copy row 330's values to row 350
    stmt = """update ints500 
set small500 = 1184, int500 = 339448811
where counter = 350;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # 5. copy row 430's values to row 450
    stmt = """update ints500 
set small500 = 4146, int500 = 1946918247
where counter = 450;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # Now test DISTINCT
    # (more than one DISTINCT aggregate is not supported,
    # so we do them all separately)
    #
    stmt = """select
Count (distinct small500) as "CountDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010f')
    # expect 1 row with the value 495
    
    stmt = """select
Avg (distinct small500) as "AverageDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010g')
    # expect 1 row with the value 2394.2868686868...
    
    stmt = """select
Sum (distinct small500) as "SumDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010h')
    # expect 1 row with the value 1185172
    
    stmt = """select
Variance (distinct small500) as "VarDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010i')
    # expect 1 row with the value 2.14781268677053970E+006
    
    stmt = """select
Min (distinct small500) as "MinDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010j')
    # expect 1 row with the value 4
    
    stmt = """select
StdDev (distinct small500) as "StDevDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010k')
    # expect 1 row with the value 1.46554177244135210E+003
    
    stmt = """select
Max (distinct small500) as "MaxDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010l')
    # expect 1 row with the value 4994
    
    # Now test ALL
    
    stmt = """select
Count (all small500) as "CountAll",
Avg (all small500) as "AverageAll",
Sum (all small500) as "SumAll",
Variance (all small500) as "VarAll",
Min (all small500) as "MinAll",
StdDev (all small500) as "StDevAll",
Max (all small500) as "MaxAll"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010m')
    # expect 1 row with the following values:
    # 	Count = 500
    # 	Avg = 2398.61
    # 	Sum = 1199305
    # 	Var = 2156003.06002004
    # 	Min = 4
    # 	StDev = 1468.33342944307
    # 	Max = 4994
    #
    # Now test with no DISTINCT or ALL
    
    stmt = """select
Count (small500) as "CountAll",
Avg (small500) as "AverageAll",
Sum (small500) as "SumAll",
Variance (small500) as "VarAll",
Min (small500) as "MinAll",
StdDev (small500) as "StDevAll",
Max (small500) as "MaxAll"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test010exp""", 'test010n')
    
    # expect 1 row with the following values:
    # 	Count = 500
    # 	Avg = 2398.61
    # 	Sum = 1199305
    # 	Var = 2156003.06002004
    # 	Min = 4
    # 	StDev = 1468.33342944307
    # 	Max = 4994
    #
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

