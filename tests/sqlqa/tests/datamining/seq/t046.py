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
    
def test001(desc="""test046"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test046
    # Sequence function tests: test for LARGEINT
    # 1. running functions
    #
    stmt = """select count (*) from vwseqtb46;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test046.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, b,
runningcount(b) as rcount_b,
cast (runningsum(b) as dec (18,0)) as rsum_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test046.exp""", 's2')
    # expect the count to run from 1-98 with dupes at the nulls in rows 46 & 88
    # expect the sum at row 17 = 20732333079, 57 = 72737818917, 99 = 114972315439
    
    stmt = """select a, b,
runningmax(b) as rmax_b,
runningmin(b) as rmin_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test046.exp""", 's3')
    # expect the runningmax at row 20 = 3177230455, 70-100 = 3226616552
    # expect the runningmin at row 20-100 = 172745
    
    stmt = """select a, b,
cast (runningsum(b) as dec (18,0)) as rsum_b,
cast(runningavg(b) as dec(18,3)) as ravg_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test046.exp""", 's4')
    # expect the sum at row 17 = 20732333079, 57 = 72737818917, 99 = 114972315439
    # expect the avg at row 17 = 1219549004, 57 = 1276102086, 99 = 1161336519
    
    stmt = """select a, b,
cast (runningstddev(b) as dec (13,3)) as rstdev_b,
cast (runningvariance(b) as largeint) as rvar_b
from vwseqtb46 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test046.exp""", 's5')
    # expect stddev at 17 = 655263485.451, 49 = 660621674.798, 73 = 647710489.216
    # var at 17 = 429370235365654..., 49 = 436420997213083..., 73 = 419528877841204...
    
    _testmgr.testcase_end(desc)

