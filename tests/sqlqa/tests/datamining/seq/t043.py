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
    
def test001(desc="""test043"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test043
    # Sequence function tests: test for SMALLINT
    # 1. running functions
    #
    stmt = """select count (*) from vwseqtb43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test043.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, c,
runningcount(c) as rcount_c,
runningsum(c) as rsum_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test043.exp""", 's2')
    # expect the count to run from 1-100
    # expect the sum at row 17 = 62368, 56 = 582084, 100 = 1681560
    
    stmt = """select a, c,
runningmax(c) as rmax_c,
runningmin(c) as rmin_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test043.exp""", 's3')
    # expect the runningmax at row 20 = 8809, 60 = 20909, 95 = 29915
    # expect the runningmin at all rows = 437
    
    stmt = """select a, c,
runningsum(c) as rsum_c,
cast(runningavg(c) as dec(18,3)) as ravg_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test043.exp""", 's4')
    # expect the sum at row 17 = 62368,   56 = 582084,  100 = 1681560
    # expect the avg at row 17 = 3668.70, 56 = 10583.34, 85 = 14881.89
    
    stmt = """select a, c,
cast (runningstddev(c) as dec (13,3)) as rstdev_c,
cast (runningvariance(c) as dec (13,3)) as rvar_c
from vwseqtb43 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test043.exp""", 's5')
    # expect stddev at row 4 = 454.408, 15 = 1925.196, 55 = 5620.760, 86 = 7967.628
    # expect var at row 4 = 206487, 15 = 3706380.41, 55 = 31592942.712, 86 = 63483088.187
    
    _testmgr.testcase_end(desc)

