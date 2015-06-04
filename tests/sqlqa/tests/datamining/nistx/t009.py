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
    
def test001(desc="""test009"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testx009
    # jclear
    # 1997-05-05
    # Extra tests on NIST database
    #
    stmt = """select empname from STAFF 
where empnum in
(select empnum from WORKS 
where pnum =
(select pnum from PROJ 
where pname = 'IRM')
or hours = 80)
and city in
(select city from PROJ 
where pnum =
(select pnum from WORKS 
where hours=80 and empnum = 'E2')
or pname = 'IRM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's1')
    # should select 'Betty'
    
    stmt = """select empname from STAFF 
where empnum in
(select empnum from WORKS 
where pnum =
(select pnum from PROJ 
where pname = 'IRM')
or hours = 80)
order by EMPNAME
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's2')
    # expect 3 rows with EMPNAME = Alice Betty Don
    
    stmt = """select empname from STAFF 
where city in
(select city from PROJ 
where pnum =
(select pnum from WORKS 
where hours=80 and empnum = 'E2')
or pname = 'IRM')
order by EMPNAME
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's3')
    # expect 2 rows with EMPNAME = Betty Carmen
    
    stmt = """select empname from VWSTAFF 
where empnum in
(select empnum from VWWORKS 
where pnum =
(select pnum from VWPROJ 
where pname = 'IRM')
or hours = 80)
and city in
(select city from VWPROJ 
where pnum =
(select pnum from VWWORKS 
where hours=80 and empnum = 'E2')
or pname = 'IRM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's4')
    # should select 'Betty'
    
    stmt = """select empname from VWSTAFF 
where empnum in
(select empnum from VWWORKS 
where pnum =
(select pnum from VWPROJ 
where pname = 'IRM')
or hours = 80)
order by EMPNAME
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's5')
    # expect 3 rows with EMPNAME = Alice Betty Don
    
    stmt = """select empname from VWSTAFF 
where city in
(select city from VWPROJ 
where pnum =
(select pnum from VWWORKS 
where hours=80 and empnum = 'E2')
or pname = 'IRM')
order by EMPNAME
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test009.exp""", 's6')
    # expect 2 rows with EMPNAME = Betty Carmen
    
    _testmgr.testcase_end(desc)

