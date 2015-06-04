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
    
def test001(desc="""test003"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test003
    # Sequence function tests: based on the example from the External Specs. p.8
    #
    stmt = """SELECT RUNNINGCOUNT (*) as rc_star,
C,
RUNNINGSUM (C) as rsum,
cast (RUNNINGAVG (C) as dec (18,2)) as ravg,
MOVINGSUM (C, 5) as mvsum,
cast (MOVINGAVG (C, 5) as dec (18,2)) as mvavg,
RUNNINGMAX (C) as runmax
---     MOVINGMAX (C, 5) as mvmax, Gets Error while fetching from the TCB tree.
FROM seqtb4 
SEQUENCE BY I
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", 's1')
    # expect 10 rows in order with the following values
    #
    #    RC_STAR   C   RSUM     RAVG    MVSUM   MVAVG  RUNMAX
    #        1     2      2     2.00      2      2.00     2
    #        2     4      6     3.00      6      3.00     4
    #        3     6     12     4.00     12      4.00     6
    #        4     8     20     5.00     20      5.00     8
    #        5     ?     20     5.00     20      5.00     8
    #        6     5     25     5.00     23      5.75     8
    #        7     7     32     5.33     26      6.50     8
    #        8     9     41     5.85     29      7.25     9
    #        9    11     52     6.50     32      8.00    11
    #       10    10     62     6.88     42      8.40    11
    
    stmt = """select c, MOVINGSUM (C, 5) as mvsum
from vwseqtb4 
sequence by I;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", 's2')
    # expect 10 rows in order with the following values
    #           2                      2
    #           4                      6
    #           6                     12
    #           8                     20
    #           ?                     20
    #           5                     23
    #           7                     26
    #           9                     29
    #          11                     32
    #          10                     42
    
    _testmgr.testcase_end(desc)

