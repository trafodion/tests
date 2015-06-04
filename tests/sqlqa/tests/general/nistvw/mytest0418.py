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

# TEST:0418 AVG, SUM, COUNT on Cartesian product with NULL!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT AVG(T1.COL4), AVG(T1.COL4 + T2.COL4),
SUM(T2.COL4), COUNT(DISTINCT T1.COL4)
FROM VTABLE T1, VTABLE T2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0418.exp""", """s1""")
    
    # PASS:0418 If AVG(T1.COL4) = 147 or 148?
    # PASS:0418 If AVG(T1.COL4 + T2.COL4) = 295 or 296?
    # PASS:0418 If SUM(T2.COL4) = 1772?
    # PASS:0418 If COUNT(DISTINCT T1.COL4) = 3?
    
    # END TEST >>> 0418 <<< END TEST
    
