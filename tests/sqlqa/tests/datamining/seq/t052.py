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
    
def test001(desc="""test052"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test052
    # Sequence function tests: test for FLOAT
    # 1. running functions
    #
    stmt = """select count (*) from vwseqtb52;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's1')
    # expect count = 100
    
    stmt = """select a, cast (b as dec (10,3)),
runningcount(b) as rcount_b,
cast (runningsum(b) as dec (18,3)) as rsum_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's2')
    # expect the count to run from 1-98 with dupes at rows 25 & 40
    # expect the sum at row 25 = 120320.0, 40 = 268956.3, 100 = 1627354.26
    
    stmt = """select a, cast (b as dec (10,3)),
cast (runningmax(b) as dec (10,3)) as rmax_b,
cast (runningmin(b) as dec (10,3)) as rmin_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's3')
    # expect runningmax at row 25 = 8859.43, 40 = 12415.47, 90 = 28339.32
    # expect the runningmin at all rows = 98.27
    
    stmt = """select a, cast (b as dec (10,3)) as col_b,
cast (runningsum(b) as dec (18,3)) as rsum_b,
cast(runningavg(b) as dec(18,3)) as ravg_b
from vwseqtb52 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's4')
    # expect runningsum at row 25 = 120320.0, 40 = 268956.3, 85 = 1186237.62
    # expect runningavg at row 25 = 5013.333, 40 = 7077.797, 85 = 14292.019
    
    #- gets divide by zero error XXXXX
    #- select a, cast (b as dec (10,3)),
    #-        cast (runningstddev(b) as dec (10,3)) as rstdev_b,
    #-        cast (runningvariance(b) as dec (10,3)) as rvar_b
    #-     from vwseqtb52
    #-       sequence by a;
    
    _testmgr.testcase_end(desc)

