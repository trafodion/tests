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

# TEST:0411 Effective set difference!
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT W1.EMPNUM FROM WORKS W1
WHERE W1.PNUM = 'P2'
AND NOT EXISTS (SELECT * FROM WORKS W2
WHERE W2.EMPNUM = W1.EMPNUM
AND W2.PNUM = 'P1')
ORDER BY 1 ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0411.exp""", """test0411""")
    
    # PASS:0411 If 2 rows are selected?
    # PASS:0411 If FOR ROW #1, W1.EMPNUM = 'E3'?
    # PASS:0411 If FOR ROW #2, W1.EMPNUM = 'E4'?
    
    # END TEST >>> 0411 <<< END TEST
    
