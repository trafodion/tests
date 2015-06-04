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

# test0020
# JClear
# 1999-04-07
# VALUES tests: using NIST test0020
#
# TEST:0020 SELECT NULL value !

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    # setup
    stmt = """insert into WORKS
VALUES('E18','P18',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0020 If 1 row is inserted?
    
    stmt = """values ((
SELECT HOURS
FROM   VWWORKS
WHERE  EMPNUM='E18' AND PNUM='P18'
), (
SELECT EMPNUM
FROM   VWWORKS
WHERE  EMPNUM='E18' AND PNUM='P18'
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", """test020b""")
    
    # PASS:0020 If EMPNUM = 'E18' and HOURS is NULL?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values ((
select count (*) from VWWORKS
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", """test020c""")
    # pass if count = 12
    
    # END TEST >>> 0020 <<< END TEST
    
