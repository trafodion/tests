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

# TEST:0267 Update compound key, interim uniqueness conflict!

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
    stmt = """DELETE FROM WORKS1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO WORKS1 VALUES
('P1','P6',1),
('P2','P6',2),
('P3','P6',3),
('P4','P6',4),
('P5','P6',5),
('P6','P6',6),
('P1','P5',7),
('P2','P5',8),
('P3','P5',9),
('P4','P5',10),
('P5','P5',11),
('P6','P5',12),
('P1','P4',13),
('P2','P4',14),
('P3','P4',15),
('P4','P4',16),
('P5','P4',17),
('P6','P4',18),
('P1','P3',19),
('P2','P3',20),
('P3','P3',21),
('P4','P3',22),
('P5','P3',23),
('P6','P3',24),
('P1','P2',25),
('P2','P2',26),
('P3','P2',27),
('P4','P2',28),
('P5','P2',29),
('P6','P2',30),
('P1','P1',31),
('P2','P1',32),
('P3','P1',33),
('P4','P1',34),
('P5','P1',35),
('P6','P1',36);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 36)
    ##expectfile ${test_dir}/test0267.exp test0267c
    stmt = """UPDATE WORKS1
SET PNUM = EMPNUM, EMPNUM = PNUM;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 36)
    # PASS:0267 If 0 rows are updated?
    stmt = """SELECT COUNT(*)
FROM WORKS1
WHERE EMPNUM = 'P1' AND HOURS > 30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0267.exp""", """test0267d""")
    # PASS:0267 If count = 6?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0267 <<< END TEST
    
