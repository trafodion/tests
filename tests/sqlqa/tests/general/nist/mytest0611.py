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

# TEST:0611 FIPS sizing, DATETIME data types (static)!

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    stmt = """CREATE TABLE TSFIPS (
FIPS1 TIME,
FIPS2 TIMESTAMP,
FIPS3 INTERVAL YEAR (2) TO MONTH,
FIPS4 INTERVAL DAY (2) TO SECOND (6)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # PASS:0611 If table is created?
    
    #    COMMIT WORK;		-- XXXXX
    stmt = """INSERT INTO TSFIPS VALUES (
TIME '16:03:00',
TIMESTAMP '1996-08-24 16:03:00.999999',
INTERVAL -'99-6' YEAR (2) TO MONTH,
INTERVAL '99 0:10:00.999999' DAY (2) TO SECOND (6)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0611 If 1 row is inserted?
    stmt = """SELECT EXTRACT (SECOND FROM FIPS2)
* 1000000 - 999990 FROM TSFIPS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0611.exp""", """test0611c""")
    
    # PASS:0611 If 1 row selected and value is 9?
    stmt = """SELECT EXTRACT (YEAR FROM FIPS3),
EXTRACT (MONTH FROM FIPS3)
FROM TSFIPS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0611.exp""", """test0611d""")
    
    # PASS:0611 If 1 row selected and values are -99 and -6?
    stmt = """SELECT EXTRACT (DAY FROM FIPS4),
EXTRACT (SECOND FROM FIPS4) * 1000000 - 999990
FROM TSFIPS;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0611.exp""", """test0611e""")
   
    stmt = """DROP TABLE TSFIPS CASCADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    # PASS:0611 If 1 row selected and values are 99 and 9?
    # stmt = """ROLLBACK WORK;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    #   DROP TABLE TSFIPS CASCADE;		-- XXXXX
    
    #    COMMIT WORK;		-- XXXXX
    
    # END TEST >>> 0611 <<< END TEST
    
