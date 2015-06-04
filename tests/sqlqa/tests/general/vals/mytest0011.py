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

# test0011
# JClear
# 1999-04-07
# VALUES tests: using NIST test0011
#
# TEST:0011 FIPS sizing - DECIMAL (15)!
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
    stmt = """delete from vwlongint;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """insert into vwlongint
VALUES(123456789012345.);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # PASS:0011 If 1 row is inserted?
    
    stmt = """values ((
select long_int
from vwlongint
), (
select cast (long_int / 1000000 as dec (18,7))
from vwlongint
), (
select long_int - 123456789000000.
from vwlongint
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test011.exp""", """test011b""")
    
    # PASS:0011 If values are (123456789012345, 123456789, 12345), but?
    # PASS:0011 Second value may be between 123456788 and 123456790?
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
