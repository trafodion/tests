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

# TEST:0494 SQLSTATE 22003: data exception/numeric value out of range!

# setup
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """DELETE FROM HH;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    stmt = """INSERT INTO HH
VALUES (10);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0494 If 1 row is inserted?
    # PASS:0494 OR ERROR, data exception/numeric value out of range?
    # PASS:0494 OR 0 rows inserted OR SQLSTATE = 22003 OR SQLCODE < 0?
    stmt = """INSERT INTO HH
VALUES (100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0494 If 1 row is inserted?
    # PASS:0494 OR ERROR, data exception/numeric value out of range?
    # PASS:0494 OR 0 rows inserted OR SQLSTATE = 22003 OR SQLCODE < 0?
    stmt = """INSERT INTO HH
VALUES (1000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0494 If 1 row is inserted?
    # PASS:0494 OR ERROR, data exception/numeric value out of range?
    # PASS:0494 OR 0 rows inserted OR SQLSTATE = 22003 OR SQLCODE < 0?
    stmt = """INSERT INTO HH
VALUES (10000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0494 If 1 row is inserted?
    # PASS:0494 OR ERROR, data exception/numeric value out of range?
    # PASS:0494 OR 0 rows inserted OR SQLSTATE = 22003 OR SQLCODE < 0?
    stmt = """INSERT INTO HH
VALUES (100000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    # PASS:0494 If 1 row is inserted?
    # PASS:0494 OR ERROR, data exception/numeric value out of range?
    # PASS:0494 OR 0 rows inserted OR SQLSTATE = 22003 OR SQLCODE < 0?
    stmt = """INSERT INTO HH
VALUES (1000000);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    
    # PASS:0494 If 1 row is inserted?
    # PASS:0494 OR ERROR, data exception/numeric value out of range?
    # PASS:0494 OR 0 rows inserted OR SQLSTATE = 22003 OR SQLCODE < 0?
    
    # restore
    #    ROLLBACK WORK;
    stmt = """delete from hh;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    # END TEST >>> 0494 <<< END TEST
    
