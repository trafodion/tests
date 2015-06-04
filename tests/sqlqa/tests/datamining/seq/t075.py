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
    
def test001(desc="""test075"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test075
    # Sequence function tests: test for INTERVAL
    # 1. running functions
    #
    stmt = """select count (*) from vwseqtb75;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test075.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningsum(b) as rsum_b
from vwseqtb75 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test075.exp""", 's2')
    # expect the count to run from 1-100
    # expect the sum at row 29 = 121497, 71 = 716343, 100 = 1499159
    
    stmt = """select a, b,
runningmax(b) as rmax_b,
runningmin(b) as rmin_b
from vwseqtb75 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test075.exp""", 's3')
    # expect the runningmax at row 29 = 7577, 71 = 21089, 90 = 28558
    # expect the runningmin at all rows = 38
    
    stmt = """select a, b,
runningcount(b) as rcount_b,
cast(runningavg(b) as dec(18,3)) as ravg_b
from vwseqtb75 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test075.exp""", 's4')
    # expec tthe count to run from 1-98, with 2 @ 28 and 2 @ 69
    # expect the runningavg at row 25 = 1943.091, 71 = 1967.701, 85 = 1974.926
    
    stmt = """select a, b,
cast (runningstddev (cast (b as int)) as dec (18,3)) as rstdev_b,
cast (runningvariance (cast (b as int)) as dec (18,3)) as rvar_b
from vwseqtb75 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test075.exp""", 's5')
    # expect the following values:
    # at line 10 :  Variance is 10.678,     StdDev is 3.268
    # at line 30 :  Variance is 352629.352, StdDev is 593.826
    # at line 50 :  Variance is 287755.889, StdDev is 536.429
    # at line 72 :  Variance is 206540.044, StdDev is 454.467
    # at line 97 :  Variance is 157479.625, StdDev is 396.837
    # at line 100:  Variance is 153195.566, StdDev is 391.402
    
    _testmgr.testcase_end(desc)

