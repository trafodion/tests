# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
    
def test001(desc="""test025"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test025
    # JClear
    # 1998-11-05
    # Sampling tests: random sampling before the where clause
    #
    # make sure the temp tables are empty
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from tempt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (intcol)
select count (*) from vwsamptb1 
where a between 0 and 50
sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where intcol between 0 and 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's2')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/test025.exp s3
    stmt = """insert into tempt1 
select a, b, c from vwsamptb1 
where a between 0 and 50
sample random 10 percent rows
order by a;"""
    output = _dci.cmdexec(stmt)
    # pass if 0-15 rows are inserted
    
    stmt = """insert into tempt2 (intcol)
select count (*) from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2 
where intcol between 0 and 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's5')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/test025.exp s6
    stmt = """insert into tempt1 
select a, b , c from vwsamptb1 
where a < 50
sample random 10 percent
order by a;"""
    output = _dci.cmdexec(stmt)
    # pass if 0-15 rows are inserted
    
    stmt = """insert into tempt2 (intcol)
select count (*) from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2 
where intcol between 0 and 15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's8')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile ${test_dir}/test025.exp s9
    stmt = """insert into tempt1 
select a, b, c from vwsamptb1 
where a < 50
sample random 10 percent rows;"""
    output = _dci.cmdexec(stmt)
    # pass if 0-15 rows are inserted
    
    stmt = """insert into tempt2 (intcol)
select count (*) from tempt1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt2 
where intcol between 0 and 19;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's11')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
select cast (avg (b) as numeric (15,2))
from vwsamptb1 
where a is not null and a > 0
sample random 10 percent;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 7000 and 21000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's13')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select cast (variance (b) as numeric (15,2))
from vwsamptb1 
where a is not null and a > 0
sample random 10 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 12500000 and 220000000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's15')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select cast (stddev (b) as numeric (15,2))
from vwsamptb1 
where a is not null and a > 0
sample random 10 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 500 and 20000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's17')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select cast (avg (b) as numeric (15,2))
from vwsamptb1 
where a is not null and a < 1000
sample random 10 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 3000 and 25000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's19')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select cast (variance (b) as numeric (15,2))
from vwsamptb1 
where a is not null and a < 1000
sample random 10 percent);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 5500000 and 320000000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's21')
    # expect count = 1
    
    stmt = """delete from tempt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tempt1 (numcol)
(select sum (b) from vwsamptb1 
where a < 50
sample random 10 percent rows);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # pass if 1 row is inserted
    
    stmt = """select count (*) from tempt1 
where numcol between 3000 and 220000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test025.exp""", 's23')
    # expect count = 1
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

