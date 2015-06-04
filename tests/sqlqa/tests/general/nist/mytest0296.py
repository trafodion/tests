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

# TEST:0296 FIPS Flagger - vendor provided character function!
# FIPS Flagger Test.  Support for this feature is not required.
# If supported, this feature must be flagged as an extension to the standard.

# NOTE:0296 If the vendor does not pass this test, as written,
# NOTE:0296    the vendor should replace the SUBSTR(...) syntax below
# NOTE:0296    with a vendor extension which selects exactly 1 row.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """SELECT COUNT(*)
FROM STAFF
WHERE SUBSTRING (EMPNAME,1,3) = 'Ali';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0296.exp""", """test0296""")
    # PASS:0296 If count = 1?
    
    # END TEST >>> 0296 <<< END TEST
    
