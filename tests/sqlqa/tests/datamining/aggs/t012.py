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
    
def test001(desc="""test012"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test012
    # weights.sql
    # jclear
    # 22 Apr 1997
    # Test for the new aggreate functions.
    # Tests Variance and StdDev on a smallint column with 500 values.
    # Uses weighting, and DISTINCT, ALL and default (= ALL).
    #
    # test DISTINCT
    #select
    #    Variance (distinct small500, weight) as "PVarWtDis"
    #        from ints500;
    stmt = """select
Variance (distinct small500) as "PVarWtDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012exp""", 'test012a')
    # expect 1 row with the value 2359932.92339632
    
    stmt = """select
StdDev (distinct small500) as "PStDevWtDis"
from ints500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012exp""", 'test012b')
    # expect 1 row with the value 1536.20731784363
    
    # test ALL & default (= ALL)
    stmt = """select
Variance (all small500, weight) as "PVarWtAll",
Variance (small500, weight) as "PVarWt"
from weights;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012exp""", 'test012c')
    # expect 1 row with both PVar = 2.35993292339631590E+006
    
    stmt = """select
StdDev (all small500, weight) as "PStDevWtAll",
StdDev (small500, weight) as "PStDevWt"
from weights;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test012exp""", 'test012d')
    # expect 1 row with the both PStDev = 1.53620731784362870E+003
    #
    
    _testmgr.testcase_end(desc)

