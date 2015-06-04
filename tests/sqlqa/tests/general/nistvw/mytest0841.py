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

# TEST:0841 Multiple-join and default order of joins !

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
    stmt = """DELETE FROM STAFF3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """INSERT INTO STAFF3
SELECT * FROM VWSTAFF;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #    DELETE FROM HU.STAFF4;		XXXXX
    stmt = """DELETE FROM STAFF4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    #    INSERT INTO HU.STAFF4		XXXXX
    #       SELECT * FROM HU.STAFF3	XXXXX
    stmt = """INSERT INTO STAFF4
SELECT * FROM VWSTAFF3
WHERE EMPNUM > 'E3';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """SELECT EMPNUM FROM
--       HU.STAFF3 NATURAL LEFT JOIN HU.STAFF NATURAL INNER JOIN HU.STAFF4
VWSTAFF3 NATURAL LEFT JOIN VWSTAFF NATURAL INNER JOIN VWSTAFF4
ORDER BY EMPNUM DESC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0841.exp""", """s1""")
    # PASS:0841 If 2 rows selected?
    # PASS:0841 If ordered EMPNUM values are: E5, E4 ?
    
    stmt = """SELECT EMPNUM FROM
--       (HU.STAFF3 NATURAL LEFT JOIN HU.STAFF) NATURAL INNER JOIN HU.STAFF4
(VWSTAFF3 NATURAL LEFT JOIN VWSTAFF) NATURAL INNER JOIN VWSTAFF4
ORDER BY EMPNUM ASC;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0841.exp""", """s2""")
    # PASS:0841 If 2 rows selected?
    # PASS:0841 If ordered EMPNUM values are: E4, E5 ?
    
    stmt = """SELECT EMPNUM FROM
--       HU.STAFF3 NATURAL LEFT JOIN (HU.STAFF NATURAL INNER JOIN HU.STAFF4)
VWSTAFF3 NATURAL LEFT JOIN (VWSTAFF NATURAL INNER JOIN VWSTAFF4)
ORDER BY EMPNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0841.exp""", """s3""")
    # PASS:0841 If 5 rows selected?
    # PASS:0841 If ordered EMPNUM values are: E1, E2, E3, E4, E5 ?
    
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) FROM VWSTAFF4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0841.exp""", """s4""")
    # pass if count = 0
    
    # END TEST >>> 0841 <<< END TEST
    
