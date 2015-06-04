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
    
def test001(desc="""test011"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testx011
    # jclear
    # 1997-05-05
    # Extra tests on NIST database
    #
    stmt = """select empname from STAFF 
where grade =
(select 4 * count (*) from PROJ 
where STAFF.city = PROJ.city)
or empnum in
(select empnum from WORKS 
where WORKS.empnum = STAFF.empnum)
order by empname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test011.exp""", 's1')
    # should select Alice, Betty, Carmen, Don
    
    stmt = """select empname from VWSTAFF 
where grade =
(select 4 * count (*) from VWPROJ 
where VWSTAFF.city = VWPROJ.city)
or empnum in
(select empnum from VWWORKS 
where VWWORKS.empnum = VWSTAFF.empnum)
order by empname;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test011.exp""", 's2')
    # should select Alice, Betty, Carmen, Don
    
    _testmgr.testcase_end(desc)

