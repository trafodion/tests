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
    
def test001(desc="""test106"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test106
    # Sqlci hangs on Sequence running functions with PCODE turned off
    #
    # Also seen with MOVINGMAX and the DIFF functions (all 4 variations)
    #
    #    create table seqtb106 (a int, b int, c smallint, d largeint);
    #
    #    insert into seqtb106 values
    #        (2, 74, 27648, 498921136),
    #        (80, 24011, 22223, 859834),
    #        (89, 28238, 28519, 285854226),
    #        (51, 15294, 18450, 100322507),
    #        (33, 9031, 32354, 1130723134),
    #        (53, 15474, 5573, 476322978),
    #        (50, 15250, 24665, 196331131),
    #        (71, null, 27138, 37182688),
    #        (76, 23010, 6585, 666815330),
    #        (47, 13457, 32039, 186130057);
    #
    #
    stmt = """set envvar PCODE off;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
runningsum(b) as rsum_b
from seqtb106 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test106.exp""", 's1')
    
    stmt = """select a, b,
runningcount(*) as rcount_star,
movingmax(b,3) as mmax_b4
from seqtb106 
sequence by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test106.exp""", 's2')
    
    _testmgr.testcase_end(desc)

