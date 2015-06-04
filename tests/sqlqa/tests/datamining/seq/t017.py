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
    
def test001(desc="""test017"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test017
    # Sequence function tests: test for RUNNINGVARIANCE(column)
    #
    stmt = """select i1,
cast (runningvariance (i1) as dec (18,3)) as runningvariance_i1,
cast (runningstddev (i1) as dec (18,3)) as runningstddev_i1
from vwseqtb2 please
sequence by ts;"""
    output = _dci.cmdexec(stmt)
    # expect the following values in order
    #          1                  .000                  .000
    #          2                  .500                  .707
    #          3                 1.000                 1.000
    #          4                 1.666                 1.290
    #          5                 2.500                 1.581
    #          6                 3.500                 1.870
    #          7                 4.666                 2.160
    #          8                 6.000                 2.449
    #          9                 7.500                 2.738
    #         10                 9.166                 3.027
    #         11                11.000                 3.316
    #         12                13.000                 3.605
    #         13                15.166                 3.894
    #         14                17.500                 4.183
    #         15                20.000                 4.472
    #         16                22.666                 4.760
    #         17                25.500                 5.049
    #         18                28.500                 5.338
    #         19                31.666                 5.627
    #         20                35.000                 5.916
    
    _testmgr.testcase_end(desc)

