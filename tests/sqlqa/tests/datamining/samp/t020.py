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
    
def test001(desc="""test020"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test020
    # JClear
    # 1999-02-01
    # Sampling tests: random sampling
    # These test results are very ramdom, so here's how we'll
    # test them:
    # 1. do a random query & insert the answer into a temp table
    #    query the temp table for a value between expected limits
    # 2. do a random query inserting the rows into a temp table
    #    count the rows and insert the value into temp table 2
    #    query the temp table for a value between expected limits
    # 3. selecting rows is also random so we get random counts of
    #    rows inserted.
    #    The last op of this script is to 'sed' out those lines
    #    before we do the diff.
    #
    stmt = """set param ?ten 10;"""
    output = _dci.cmdexec(stmt)
    
    # make sure the temp tables are empty
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from tempt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (intcol)
select count (*) from vwsamptb1 
sample random 10 percent rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where intcol between 0 and 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's2')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (intcol)
(select count (*) from vwsamptb1 
sample random 10 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where intcol between 0 and 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's4')
    # expect count = 1
    
    #- params not yet supported for sampling
    #- update tempt1 set intcol =
    #-   select count (*) from vwsamptb1
    #-     sample random ?ten percent rows;
    #- -- pass if 1 row is updated
    
    stmt = """select count (*) from tempt1 
where intcol between 0 and 25;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's5')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/test020.exp s6
    stmt = """insert into tempt1 
select a, b, c from vwsamptb1 
sample random 10 percent rows;"""
    output = _dci.cmdexec(stmt)
    # pass if 0-25 rows are inserted
    
    stmt = """insert into tempt2 (intcol)
select count (*) from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    #--------------------------
    # 09/18/07
    # Elena Krotkova
    # Binomial distribution
    # The lowest boundary should be 0
    # The highest boundary should be 26
    # For bigger numbers( 27 -100) probability is almost 0
    #--------------------------
    
    stmt = """select count (*) from tempt2 
where intcol between 0 and 26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's8')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select cast (avg (b) as numeric (15,2))
from vwsamptb1 
sample random 30 percent rows;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 7000 and 300000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's10')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select cast (variance (b) as numeric (15,2))
from vwsamptb1 
sample random 30 percent rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 40000000 and 155000000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's12')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select cast (stddev (b) as numeric (15,2))
from vwsamptb1 
sample random 30 percent rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 6500 and 15000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's14')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select sum (b) from vwsamptb1 
sample random 10 percent rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count (*) from tempt1 
where numcol between 15000 and 420000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test020.exp""", 's16')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

