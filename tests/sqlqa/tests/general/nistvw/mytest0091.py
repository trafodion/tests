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

# TEST:0091 Data type FLOAT!

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
    _dci.expect_complete_msg(output)
    
    # setup
    stmt = """INSERT INTO JJ
VALUES(12.345678,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0091 If 1 row is inserted?
    
    stmt = """SELECT FLOATTEST
FROM VWJJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0091.exp""", """s1""")
    # PASS:0091 If FLOATTEST = 12.345678 ?
    # PASS:0091 OR  is between 12.345673 and 12.345683 ?
    
    stmt = """SELECT *
FROM VWJJ
WHERE FLOATTEST > 12.345672 and FLOATTEST < 12.345684;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0091.exp""", """s2""")
    # PASS:0091 If 1 row selected?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWJJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0091.exp""", """s3""")
    # pass if count = 0
    