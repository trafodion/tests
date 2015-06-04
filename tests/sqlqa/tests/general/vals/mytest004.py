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

# test004
# JClear
# 1999-04-06
# VALUES tests -- datetime functions
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
    
    stmt = """values (extract (year from date '1999-12-31'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test004.exp""", """test004a""")
    # expect 1999
    
    stmt = """values (week (date '12/26/1999'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test004.exp""", """test004b""")
    # expect 53 (actually 52 and a fraction)
    
    stmt = """values (dayname (date '25.12.1999'),
dayofmonth (date '25.12.1999'),
monthname (date '25.12.1999'),
year (date '25.12.1999')
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test004.exp""", """test004c""")
    # expect Saturday 25 December 1999
    
    stmt = """values (dayofweek
(converttimestamp
(juliantimestamp
(timestamp '1999-12-25 00:00:00.000')
)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test004.exp""", """test004d""")
    # expect 7 (Saturday)
    
