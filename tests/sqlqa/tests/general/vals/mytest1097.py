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

# TEST:0097 Subquery with AVG - 1 in <= comparison predicate!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """values ((
---   select *
select EMPNUM
from vwstaff
where grade <=
(select avg (grade) - 1
from vwstaff)
-- pass if empnum = E2
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test1097.exp""", """test097a""")
    
    stmt = """values ((
---   select *
select EMPNAME
from vwstaff
where grade <=
(select avg (grade) - 1
from vwstaff)
-- pass if empname = Betty
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test1097.exp""", """test097b""")
    
    stmt = """values ((
---   select *
select GRADE
from vwstaff
where grade <=
(select avg (grade) - 1
from vwstaff)
-- pass if grade = 10
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test1097.exp""", """test097c""")
    
    stmt = """values ((
---   select *
select CITY
from vwstaff
where grade <=
(select avg (grade) - 1
from vwstaff)
-- pass if city = Vienna
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test1097.exp""", """test097d""")
    
