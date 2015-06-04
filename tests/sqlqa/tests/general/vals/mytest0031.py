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

# test0031
# JClear
# 1999-04-08
# VALUES tests: using NIST test0031
#
# TEST:0031 INSERT(column list) VALUES(NULL and literals)!

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
    stmt = """insert into TMP (T2, T3, T1)
VALUES (NULL,'zz','z');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0031 If 1 row inserted?
    
    stmt = """values ((
SELECT T1
FROM VWTMP
WHERE T2 IS NULL
), (
SELECT T2
FROM VWTMP
WHERE T2 IS NULL
), (
SELECT T3
FROM VWTMP
WHERE T2 IS NULL
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test031.exp""", """test031b""")
    
    # PASS:0031 If T1 = 'z         '?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """values ((
select count (*) FROM VWTMP
-- pass if count = 0
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test031.exp""", """test031c""")
    
    # END TEST >>> 0031 <<< END TEST
    
