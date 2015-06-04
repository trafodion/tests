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
    
def test001(desc="""test054"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test054
    # DDunn
    # 1999-01-18
    # Testing random sampling.
    # Testing oversampling.  I will ask for 150percent, therefore the query should
    # return 45 rows with half of the rows duplicated.
    # Then I delete 1 row so that the number of existing rows is not an even
    # number in order to see how MX handles.
    # This time the query should return 43 or 44.
    #
    # make sure the temp tables are empty
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from tempt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    # pass if 30-55 rows are selected
    stmt = """insert into tempt2 (intcol)
select count (*) from samptb054 
sample random 150 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2 
where intcol between 30 and 55;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test054.exp""", 's2')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from samptb054 where empid = 9789;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # expect 1 row deleted
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    # pass if 30-55 rows are selected
    stmt = """insert into tempt2 (intcol)
select count (*) from samptb054 
sample random 150 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2 
where intcol between 30 and 55;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test054.exp""", 's5')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

