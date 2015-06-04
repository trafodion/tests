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

# TEST:0112 Search condition unknown AND true!

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
    stmt = """insert into works
VALUES ('E8','P8',NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # PASS:0112 If 1 row is inserted?
    
    stmt = """values ((
select empnum
from   vwworks
where hours < (select hours from vwworks
where empnum = 'E8')
and hours in (select hours from vwworks)
), (
select pnum
from   vwworks
where hours < (select hours from vwworks
where empnum = 'E8')
and hours in (select hours from vwworks)
));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test1112.exp""", """test1112b""")
    
    # PASS:0112 If 0 rows are selected?
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
