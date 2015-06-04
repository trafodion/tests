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

# TEST:0299 FIPS Flagger - identifier length > 18!
# NOTE:  OPTIONAL FIPS Flagger test
# FIPS Flagger Test.  Support for this feature is not required.
# If supported, this feature must be flagged as an extension to the standard.

# NOTE:0299 Delete any SQL statement which causes
# NOTE:0299   this procedure to abort.  But, there
# NOTE:0299   is no need to remove a statement with a warning.

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
    stmt = """INSERT INTO TABLEFGHIJKLMNOPQ19 VALUES (299);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO SHORTTABLE VALUES (299);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO BASETABLE1 VALUES (299);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """SELECT COL2                 FROM  TABLEFGHIJKLMNOPQ19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0299.exp""", """test0299d""")
    stmt = """SELECT COLUMN123456789IS19  FROM  SHORTTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0299.exp""", """test0299e""")
    stmt = """SELECT COL3                 FROM  VIEWABCDEFGHIKLMN19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0299.exp""", """test0299f""")
    # PASS:0299 If the value 299 is selected by any of SQL SELECTs above?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """select count (*) FROM BASETABLE1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0299.exp""", """test0299h""")
    # pass if count = 0
    stmt = """select count (*) FROM SHORTTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0299.exp""", """test0299i""")
    # pass if count = 0
    stmt = """select count (*) FROM TABLEFGHIJKLMNOPQ19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0299.exp""", """test0299j""")
    # pass if count = 0
    
    # END TEST >>> 0299 <<< END TEST
    
