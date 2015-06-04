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
    
def test001(desc="""test052"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test052
    # DDunn
    # 1999-01-18
    # Testing random sampling.
    # The result of avg(salary) should be different each time.
    # I am also testing to see if the count(*) is the same for each run.
    # Note: samptb051 has 37 rows, 20% of 37 is 7.4
    #
    # make sure the temp tables are empty
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from tempt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/test052.exp s1
    stmt = """insert into tempt1 
select empid, salary, age
from samptb051 
sample random 20 percent;"""
    output = _dci.cmdexec(stmt)
    # pass if 0-20 rows are inserted
    
    stmt = """insert into tempt2 (intcol)
select count (*) from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2 
where intcol between 0 and 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's3')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select cast (sum (salary) / 37 as dec (15,3))
from samptb051 
sample random 20 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 0 and 30000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's5')
    # expect count = 1
    
    stmt = """update tempt1 set numcol =
(select cast (avg (salary) as dec (15,3))
from samptb051 
sample random 20 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # pass if 1 row is updated
    
    stmt = """select count (*) from tempt1 
where numcol between 19000 and 55000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's7')
    # expect count = 1
    
    stmt = """update tempt1 set numcol =
(select count (*)
from samptb051 
sample random 20 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # pass if 1 row is updated
    
    stmt = """select count (*) from tempt1 
where numcol between 2 and 14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test052.exp""", 's9')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

