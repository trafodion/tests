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
    
def test001(desc="""test002"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test002
    # Sequence function tests: based on the 2nd example from the External Specs.
    #
    stmt = """SELECT RUNNINGCOUNT (*) as rc_star,
B,
C,
RUNNINGSUM (C) as rsum,
cast (RUNNINGAVG (C) as dec (18,2)) as ravg,
MOVINGSUM (C, 5) as mvsum,
cast (MOVINGAVG (C, 5) as dec (18,2)) as mvavg,
RUNNINGMAX (B) as runmax,
---     MOVINGMAX (B, 5) as mvmax, Gets Error while fetching from the TCB tree.
dt
FROM seqtb1 
SEQUENCE BY dt
;"""
    output = _dci.cmdexec(stmt)
    # expect 33 rows in order
    # expect running sum at line 9 = 3979,   19 = 9677,   32 = 18172
    # expect running avg at line 9 = 442.11, 19 = 509.32, 32 = 567.88
    # expect moving sum at line  9 = 1708,   19 = 3223,   32 = 2043
    # expect moving avg at line  9 = 341.60, 19 = 644.6,  32 = 408.6
    # expect moving max at line  9 = 941,    19 = 774,    32 = 978
    # expect running max (b) at  9 = 4770.1, 19 = 5074.1, 32 = 5606.36
    
    _testmgr.testcase_end(desc)

