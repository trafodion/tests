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

# TEST:0279 IN is a 3-valued predicate, EXISTS is 2-valued!

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
    stmt = """UPDATE WORKS
SET HOURS = NULL
WHERE PNUM = 'P5' OR EMPNUM = 'E4';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 4)
    # PASS:0279 If 4 rows are updated?
    stmt = """SELECT COUNT(*)
FROM STAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0279.exp""", """test0279b""")
    # PASS:0279 If count = 5?
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE 40 IN (SELECT HOURS FROM WORKS
WHERE STAFF.EMPNUM = WORKS.EMPNUM);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0279.exp""", """test0279c""")
    # PASS:0279 If count = 2?
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE 40 NOT IN (SELECT HOURS FROM WORKS
WHERE STAFF.EMPNUM = WORKS.EMPNUM);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0279.exp""", """test0279d""")
    # PASS:0279 If count = 2?
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE EXISTS (SELECT * FROM WORKS
WHERE HOURS = 40 AND
STAFF.EMPNUM = WORKS.EMPNUM);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0279.exp""", """test0279e""")
    # PASS:0279 If count = 2?
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE NOT EXISTS (SELECT * FROM WORKS
WHERE HOURS = 40 AND
STAFF.EMPNUM = WORKS.EMPNUM);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0279.exp""", """test0279f""")
    # PASS:0279 If count = 3?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0279 <<< END TEST
    
