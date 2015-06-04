# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc='grant privileges'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    tablelist = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't66', 't7', 't8', 't9', 't10', 'cube1', 'cube2', 'cube3', 'cube4']

    for table in tablelist:
        # set privilege
        stmt = 'revoke all on table ' + table + ' from PUBLIC;'
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)

        stmt = 'grant select on table ' + table + ' to PUBLIC;'
        output = _dci.cmdexec(stmt)
        _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

