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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""test086"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test086
    # JClear
    # 1999-05-24
    # sample test: oversampling random
    #
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select avg (x) from vwsamptb085b 
sample random 150 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count (*) from tempt1 
where numcol between 109 and 115;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test086.exp""", 's2')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select avg (x) from vwsamptb085b 
sample random 150 percent clusters of 1 blocks;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4113')
    
    stmt = """select count (*) from tempt1 
where numcol between 109 and 115;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test086.exp""", 's4')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

