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

# TEST:0436 NULL values for various SQL data types!

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
    
    stmt = """INSERT INTO BBB VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO EEE VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO GGG VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO HHH VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO III VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO JJJ VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO MMM VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO SSS VALUES(NULL,1);"""
    output = _dci.cmdexec(stmt)
    stmt = """SELECT CHARTEST
FROM BBB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436a""")
    # PASS:0436 If CHARTEST is NULL (Implementor defined print format)?
    stmt = """SELECT INTTEST
FROM EEE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436b""")
    # PASS:0436 If INTTEST is NULL (Implementor defined print format)?
    stmt = """SELECT REALTEST
FROM GGG;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436c""")
    # PASS:0436 If REALTEST is NULL (Implementor defined print format)?
    stmt = """SELECT COUNT(*)
FROM GGG
WHERE REALTEST IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436d""")
    # PASS:0436 If count = 1?
    stmt = """SELECT SMALLTEST
FROM HHH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436e""")
    # PASS:0436 If SMALLTEST is NULL (Implementor defined print format)?
    stmt = """SELECT DOUBLETEST
FROM III;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436f""")
    # PASS:0436 If DOUBLETEST is NULL (Implementor defined print format)?
    stmt = """SELECT COUNT(*)
FROM III
WHERE DOUBLETEST IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436g""")
    # PASS:0436 If count = 1?
    stmt = """SELECT FLOATTEST
FROM JJJ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436h""")
    # PASS:0436 If FLOATTEST is NULL (Implementor defined print format)?
    stmt = """SELECT COUNT(*)
FROM JJJ
WHERE FLOATTEST IS NULL;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436i""")
    # PASS:0436 If count = 1?
    stmt = """SELECT NUMTEST
FROM MMM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436j""")
    # PASS:0436 If NUMTEST is NULL (Implementor defined print format)?
    stmt = """SELECT NUMTEST
FROM SSS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0436.exp""", """test0436k""")
    # PASS:0436 If NUMTEST is NULL (Implementor defined print format)?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0436 <<< END TEST
    
