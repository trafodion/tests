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
    
def test001(desc="""test061"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test061
    # Sequence function tests: test for DECIMAL
    # 1. running functions
    #
    stmt = """select count (*) from vwseqtb61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test061.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, b,
runningcount(b) as rcount_b,
runningsum(b) as rsum_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test061.exp""", 's2')
    # expect the count to run from 1-97 with dupes at rows 61, 74 & 82
    # expect the sum at row 30 = 469229.42, 61 = 951562.21, 100 = 1677240.91
    
    stmt = """select a, b,
runningmax(b) as rmax_b,
runningmin(b) as rmin_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test061.exp""", 's3')
    # expect the runningmax at row 31 = 32291.91, 50 = 32291.91, 97 = 32519.93
    # expect the runningmin at all rows = 366.27
    
    stmt = """select a, b,
runningsum(b) as rsum_b,
cast(runningavg(b) as dec(18,3)) as ravg_b
from vwseqtb61 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test061.exp""", 's4')
    # expect the runningsum at row 30 = 469229.42, 61 = 951562.21, 82 = 1338381.23
    # expect the runningavg at row 30 = 15640.98,  61 = 15859.37,  82 = 16941.535
    
    #- gets divide by zero error XXXXX
    #- select a, b,
    #-        runningstddev(b) as rstdev_b,
    #-        runningvariance(b) as rvar_b
    #-     from vwseqtb61
    #-       sequence by a;
    
    _testmgr.testcase_end(desc)

