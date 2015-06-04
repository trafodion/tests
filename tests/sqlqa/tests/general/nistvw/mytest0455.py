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

# TEST:0455 Relaxed union compatability rules for columns!
# NOTE:  OPTIONAL FIPS Flagger test
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
    
    stmt = """SELECT EMPNUM, CITY FROM VWSTAFF
UNION
SELECT PTYPE, CITY FROM VWPROJ
order by EMPNUM, CITY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0455.exp""", """s1""")
    
    # PASS:0455 If 9 rows are selected?
    # NOTE:0455 Shows support for UNION of CHAR columns
    # NOTE:0455   with different lengths.
    
    stmt = """SELECT EMPNUM, CITY FROM VWSTAFF
UNION
SELECT 'e1 ', CITY FROM VWPROJ
order by EMPNUM, CITY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0455.exp""", """s2""")
    
    # PASS:0455 If 8 rows selected?
    # NOTE:0455 Shows support for UNION of Char column
    # NOTE:0455   with CHAR literal.
    
    stmt = """SELECT EMPNUM, GRADE FROM VWSTAFF
UNION
SELECT EMPNUM, HOURS FROM VWWORKS
order by EMPNUM, GRADE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0455.exp""", """s3""")
    
    # PASS:0455 If 14 rows selected?
    # NOTE:0455 Shows support for UNION of DECIMAL columns
    # NOTE:0455   with different precision.
    
    # END TEST >>> 0455 <<< END TEST
