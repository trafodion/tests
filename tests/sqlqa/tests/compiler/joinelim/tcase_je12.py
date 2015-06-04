# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# =================  Begin Test Case Header  ==================
#
#  Description:        Miscellaneous tests for join elimination and
#                      extra-hub marking.
#  Purpose:
#
#
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Join elimination with mismatched partially null foreign key"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # insert referencing row that doesn't match referenced row, but has partially
    # null foreign key.
    stmt = """insert into m4 values(1,2,3,'');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into m3 values(1,2,3,8,9,null,'');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # Do a join elimination query and check the results.
    stmt = """prepare s from
select pk3a
from m3, m4
where fk34a=pk4a and fk34b=pk4b and fk34c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #unexpect any *_scan*M4*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # restore table content
    stmt = """delete from m3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from m4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

