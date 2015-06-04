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

# test003
# JClear
# 1999-04-06
# VALUES tests -- to upper string functions
#
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """values (1, 2, 3, (select upshift (fname) from valtb003),
(select upper (minit) from valtb003),
(select ucase (lname) from valtb003));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", """test003a""")
    
    stmt = """values (2, 3, 4, (select lcase (fname) from valtb003),
(select lcase (minit) from valtb003),
(select lower (lname) from valtb003),
null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test003.exp""", """test003b""")
    
