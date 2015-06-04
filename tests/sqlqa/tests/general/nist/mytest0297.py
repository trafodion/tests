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

# TEST:0297 FIPS Flagger - vendor provided integer function!
# FIPS Flagger Test.  Support for this feature is not required.
# If supported, this feature must be flagged as an extension to the standard.
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
    stmt = """UPDATE STAFF
SET GRADE = -GRADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 5)
    
    # NOTE:0297 If the vendor does not pass this test, as written,
    # NOTE:0297    the vendor should replace the ABS(...) syntax below
    # NOTE:0297    with a vendor extension which selects 2 rows.
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE ABS(GRADE) = 12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0297.exp""", """test0297c""")
    # PASS:0297 If count = 2?
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # END TEST >>> 0297 <<< END TEST
    
