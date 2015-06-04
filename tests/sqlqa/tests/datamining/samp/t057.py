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
    
def test001(desc="""test057"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test057
    # DDunn
    # 1999-01-18
    # Verify that random sample really returns r * N/100
    #	where r is the percent and N is the total rows in the query.
    # 37 rows exist and we are asking for 20 percent.  So 7.4 should actually
    # be returned.  Round down to 7 or up to 8 rows.  Expecting 7 or 8 rows.
    # Additionally, testing that the same rows are returned for periodic sample
    # with the sort by clause.
    #
    # make sure the temp tables are empty
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from tempt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select count(salary)
from samptb051 
sample random 20 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 0-20 rows are selected
    
    stmt = """insert into tempt2 (intcol)
select numcol from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count(intcol) from tempt2 
where intcol between 0 and 20;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test057.exp""", 's3')
    
    # pass if 0-20 rows are selected
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select count(salary)
from samptb051 
sample periodic 2 rows every 10 rows
sort by age;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 2-13 rows are selected
    
    stmt = """insert into tempt2 (intcol)
select intcol from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count(intcol) from tempt2 
where intcol between 2 and 13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test057.exp""", 's6')
    # pass if 2-13 rows are selected
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select salary
from samptb051 
sample first 10 rows
sort by age;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test057.exp""", 's7')
    # expect 10 rows with the following values in this order
    #       40000.00
    #       45000.00
    #       55000.00
    #       25000.00
    #       30000.00
    #       40000.00
    #       36000.00
    #       60000.00
    #       20050.00
    #       20000.00
    
    _testmgr.testcase_end(desc)

