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
    
def test001(desc="""test040"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test040
    # Sequence function tests: test for INT
    # 1. running functions
    #
    stmt = """select count (*) from vwseqtb40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test040.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningsum(b) as rsum_b
from vwseqtb40 
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test040.exp""", 's2')
    # expect the count to run from 1-100
    # expect the sum at row 29 = 121497, 71 = 716343, 100 = 1499159
    
    stmt = """select a, b,
runningmax(b) as rmax_b,
runningmin(b) as rmin_b
from vwseqtb40 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test040.exp""", 's3')
    # expect the runningmax at row 29 = 7577, 71 = 21089, 90 = 28558
    # expect the runningmin at all rows = 38
    
    stmt = """select a, b,
runningcount(b) as rcount_b,
cast(runningavg(b) as dec(18,3)) as ravg_b
from vwseqtb40 
sequence by a asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test040.exp""", 's4')
    # expect the count to run from 1-98, with 2 @ 28 and 2 @ 69
    # expect the runningavg at row 29 = 4339.17, 71 = 10381.78, 85 = 12660.08
    
    stmt = """select a, b,
cast (runningstddev(b) as dec (18,3)) as rstdev_b,
cast (runningvariance(b) as dec (18,3)) as rvar_b
from vwseqtb40 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test040.exp""", 's5')
    # expect stdd at 10 = 967.034, 30 = 2732.752, 72 = 6348.450, 97 = 9151.332
    # var at 10 = 935155.122, 30 = 7467938.378, 72 = 40302822.503 , 97 = 83746893.875
    
    _testmgr.testcase_end(desc)

