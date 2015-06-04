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

# TEST:0214 FIPS sizing -- 2000-byte row!
# FIPS sizing TEST

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
    stmt = """INSERT INTO T2000(STR110,STR200,STR216)
VALUES
('STR11111111111111111111111111111111111111111111111',
'STR22222222222222222222222222222222222222222222222',
'STR66666666666666666666666666666666666666666666666');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0214 If 1 row is inserted?
    
    stmt = """select count (*) from VWT2000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0214.exp""", """s1""")
    
    stmt = """UPDATE T2000
SET STR140 =
'STR44444444444444444444444444444444444444444444444';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0214 If 1 row is updated?
    
    stmt = """select STR140
from VWT2000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0214.exp""", """s2""")
    
    stmt = """UPDATE T2000
SET STR180 =
'STR88888888888888888888888888888888888888888888888';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # PASS:0214 If 1 row is updated?
    
    stmt = """SELECT STR110,STR180,STR216
FROM VWT2000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0214.exp""", """s3""")
    # PASS:0214 If STR110 = ?
    # PASS:0214   'STR11111111111111111111111111111111111111111111111'?
    # PASS:0214 If STR180 = ?
    # PASS:0214   'STR88888888888888888888888888888888888888888888888'?
    # PASS:0214 If STR216 = ?
    # PASS:0214   'STR66666666666666666666666666666666666666666666666'?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) from VWT2000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0214.exp""", """s4""")
    # pass if count = 0
    
