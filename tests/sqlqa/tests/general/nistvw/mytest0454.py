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

# TEST:0454 SELECT nonGROUP column in GROUP BY!
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
    
    stmt = """SELECT PTYPE, CITY, SUM (BUDGET), COUNT(*)
FROM VWPROJ
GROUP BY CITY
ORDER BY CITY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4005')
    
    # PASS:0454 If either 3, 4, or 6 rows are selected?
    # NOTE:0454 If 3 rows, then note whether sample CITY is given.
    # NOTE:0454 If 4 or 6 rows, then note whether SUM and COUNT
    # NOTE:0454   are for CITY or for PTYPE within CITY.
    
    # END TEST >>> 0454 <<< END TEST
