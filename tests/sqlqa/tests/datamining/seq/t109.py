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
    
def test001(desc="""test109"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test109
    # jc
    # 2002-08-09
    # Test for the fix to the Average functions:
    # Treat NULL not as a 0 but as a NULL and don't count the row as a row.
    #    create table seqtb109 (a real, b float);
    #
    stmt = """BEGIN WORK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into seqtb109 values
(1, 3.5, 1), (2, 4.5, 2), (3, null, 3), (4, 2.75, 4), (5, 4.4, 5),
(6, 4.6, 6), (7, null, 7), (8, 5.8, 8), (9, 3.63, 9), (10, 9.84, 10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 10)
    
    stmt = """select cast (a as int) as col_a, cast (b as dec (18,3)) as col_b,
cast (RUNNINGSUM (b) as dec (18,3)) as rsum,
cast (RUNNINGAVG (b) as dec (18,3)) as ravg,
cast (MOVINGAVG (b, 5) as dec (18,3)) as mvavg
from seqtb109 sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test109.exp""", 's2')
    
    # Expecting
    #    A     B    RSum    RAvg   MvAvg
    #  -----------------------------------
    #    1  3.500   3.500  3.500   3.500
    #    2  4.500   8.000  4.000   4.000
    #    3      ?   8.000  4.000   4.000
    #    4  2.750  10.750  3.583   3.583
    #    5  4.400  15.150  3.788   3.788
    #    6  4.600  19.750  3.950   4.063
    #    7      ?  19.750  3.950   3.917
    #    8  5.800  25.550  4.258   4.388
    #    9  3.630  29.180  4.169   4.607
    #   10  9.840  39.020  4.877   5.967
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

