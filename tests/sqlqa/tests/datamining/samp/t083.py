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
    
def test001(desc="""test083"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test083
    # JClear
    # 1999-02-02
    # Sampling: FIRST-N after runningcount
    #
    stmt = """select runningcount(*) as rcount,
rows since (name is not null) as rowssince
from samptb077 
sample first 5 rows
sort by name
sequence by name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test083.exp""", 's1')
    # expect a running count from 1-5 and NULL followed by 5 ones
    
    stmt = """select runningcount(*) as rcount, name
from samptb077 
sample first 5 rows
sort by name
sequence by name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test083.exp""", 's2')
    # expect a running count from 1-5 and the following 5 names in order:
    #        1  Abbie
    #        2  Chris
    #        3  David
    #        4  Debbie
    #        5  Donna
    
    _testmgr.testcase_end(desc)

