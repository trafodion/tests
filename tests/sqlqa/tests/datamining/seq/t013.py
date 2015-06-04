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
    
def test001(desc="""test013"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test013
    # Sequence function tests: test for RUNNINGMAX(column)
    #
    stmt = """select runningmax (i1) as runningmax_i1, i1
from vwseqtb2 sequence by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013.exp""", 's1')
    # expect two columns of numbers 1 - 20
    
    stmt = """select runningmax (i1) as runningmax_i1, i1
from vwseqtb2 sequence by ts asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013.exp""", 's2')
    # expect two columns of numbers 1 - 20
    
    stmt = """select runningmax (i1) as runningmax_i1, i1
from vwseqtb2 sequence by ts desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test013.exp""", 's3')
    # expect 20 rows of sorted data like this:
    
    # RUNNINGMAX_I1  I1
    # -------------  -----------
    #
    #            20           20
    #            20           19
    #            20           18
    #            20           17
    #            20           16
    #            20           15
    #            20           14
    #            20           13
    #            20           12
    #            20           11
    #            20           10
    #            20            9
    #            20            8
    #            20            7
    #            20            6
    #            20            5
    #            20            4
    #            20            3
    #            20            2
    #            20            1
    
    _testmgr.testcase_end(desc)

